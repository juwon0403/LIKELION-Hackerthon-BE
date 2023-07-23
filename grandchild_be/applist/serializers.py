from rest_framework import serializers
from .models import *


class AppSerializer(serializers.ModelSerializer):
    levelvalue = serializers.SerializerMethodField()
    levelcomment = serializers.SerializerMethodField()

    class Meta:
        model = AppInfo
        fields = '__all__'

    def get_levelvalue(self, obj):
        return obj.level.level_value
    
    def get_levelcomment(self, obj):
        return obj.level.level_comment
