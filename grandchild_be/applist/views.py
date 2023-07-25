from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db.models import F
import random


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
        # 어플들을 레벨의 내림차순으로 정렬
        applist = list(AppInfo.objects.all().order_by('level__level_value', 'id'))

        # 레벨이 같은 어플들을 랜덤하게 섞음
        grouped_applist = []
        current_group = []
        prev_level = None

        for app in applist:
            if prev_level is None or app.level.level_value == prev_level:
                current_group.append(app)
            else:
                random.shuffle(current_group)
                grouped_applist.extend(current_group)
                current_group = [app]
            prev_level = app.level.level_value

        if current_group:
            random.shuffle(current_group)
            grouped_applist.extend(current_group)

        # 상위 4개의 어플만 선택
        applist = grouped_applist[:4]

        appserializer = AppSerializer(applist, many=True)
        return Response(appserializer.data, status=status.HTTP_200_OK)


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