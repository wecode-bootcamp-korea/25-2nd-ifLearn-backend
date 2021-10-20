from django.db      import models

from core.models    import TimeStampModel

class User(TimeStampModel) :
    nickname     = models.CharField(max_length = 100)
    password     = models.CharField(max_length = 200)
    email        = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length = 13, null=True)
    introduce    = models.TextField(default = '', null=True)
    blog         = models.CharField(max_length = 100, default = '', null=True)
    sharer       = models.BooleanField(default = False)
    kakao_id     = models.CharField(max_length = 100)

    class Meta :
        db_table = "users"