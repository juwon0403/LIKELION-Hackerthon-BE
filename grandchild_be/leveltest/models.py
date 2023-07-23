from django.db import models


    
class Test(models.Model):
    #question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    count = models.IntegerField(default=0) # answer의 True 수 체크
    result = models.CharField(max_length=10, null=True, blank=True) # 회원등급

    def __str__(self):
        return f"총 {self.count}점"
    
    def get_count(self):
        return self.count
    

    def get_result(self):
        if self.count == 0:
            self.result= "씨앗"
        elif self.count == 1:
            self.result= "새싹"
        elif self.count == 2:
            self.result= "꽃"
        elif self.count in (3, 4):
            self.result= "열매"
        elif self.count == 5:
            self.result= "나무"
            
        return self.result
    
    class Meta:
        verbose_name_plural = "Test"