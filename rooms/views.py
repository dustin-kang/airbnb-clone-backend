from django.db import transaction # https://docs.djangoproject.com/en/4.1/topics/db/transactions/
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
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
                    raise ParseError("Category is required") # ParseError : 잘못된 데이터를 입력했을 경우(400)
                try:
                    category = Category.objects.get(pk=category_pk) # 카테고리 아이디를 통해 해당 카테고리로 가져온다.
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES: # 해당 카테고리가 존재하지 않는 카테고리면 오류 발생
                        raise ParseError("The Category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
                try:
                    with transaction.atomic(): # Transaction : 모든 코드가 성공하거나 그렇지 않으면(하나라도 실패) 원래 상태로 되돌아가게 된다.
                        room = serializer.save(owner=request.user, category=category)
                        amenities = request.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found") # transaction 에러가 발생할 경우
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
    
    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied

        serializer = RoomDetailSerializer(room, request.data, partial=True)

        if serializer.is_valid():
            with transaction.atomic():
                category_pk = request.data.get("category")
                amenities_pk = request.data.get("amenities")

                if category_pk:
                    try:
                        category = Category.objects.get(pk=category_pk)
                    except Exception:
                        raise ParseError("Category not found")
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES: # 카테고리가 experiences 카테고리일경우,
                        raise ParseError("The Category kind should be 'rooms'")
                else:
                    category = room.category

  
                if amenities_pk:
                    amenities = []
                    for amenity_pk in amenities_pk:
                        try:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            amenities.append(amenity)
                        except Exception:
                            raise ParseError("Amenitiy not found")
                else:
                    amenities = room.amenities.all()       

                updated_room = serializer.save(
                    owner=request.user,
                    category=category,
                    amenities=amenities,
                )
                return Response(RoomDetailSerializer(updated_room).data)
        else:
            return Response(serializer.errors)       
                    

        
    
    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated # 로그인이 되어 있는지 확인
        if room.owner != request.user:
            raise PermissionDenied # 작성자가 맞는지 확인
        room.delete 
        return Response(status=status.HTTP_204_NO_CONTENT)