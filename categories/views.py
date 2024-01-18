from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer

# Create your views here.

class Categories(APIView):
    
    def get(self, request):
        all_categories = Category.objects.all()
        serializers = CategorySerializer(all_categories, many=True)
        return Response(serializers.data)
    
    def post(self, request):
        # Category.objects.create()에 request 받은 정보를 담을 수 있으나 검증을 하지 않은채 응답받음.
        serializers = CategorySerializer(data=request.data)
        if serializers.is_valid():
            new_category = serializers.save() # save 메서드를 실행하면 자동으로 create 메서드가 실행됨.
            return Response(
                CategorySerializer(new_category).data,
            )
        else:
            return Response(serializers.errors)


class CategoryDetail(APIView): # Category 모델과 혼동 방지를 위해 변경
    
    def get_object(self, pk):
        """
        해당 데이터가 있는지 없는지 확인해서 쿼리셋 반환
        """
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound  
        return category      

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)
    
    def put(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        


