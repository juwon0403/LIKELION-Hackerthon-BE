# celery.py

'''import os
from celery import Celery

CELERY_MAIN = 'grandchild_be'  # Django 프로젝트의 모듈 경로를 입력해야 합니다.

app = Celery(CELERY_MAIN)

# settings.py의 CELERY 설정을 이용하여 Celery 앱 설정
app.config_from_object('django.conf:settings', namespace='CELERY')

# tasks.py 모듈을 찾아서 자동으로 등록
app.autodiscover_tasks()

from applist import tasks
app.register_task(tasks.create_tts_file)'''

# grandchild_be/celery.py

import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandchild_be.settings')
app = Celery('grandchild_be')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# 직접 작업들을 import하여 등록
#from applist.tasks import create_tts_file
#app.register_task(create_tts_file)
# 다른 작업도 있다면 이와 같이 등록하세요.

#if __name__ == '__main__':
#    app.start()
