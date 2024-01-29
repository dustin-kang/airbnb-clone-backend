from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer

class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['name', 'description',]

class RoomDetailSerializer(ModelSerializer):
    
    # foreign Key{}, ManytoMany[{}] : depth로 모든 필드를 가져오는 것보다 효율적이다.
    owner = TinyUserSerializer(read_only=True) # 사용자에게 owner 입력에 대한 권한을 주면 안됨. -> read_only=True
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room): # get_계산하려는 속성
         return room.rating()
    
    def get_is_owner(self, room): # get_계산하려는 속성
        request = self.context['request']
        return room.owner == request.user # True or False

class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ["pk", "name", "country", "city", "price", "rating","is_owner",]

    def get_rating(self, room):
        return room.rating()
    
    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user # True or False