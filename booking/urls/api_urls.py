from django.conf.urls import url


from booking.apis import (
    RoomTypeListApi,
    BookingRequestApi,
    EmailExistApi,
    MealListApi,
    BookingRequestsApi,
    CheckPhoneApi
)

urlpatterns = [
    url(
        regex=r'^room-types/$',
        view=RoomTypeListApi.as_view(),
        name='room-type-list'
    ),
    url(
        regex=r'^meals/$',
        view=MealListApi.as_view(),
        name='meal-list'
    ),
    url(
        regex=r'^booking-request/$',
        view=BookingRequestApi.as_view(),
        name='booking-request'
    ),
    url(
        regex=r'^email-exist/$',
        view=EmailExistApi.as_view(),
        name='email-exist'
    ),
    url(
        regex=r'^booking-requests/$',
        view=BookingRequestsApi.as_view(),
        name='booking-requests'
    ),
    url(
        regex=r'^check-phone/$',
        view=CheckPhoneApi.as_view(),
        name='check-phone'
    ),
]
