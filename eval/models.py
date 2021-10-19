from django.db      import models
from django.db.models.deletion import CASCADE
from core.models    import TimeStampModel

# Create your models here.
class Like(models.Model) :
    user    = models.ForeignKey('users.User', on_delete=CASCADE, related_name='like_by_user')
    course  = models.ForeignKey('courses.Course', on_delete=CASCADE, related_name='like_by_course')

    class Meta :
        db_table = 'likes'


class Review(TimeStampModel) :
    user    = models.ForeignKey('users.User', on_delete=CASCADE, related_name='review_by_user')
    course  = models.ForeignKey('courses.Course', on_delete=CASCADE, related_name='review_by_course')
    stars   = models.IntegerField(default=5)

    class Meta :
        db_table = 'reviews'


class Question(TimeStampModel) :
    user    = models.ForeignKey('users.User', on_delete=CASCADE, related_name='question_by_user')
    course  = models.ForeignKey('courses.Course', on_delete=CASCADE, related_name='question_by_course')
    title   = models.CharField(max_length=50)
    content = models.TextField(default=None)

    class Meta :
        db_table = 'questions'


class Answer(TimeStampModel) :
    user    = models.ForeignKey('users.User', on_delete=CASCADE, related_name='answer_by_user')
    question= models.ForeignKey('Question', on_delete=CASCADE, related_name='answer_by_question')

    class Meta :
        db_table = 'answers'