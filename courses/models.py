from django.db import models
from core.models import TimeStampModel 

class Category(TimeStampModel):
    name = models.CharField(max_length = 20)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

class SubCategory(TimeStampModel):
    name     = models.CharField(max_length = 20)
    category = models.ForeignKey('Category', on_delete = models.CASCADE, related_name = 'sub_categories')

    class Meta:
        db_table = 'sub_categories'

    def __str__(self):
        return self.name

class Course(TimeStampModel):
    name                  = models.CharField(max_length = 100)
    summary               = models.TextField()
    detail                = models.TextField()
    thumbnail_url         = models.TextField()
    visible               = models.IntegerField()
    price                 = models.DecimalField(max_digits = 10, decimal_places = 2)
    learning_period_month = models.IntegerField()
    level                 = models.ForeignKey('Level', on_delete       = models.CASCADE, related_name = 'courses_by_level')
    subcategory           = models.ForeignKey('SubCategory', on_delete = models.CASCADE, related_name = 'courses_by_subcategory')
    sharer                = models.ForeignKey('users.User', on_delete   = models.CASCADE, related_name = 'courses_by_user')

class Section(TimeStampModel):
    name       = models.CharField(max_length = 100)
    priority   = models.IntegerField()
    course     = models.ForeignKey('Course', on_delete = models.CASCADE, related_name = 'sections')

    class Meta:
        db_table = 'sections'

    def __str__(self):
        return self.name

class Lecture(TimeStampModel):
    name         = models.CharField(max_length = 100)
    storage_key  = models.CharField(max_length = 200) 
    storage_path = models.CharField(max_length = 200) 
    priority     = models.IntegerField() 
    play_time    = models.IntegerField() 
    section      = models.ForeignKey('Section', on_delete = models.CASCADE, related_name = 'lecture') 

    class Meta:
        db_table = 'lectures'

    def __str__(self):
        return self.name

class LectureCompletion(TimeStampModel):
    user    = models.ForeignKey('users.User', on_delete = models.CASCADE, related_name = 'lecture_completion_by_user')
    lecture = models.ForeignKey('Lecture', on_delete    = models.CASCADE, related_name   = 'lecture_completion_by_lecture')
    
    class Meta:
        db_table = 'lecture_completions'

class CourseInfo(TimeStampModel):
    name      = models.CharField(max_length = 20)
    info_type = models.ForeignKey('InfoType', on_delete = models.CASCADE, related_name = 'course_info_by_type')
    course    = models.ForeignKey('Course', on_delete   = models.CASCADE, related_name = 'course_info_by_course')

    class Meta:
        db_table = 'course_info'

    def __str__(self):
        self.name

class InfoType(TimeStampModel):
    name = models.CharField(max_length = 20)

    class Meta:
        db_table = 'info_types'

    def __str__(self):
        self.name

class CourseHashtag(TimeStampModel):
    hashtag = models.ForeignKey('Hashtag', on_delete = models.CASCADE, related_name = 'coursehashtag_by_hashtag')
    course  = models.ForeignKey('Course', on_delete  = models.CASCADE, related_name = 'coursehashtag_by_course')

    class Meta:
        db_table = 'coursehashtags'

class Hashtag(TimeStampModel):
    name = models.CharField(max_length = 20)
    
    class Meta:
        db_table = 'hashtags'

    def __str__(self):
        return self.name

class Level(TimeStampModel):
    name = models.CharField(max_length = 20)
    
    class Meta():
        db_table = 'levels'

    def __str__(self):
        return self.name
