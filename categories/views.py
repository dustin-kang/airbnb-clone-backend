from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
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

@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)


