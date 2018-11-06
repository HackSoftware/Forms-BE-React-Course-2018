from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from rest_framework import status
from rest_framework.response import Response

from booking.models import RoomType, Meal, User, BookingRequest


class RoomTypeListApi(ListAPIView):
    queryset = RoomType.objects.all()


class BookingRequestApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        email = serializers.CharField()
        phone = serializers.CharField()

        start = serializers.DateField(format='%Y-%m-%d')
        end = serializers.DateField(format='%Y-%m-%d')

        room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())
        meal = serializers.PrimaryKeyRelatedField(queryset=Meal.objects.all())
        number_of_people = serializers.IntegerField()

        notes = serializers.CharField()

    serializer_class = InputSerializer

    class OutputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(source='user.name')
        phone = serializers.CharField(source='user.phone')
        email = serializers.CharField(source='user.email')
        meal = serializers.CharField(source='meal.name')
        room_type = serializers.CharField(source='room_type.name')

        class Meta:
            model = BookingRequest
            fields = (
                'name',
                'email',
                'phone',
                'created_at',
                'meal',
                'room_type',
                'number_of_people',
                'notes'
            )

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = User.objects.create(email=data['email'], name=data['name'], phone=data['phone'])

        booking_request = BookingRequest.objects.create(
            user=user,
            **data
        )

        return Response(status=status.HTTP_200_OK, data=self.OutputSerializer(booking_request).data)