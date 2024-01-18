from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rooms.models import Amenity, Room
from rooms.serializers import AmenitySerializer, RoomSerializer
# Create your views here.


class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializers = AmenitySerializer(data = request.data)
        if serializers.is_valid():
            amenity = serializers.save()
            return Response(
                AmenitySerializer(amenity).data,
            )
        else:
            return Response(serializers.errors)

class AmenityDetail(APIView):

    def get_object(self, pk):
        # 데이터를 가져오는 함수
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk): # url에 Pk 변수를 사용하므로 파라미터로 넣어야함.
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(serializer.errors)            
    
    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomSerializer(all_rooms, many=True)
        return Response(serializer.data)