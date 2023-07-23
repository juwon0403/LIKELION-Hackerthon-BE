from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# 카테고리 페이지
class AppListAPI(APIView):
    @swagger_auto_schema(
            responses = {
                200: openapi.Response('모든 어플 조회 완료', AppSerializer)
            }
        )
    
    def get(self, request):
        top_app = AppInfo.objects.all().order_by('?')
        level_0 = AppInfo.objects.filter(level__level_value=0)
        level_1 = AppInfo.objects.filter(level__level_value=1)
        level_2 = AppInfo.objects.filter(level__level_value=2)
        level_3_4 = AppInfo.objects.filter(level__level_value__in=[3, 4])
        level_5 = AppInfo.objects.filter(level__level_value=5)

        data = {
            "top_app": AppSerializer(top_app, many=True).data,
            "level_0": AppSerializer(level_0, many=True).data,
            "level_1": AppSerializer(level_1, many=True).data,
            "level_2": AppSerializer(level_2, many=True).data,
            "level_3_4": AppSerializer(level_3_4, many=True).data,
            "level_5": AppSerializer(level_5, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)


# 추천페이지 - 어플 4개
class AppRecommendAPI(APIView):
    @swagger_auto_schema(
            responses = {
                200: openapi.Response('어플 추천 완료', AppSerializer)
            }
        )
    
    def get(self, request):
        # level_value가 적은 순서대로 AppInfo 모델 데이터를 가져옴
        app_info_queryset = AppInfo.objects.all().order_by('level__level_value')

        # level_value가 같은 데이터들의 ID를 랜덤으로 섞어서 리스트로 변환
        random_level_value_ids = (
            app_info_queryset
            .order_by('?')  # 랜덤 순서
            .values_list('id', flat=True)
        )

        # 추천할 데이터의 ID 리스트
        recommended_ids = random_level_value_ids[:4]

        # 추천할 데이터들을 ID 리스트를 기준으로 조회
        recommended_apps = AppInfo.objects.filter(id__in=recommended_ids)

        serializer = AppSerializer(recommended_apps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 어플 상세페이지
class AppDetailAPI(APIView):
    @swagger_auto_schema(
            responses = {
                200: openapi.Response('어플 상세페이지 조회 완료', AppSerializer)
            }
        )
    
    def get(self, request):
        app = AppInfo.objects.all()
        appserializer = AppSerializer(app, many=True)

        return Response(appserializer.data, status=status.HTTP_200_OK)