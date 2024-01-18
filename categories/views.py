from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer

# Create your views here.

@api_view(["GET", "POST"])
def categories(request):

    if request.method == "GET":
        all_categories = Category.objects.all()
        serializers = CategorySerializer(all_categories, many=True)
        return Response(serializers.data)
    elif request.method == "POST":
        # Category.objects.create()에 request 받은 정보를 담을 수 있으나 검증을 하지 않은채 응답받음.
        serializers = CategorySerializer(data=request.data)
        if serializers.is_valid():
            new_category = serializers.save() # save 메서드를 실행하면 자동으로 create 메서드가 실행됨.
            return Response(
                CategorySerializer(new_category).data,
            )
        else:
            return Response(serializers.errors)

@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound
    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)
    elif request.mehtod == "DELETE":
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


