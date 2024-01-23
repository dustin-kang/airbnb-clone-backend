from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from rooms.models import Amenity, Room
from categories.models import Category
from rooms.serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer

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
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if request.user.is_authenticated: # 사용자가 맞는지 인증
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category") # 해당 카테고리 ID(int)를 불러온다.
                if not category_pk: # 카테고리 ID를 입력하지 않았을 때
                    raise ParseError # ParseError : 잘못된 데이터를 입력했을 경우(400)
                try:
                    category = Category.objects.get(pk=category_pk) # 카테고리 아이디를 통해 해당 카테고리로 가져온다.
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES: # 해당 카테고리가 존재하지 않는 카테고리면 오류 발생
                        raise ParseError
                except Category.DoesNotExist:
                    raise ParseError
                room = serializer.save(owner=request.user, category=category) # owner에 유저 정보를 담음
                serializer = RoomDetailSerializer(room)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else: # 사용자가 아닌경우
            raise NotAuthenticated

class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)