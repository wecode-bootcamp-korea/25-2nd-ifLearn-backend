from django.db      import models
from core.models    import TimeStampModel

class Carousel(TimeStampModel) :
    tags        = models.CharField(max_length = 20)
    image_url   = models.TextField(default = None)
    url_to      = models.TextField(default = None)

    class Meta:
        db_table = 'carousels'

    def __str__(self):
        return self.tags