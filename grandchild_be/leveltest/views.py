from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Test
from .serializers import TestSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class TestAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties={
                'q1': openapi.Schema(type=openapi.TYPE_STRING, description="첫번째 질문"),
                'q2': openapi.Schema(type=openapi.TYPE_STRING, description="두번째 질문"),
                'q3': openapi.Schema(type=openapi.TYPE_STRING, description="세번째 질문"),
                'q4': openapi.Schema(type=openapi.TYPE_STRING, description="네번째 질문"),
                'q5': openapi.Schema(type=openapi.TYPE_STRING, description="다섯번째 질문"),
            }
        ),
            responses = {
                200: openapi.Response('q1~q5의 O/X 개수에 따른 등급', TestSerializer)
            }
        )
    
    def post(self, request, format=None):
        # 폼에서 전송된 데이터를 받아옵니다.
        q1_answer = request.data.get('q1')
        q2_answer = request.data.get('q2')
        q3_answer = request.data.get('q3')
        q4_answer = request.data.get('q4')
        q5_answer = request.data.get('q5')

        # 각 질문에 대한 답변을 처리합니다. (O, X를 True, False로 변환하거나 다른 방법으로 처리 가능)
        q1_answer_bool = True if q1_answer == 'O' else False
        q2_answer_bool = True if q2_answer == 'O' else False
        q3_answer_bool = True if q3_answer == 'O' else False
        q4_answer_bool = True if q4_answer == 'O' else False
        q5_answer_bool = True if q5_answer == 'O' else False

        # test 모델의 count 필드에 숫자 할당
        count = 0
        if q1_answer_bool:
            count += 1
        if q2_answer_bool:
            count += 1
        if q3_answer_bool:
            count += 1
        if q4_answer_bool:
            count += 1
        if q5_answer_bool:
            count += 1

        # test 모델에 저장
        test_instance = Test.objects.create(count=count) #모델 생성
        result = test_instance.get_result() #결과값 임시변수에 할당
        test_instance.result=result #등급명 모델에 저장
        test_instance.save() #저장
        serializer=TestSerializer(test_instance)
        
        # API 응답으로 test 모델의 count 값을 반환
        return Response(serializer.data, status=status.HTTP_201_CREATED)
