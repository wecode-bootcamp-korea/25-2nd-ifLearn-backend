from django.urls    import path
from courses.views  import CourseView

urlpatterns = [
    path('/', CourseView.as_view()),
]