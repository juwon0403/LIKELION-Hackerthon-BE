from rest_framework import serializers
from .models import *
from django.conf import settings


    
class AppSerializer(serializers.ModelSerializer):
    levelvalue = serializers.SerializerMethodField()
    levelcomment = serializers.SerializerMethodField()
    field=serializers.StringRelatedField(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = AppInfo
        fields = '__all__'
        
    def get_image(self, obj):
        # 기존의 이미지 URL을 가져옵니다.
        image_url = obj.image.url

        # 현재 요청의 전체 URL을 가져옵니다.
        request = self.context.get('request')
        if request is not None:
            full_image_url = request.build_absolute_uri(image_url)
        else:
            # request가 없는 경우에는 기존의 URL을 그대로 반환합니다.
            full_image_url = image_url

        return full_image_url

    def get_levelvalue(self, obj):
        return obj.level.level_value
    
    def get_levelcomment(self, obj):
        return obj.level.level_comment
    
    