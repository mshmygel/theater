from rest_framework import routers

from theater.views import (
    GenreViewSet,
    ActorViewSet,
    TheaterHallViewSet,
    PlayViewSet,
    PerformanceViewSet,
    ReservationViewSet,
)

router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("theater_halls", TheaterHallViewSet)
router.register("plays", PlayViewSet)
router.register("performances", PerformanceViewSet)
router.register("reservations", ReservationViewSet)


urlpatterns = router.urls

app_name = "theater"
