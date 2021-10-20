from django.db      import models

from core.models    import TimeStampModel

class User(TimeStampModel) :
    nickname     = models.CharField(max_length = 100)
    email        = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length = 13, null = True)
    introduce    = models.TextField(null = True)
    blog         = models.CharField(max_length = 100, null = True)
    sharer       = models.BooleanField(default = False)
    kakao_id     = models.CharField(max_length = 100, null = True)

    class Meta :
        db_table = "users"