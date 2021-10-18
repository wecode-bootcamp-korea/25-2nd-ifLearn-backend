from django.db      import models
from core.models    import TimeStampModel

# Create your models here.
class Course(TimeStampModel) :
    name = models.CharField(max_length=100)

    class Meta : 
        db_table = "courses"