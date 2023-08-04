from django.shortcuts import render,get_object_or_404,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from gtts import gTTS
from django.conf import settings
from django.urls import reverse
from django.http import FileResponse
from .tasks import create_tts_file
from django.views import View
#from celery.result import AsyncResult
import os
import time
import uuid

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import SuspiciousOperation

from django.db.models import F
import random


# 카테고리 페이지
class AppListAPI(APIView):
    @swagger_auto_schema(
            tags = ['카테고리 페이지 : 모든 어플 조회'],
            responses = {
                200: openapi.Response('모든 어플 조회 완료 : 추천어플(top_app)과 레벨별 어플(level_0, level_1, level_2, level_3_4, level_5) 구분하여 전송', AppSerializer)
            }
        )
    
    def get(self, request):
        top_app = AppInfo.objects.filter(is_downloaded=True).order_by('?')
        level_0 = AppInfo.objects.filter(level__level_value=0)
        level_1 = AppInfo.objects.filter(level__level_value=1)
        level_2 = AppInfo.objects.filter(level__level_value=2)
        level_3_4 = AppInfo.objects.filter(level__level_value__in=[3, 4])
        level_5 = AppInfo.objects.filter(level__level_value=5)

        data = {
            "top_app": AppSerializer(top_app, many=True, context={'request': request}).data,
            "level_0": AppSerializer(level_0, many=True, context={'request': request}).data,
            "level_1": AppSerializer(level_1, many=True, context={'request': request}).data,
            "level_2": AppSerializer(level_2, many=True, context={'request': request}).data,
            "level_3_4": AppSerializer(level_3_4, many=True, context={'request': request}).data,
            "level_5": AppSerializer(level_5, many=True, context={'request': request}).data,
        }

        return Response(data, status=status.HTTP_200_OK)

#카테고리 메인 페이지
class MainAppListAPI(APIView):
    @swagger_auto_schema(
            tags = ['메인 카테고리 페이지 : 레벨별 2개의 어플 조회'],
            responses = {
                200: openapi.Response('레벨별 2개의 어플 조회 완료 : 추천어플(top_app)과 레벨별 어플(level_0, level_1, level_2, level_3_4, level_5) 구분하여 전송', AppSerializer)
            }
        )
     
    def get(self, request):
        top_app = AppInfo.objects.filter(is_downloaded=True).order_by('?')[:2]
        level_0 = AppInfo.objects.filter(level__level_value=0).order_by('?')[:2]
        level_1 = AppInfo.objects.filter(level__level_value=1).order_by('?')[:2]
        level_2 = AppInfo.objects.filter(level__level_value=2).order_by('?')[:2]
        level_3_4 = AppInfo.objects.filter(level__level_value__in=[3, 4]).order_by('?')[:2]
        level_5 = AppInfo.objects.filter(level__level_value=5).order_by('?')[:2]

        data = {
            "top_app": AppSerializer(top_app, many=True, context={'request': request}).data,
            "level_0": AppSerializer(level_0, many=True, context={'request': request}).data,
            "level_1": AppSerializer(level_1, many=True, context={'request': request}).data,
            "level_2": AppSerializer(level_2, many=True, context={'request': request}).data,
            "level_3_4": AppSerializer(level_3_4, many=True, context={'request': request}).data,
            "level_5": AppSerializer(level_5, many=True, context={'request': request}).data,
        }

        return Response(data, status=status.HTTP_200_OK)


# 추천페이지 - 어플 4개
class AppRecommendAPI(APIView):
    @swagger_auto_schema(
        tags = ['추천 페이지 : 어플 4가지 추천'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties={
                'field': openapi.Schema(type=openapi.TYPE_STRING, description="추천페이지의 최하위 분류명")
            }
        ),
            responses = {
                200: openapi.Response('입력받은 field와 관련된 어플 4가지 정렬 : 레벨 오름차순 + 같은 레벨일경우 랜덤', AppSerializer)
            }
        )
    def post(self,request):
        category=request.data.get('field')
        # 어플들을 레벨 오름차순 + 같은 레벨일 경우 랜덤으로 정렬
        applist=AppInfo.objects.filter(field__name__icontains=category).order_by('level__level_value', '?')[:4]
        appserializer = AppSerializer(applist, many=True, context={'request': request})
        return Response(appserializer.data, status=status.HTTP_200_OK)

    #def get(self, request):
        # 어플들을 레벨 오름차순 + 같은 레벨일 경우 랜덤으로 정렬
     #   applist = AppInfo.objects.all().order_by('level__level_value', '?')[:4]
      #  appserializer = AppSerializer(applist, many=True)
       # return Response(appserializer.data, status=status.HTTP_200_OK)


def tts_file_view(filename):
    # 파일 경로 생성
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # 파일이 존재하는지 확인 후, 존재하면 False
    if os.path.exists(file_path):
        #with open(file_path, 'rb') as f:
            #response = FileResponse(f, content_type='audio/mpeg')
            return False
    else:
        # 파일이 존재하지 않을 경우 True
        return True
