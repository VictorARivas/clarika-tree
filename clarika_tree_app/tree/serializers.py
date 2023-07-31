from rest_framework import serializers
from .models import Tree, SubTree

class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = '__all__'

class SubTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTree
        fields = '__all__'