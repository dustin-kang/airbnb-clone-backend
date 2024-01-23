from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer

class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['name', 'description',]

class RoomDetailSerializer(ModelSerializer):
    
    # foreign Key, ManytoMany : depth로 모든 필드를 가져오는 것보다 효율적이다.
    owner = TinyUserSerializer()
    amenities = AmenitySerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Room
        fields = "__all__"

class RoomListSerializer(ModelSerializer):
        class Meta:
            model = Room
            fields = ["pk", "name", "country", "city", "price"]