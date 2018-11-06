from django.conf.urls import url


from booking.apis import RoomTypeListApi, BookingRequestApi

urlpatterns = [
    url(
        regex=r'^room-types//$',
        view=RoomTypeListApi.as_view(),
        name='room-type-list'
    ),
    url(
        regex=r'^booking-request/$',
        view=BookingRequestApi.as_view(),
        name='booking-request'
    ),
]
