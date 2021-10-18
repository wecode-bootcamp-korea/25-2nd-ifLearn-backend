from django.db      import models
from core.models    import TimeStampModel

# Create your models here.
class User(TimeStampModel) :
    nickname = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    email    = models.CharField(max_length=100)
    phone_num= models.CharField(max_length=13)
    introduce= models.TextField(null=True)
    blog     = models.CharField(max_length=100, null=True)
    sharer   = models.BooleanField(default=False)

    class Meta :
        db_table = "users"