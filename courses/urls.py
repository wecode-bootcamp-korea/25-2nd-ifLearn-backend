from django.urls    import path
from courses.views  import CourseView, CategoryView, VideoPlayer

urlpatterns = [
    path('/', CourseView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/<path>', VideoPlayer.as_view())
]