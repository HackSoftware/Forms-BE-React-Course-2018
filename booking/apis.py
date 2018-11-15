from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from booking.models import RoomType, Meal, User, BookingRequest, Room


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
        room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), required=False, allow_null=True)
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

        user = User.objects.create(email=data['email'], name=data['name'], phone=data['phone'])

        room = data.get('room')
        if room and not room.available:
            raise ValidationError('This room is not available')

        booking_request = BookingRequest.objects.create(
            user=user,
            start=data['start'],
            end=data['end'],
            room_type=data['room_type'],
            meal=data.get('meal'),
            number_of_people=data['number_of_people'],
            notes=data['notes'],
            room=room
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


class BookingRequestsApi(ListAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(source='user.name')
        email = serializers.CharField(source='user.email')
        phone = serializers.CharField(source='user.phone')

        class Meta:
            model = BookingRequest
            fields = (
                'id',
                'name',
                'email',
                'phone',
                'start',
                'end'
            )

    serializer_class = OutputSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)

        if name is not None:
            return BookingRequest.objects.filter(user__name__icontains=name.encode())

        if start is not None and end is not None:
            return BookingRequest.objects.filter(start=start, end=end)

        return BookingRequest.objects.all()


class CheckPhoneApi(APIView):
    class InputSerializer(serializers.Serializer):
        phone = serializers.CharField(required=False, allow_blank=True)

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        email_exist = User.objects.filter(phone=data['phone']).exists()

        if email_exist:
            raise ValidationError('This phone is alreay taken')

        return Response(status=status.HTTP_200_OK)


class GetAvailableRoomsApi(APIView):
    class InputSerializer(serializers.Serializer):
        room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())

    class OutputSerializer(serializers.ModelSerializer):
        room_type = serializers.CharField(source='room_type.name')
        name = serializers.CharField(source='number')

        class Meta:
            model = Room
            fields = (
                'id',
                'name',
                'room_type',
                'available'
            )

    def get(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data={
            'room_type': self.kwargs.get('room_type')
        })
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        rooms = Room.objects.filter(room_type=data['room_type'], available=True)

        return Response(status=status.HTTP_200_OK, data=self.OutputSerializer(rooms, many=True).data)


class EmailExistPerNameApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False, allow_blank=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = (
                'id',
                'name',
                'email',
            )

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        users = User.objects.filter(name=data['name'])

        return Response(status=status.HTTP_200_OK, data=self.OutputSerializer(users, many=True).data)
