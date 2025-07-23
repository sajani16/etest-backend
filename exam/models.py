from django.db import models

# Create your models here.
class ExamResult(models.Model):
    details = models.JSONField()
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    topic = models.CharField(max_length=100 ,null=True, blank=True)
    exam_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total_questions} on {self.exam_date}"
    
    