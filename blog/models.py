from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    title2 = models.CharField(max_length=200)

    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
            
    fixed_date = models.DateTimeField(
            blank=True, null=True)
    compleat_date = models.DateTimeField(
            blank=True, null=True)

    must_worker = models.ManyToManyField("SyainTable", related_name="must")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

#社員テーブル
class SyainTable(models.Model):
    SyainNo = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):#このﾒｿｯﾄﾞで管理画面等で表示するものを決めてます
        return self.name
        
#個人登録テーブル
class KojinTourokuTable(models.Model):
    id = models.IntegerField(primary_key=True)
    KojinTourokuNo = models.IntegerField(default=1)
    SyainNo = models.IntegerField(default=1)
