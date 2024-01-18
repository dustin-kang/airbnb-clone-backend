from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.Serializer):

    pk = serializers.IntegerField()
    name = serializers.CharField(required=True)
    kind = serializers.ChoiceField(choices=Category.CategoryKindChoices.choices,) # ChoiceField
    created_at = serializers.DateTimeField()

    def create(self, validated_data):
        return Category.objects.create(**validated_data) ## **는 딕셔너리를 가져오게 된다.