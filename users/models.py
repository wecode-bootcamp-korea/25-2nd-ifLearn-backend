from django.db      import models
from core.models    import TimeStampModel

class User(TimeStampModel) :
    nickname     = models.CharField(max_length = 100)
    password     = models.CharField(max_length = 200)
    email        = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length = 13)
    introduce    = models.TextField(default = '')
    blog         = models.CharField(max_length = 100, default = '')
    sharer       = models.BooleanField(default = False)
    kakao_id     = models.CharField(max_length = 100)

    class Meta :
        db_table = "users"