# 어플 상세페이지
class AppDetailAPI(APIView):
    @swagger_auto_schema(
         tags = ['상세 페이지 : 어플 상세조회'],
            responses = {
                200: openapi.Response('id에 따른 어플 상세페이지 조회 완료 app_info는 어플정보 아래 app은 app_info가 감싸고 있음, tts는 음성파일. ', AppSerializer)
            }
        )
    
    def get(self, request, pk):
        app = get_object_or_404(AppInfo, pk=pk)
        appserializer = AppSerializer(app, context={'request': request})
        
        speak = f":어플 이름: {app.name}. 레벨: {app.level.level_comment}. 요약: {app.summary}. 상세: {app.detail}."
        temp_filename = f'temp_tts_{pk}.mp3'
        try:
            #만약 파일이 없으면
            if tts_file_view(temp_filename):  
                # TTS 생성 작업 
                tts_url = create_tts_file(speak, pk)
            
            tts_ur = settings.MEDIA_URL + temp_filename
            ## 완전한 TTS 파일 URL 구하기
            tts_url2 = request.build_absolute_uri(tts_ur)

            
            return Response({"app_info": appserializer.data, "tts": tts_url2}, status=status.HTTP_200_OK)
        except SuspiciousOperation as e:
            # 예외 처리: TTS 작업이 제대로 실행되지 않았을 경우
            return Response({"app_info": appserializer.data, "tts": None}, status=status.HTTP_200_OK)
    
    '''def get(self, request, pk):
        app = get_object_or_404(AppInfo, pk=pk)
        appserializer = AppSerializer(app, context={'request': request})
        
        speak = f":어플 이름: {app.name}. 레벨: {app.level.level_comment}. 요약: {app.summary}. 상세: {app.detail}."

        try:
            # TTS 생성 작업을 Celery로 실행
            urur = create_tts_file.delay(speak, pk)
            task_id = urur.id
            
            # 작업 완료를 대기하기 위해 반복문 사용
            while not urur.ready():
                time.sleep(1)  # 1초 대기
            
            # 완전한 TTS 파일 URL 구하기
            tts_filename = f'temp_tts_{pk}.mp3'
            tts_full_url = request.build_absolute_uri(reverse('tts_file', kwargs={'filename': tts_filename}))
            # response에 TTS 파일 URL을 원하는 형식으로 반환
            return Response({"app_info": appserializer.data, "tts": tts_full_url}, status=status.HTTP_200_OK)
        except SuspiciousOperation as e:
            # 예외 처리: TTS 작업이 제대로 실행되지 않았을 경우
            return Response({"app_info": appserializer.data, "tts": None}, status=status.HTTP_200_OK)'''

   
        
    '''def get(self, request, pk):
        app = get_object_or_404(AppInfo, pk=pk)
        appserializer = AppSerializer(app, context={'request': request})
        
        speak = f":어플 이름: {app.name}. 레벨: {app.level.level_comment}. 요약: {app.summary}. 상세: {app.detail}."

        try:
            # TTS 생성 작업을 Celery로 실행
            urur = create_tts_file.delay(speak,pk)
            taskid = urur.id

            # 파일 이름에 고유한 식별자를 추가하여 TTS 파일 저장
            unique_filename = f"temp_tts_{uuid.uuid4().hex}.mp3"
            tts_file = os.path.join(settings.MEDIA_ROOT, unique_filename)

            # 완전한 TTS 파일 URL 구하기
            tts_url = request.build_absolute_uri(reverse('tts_file', kwargs={'task_id': taskid}))

            # response에 TTS 파일 URL은 넣지 않고, 바로 상세 정보만 응답합니다.
            return Response({"app_info": appserializer.data, "tts": tts_url}, status=status.HTTP_200_OK)
        except SuspiciousOperation as e:
            # 예외 처리: TTS 작업이 제대로 실행되지 않았을 경우
            return Response({"app_info": appserializer.data, "tts": None}, status=status.HTTP_200_OK)
'''

    '''def get(self, request, pk):
        app = get_object_or_404(AppInfo, pk=pk)
        appserializer = AppSerializer(app, context={'request': request})
        
        speak = f":어플 이름: {app.name}. 레벨: {app.level.level_comment}. 요약: {app.summary}. 상세: {app.detail}."

        try:
            # TTS 생성 작업을 Celery로 실행
            urur = create_tts_file.delay(speak,task_id=pk)
            taskid = urur.id
            
            # 완전한 TTS 파일 URL 구하기
            tts_url = request.build_absolute_uri(reverse('tts_file', kwargs={'task_id': taskid}))

            # response에 TTS 파일 URL은 넣지 않고, 바로 상세 정보만 응답합니다.
            return Response({"app_info": appserializer.data, "tts": tts_url}, status=status.HTTP_200_OK)
        except SuspiciousOperation as e:
            # 예외 처리: TTS 작업이 제대로 실행되지 않았을 경우
            return Response({"app_info": appserializer.data, "tts": None}, status=status.HTTP_200_OK)'''
 

    
    