from django.db import models


# 어플 난이도
class AppLevel(models.Model):
    level_value = models.IntegerField(default=0) # 별 개수, 회원등급과 관련
    level_comment = models.CharField(max_length=20) # 별 개수에 따른 코멘트

    def __str__(self):
        return f"Level {self.level_value} : {self.level_comment}"
    
    class Meta:
        verbose_name_plural = "AppLevel"

# 어플 정보
class AppInfo(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/')
    level = models.ForeignKey(AppLevel, on_delete=models.CASCADE, related_name='levels')
    summary = models.CharField(max_length=200)
    detail = models.TextField()
    link = models.TextField()
    is_downloaded = models.BooleanField() # True일 경우, 추천페이지에서 제외
    field = models.CharField(max_length=20) # 추천페이지에서 사용

    def __str__(self):
        return f"{self.name} : Level {self.level.level_value}"
    
    class Meta:
        verbose_name_plural = "AppInfo"