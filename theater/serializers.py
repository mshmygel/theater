from django.utils.timezone import now
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from theater.models import (
    Genre,
    Actor,
    TheaterHall,
    Play,
    Performance,
    Ticket,
    Reservation,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class TheaterHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheaterHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "genres",
            "actors",
        )


class PlayListSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True, slug_field="name"
    )
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )

    class Meta:
        model = Play
        fields = ("id", "title", "genres", "actors", "image")


class PlayDetailSerializer(PlaySerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "genres",
            "actors",
            "image",
        )


class PlayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "image")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "show_time", "play", "theater_hall")

    def validate_show_time(self, value):
        if value < now():
            raise serializers.ValidationError(
                "Show time cannot be in the past."
            )
        return value


class PerformanceListSerializer(PerformanceSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    play_image = serializers.ImageField(source="play.image", read_only=True)
    theater_hall_name = serializers.CharField(
        source="theater_hall.name", read_only=True
    )
    theater_hall_capacity = serializers.IntegerField(
        source="theater_hall.capacity", read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Performance
        fields = (
            "id",
            "show_time",
            "play_title",
            "play_image",
            "theater_hall_name",
            "theater_hall_capacity",
            "tickets_available",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["performance"].theater_hall,
            ValidationError,
        )

        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance")


class TicketListSerializer(TicketSerializer):
    # performance = PerformanceListSerializer(many=False, read_only=True)
    performance = serializers.SerializerMethodField()

    def get_performance(self, obj):
        return {
            "id": obj.performance.id,
            "show_time": obj.performance.show_time,
            "play_title": obj.performance.play.title,
            "play_image": (
                obj.performance.play.image.url
                if obj.performance.play.image
                else None
            ),
            "theater_hall_name": obj.performance.theater_hall.name,
            "theater_hall_capacity": obj.performance.theater_hall.capacity,
        }

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance")


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayListSerializer(many=False, read_only=True)
    theater_hall = TheaterHallSerializer(many=False, read_only=True)
    taken_places = TicketSerializer(
        source="tickets",
        many=True,
        read_only=True
    )

    class Meta:
        model = Performance
        fields = ("id", "show_time", "play", "theater_hall", "taken_places")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            # for ticket_data in tickets_data:
            #     Ticket.objects.create(reservation=reservation, **ticket_data)
            tickets = [
                Ticket(reservation=reservation, **ticket_data)
                for ticket_data in tickets_data
            ]
            Ticket.objects.bulk_create(tickets)
            return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")
