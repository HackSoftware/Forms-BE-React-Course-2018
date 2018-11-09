from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from booking.models import RoomType, Meal, User, BookingRequest


class RoomTypeListApi(ListAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = RoomType
            fields = (
                'name',
                'id'
            )

    serializer_class = OutputSerializer
    queryset = RoomType.objects.all()


class MealListApi(ListAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Meal
            fields = (
                'name',
                'id'
            )

    serializer_class = OutputSerializer
    queryset = Meal.objects.all()


class BookingRequestApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        email = serializers.CharField()
        phone = serializers.CharField(required=False, allow_null=True)

        start = serializers.DateField(format='%Y-%m-%d')
        end = serializers.DateField(format='%Y-%m-%d')

        room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())
        meal = serializers.PrimaryKeyRelatedField(queryset=Meal.objects.all(), required=False, allow_null=True)
        number_of_people = serializers.IntegerField(required=False, allow_null=True)

        notes = serializers.CharField(required=False, allow_null=True)

    serializer_class = InputSerializer

    class OutputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(source='user.name')
        phone = serializers.CharField(source='user.phone')
        email = serializers.CharField(source='user.email')
        meal = serializers.CharField(source='meal.name', required=False)
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
        serializer = self.InputSerializer(data={
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone'),
            'start': request.data.get('start'),
            'end': request.data.get('end'),
            'room_type': request.data.get('roomType'),
            'meal': request.data.get('meal'),
            'number_of_people': request.data.get('numberOfPeople'),
            'notes': request.data.get('notes'),
        })
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user_exists = User.objects.filter(email=data['email'])
        if user_exists:
            raise ValidationError('A user with such email already exists')
        user = User.objects.create(email=data['email'], name=data['name'], phone=data['phone'])

        booking_request = BookingRequest.objects.create(
            user=user,
            start=data['start'],
            end=data['end'],
            room_type=data['room_type'],
            meal=data.get('meal'),
            number_of_people=data['number_of_people'],
            notes=data['notes']
        )

        return Response(status=status.HTTP_200_OK, data=self.OutputSerializer(booking_request).data)


class EmailExistApi(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.CharField()

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

        email_exist = User.objects.filter(email=data['email']).exists()

        message = 'Email free'
        if email_exist:
            message = 'A user with such email already exists'

        return Response(status=status.HTTP_200_OK, data={'message': message})
