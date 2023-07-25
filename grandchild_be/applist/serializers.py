from rest_framework import serializers
from .models import *


    
class AppSerializer(serializers.ModelSerializer):
    levelvalue = serializers.SerializerMethodField()
    levelcomment = serializers.SerializerMethodField()
    field=serializers.StringRelatedField(many=True)
    

    class Meta:
        model = AppInfo
        fields = '__all__'
        
    #def get_field(self,obj):
     #   return obj.field.name


    def get_levelvalue(self, obj):
        return obj.level.level_value
    
    def get_levelcomment(self, obj):
        return obj.level.level_comment
    
    