from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        depth = 1 # 자동으로 관계를 확장해주기 위해 depth 설정 (데이터 양 주의)


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"