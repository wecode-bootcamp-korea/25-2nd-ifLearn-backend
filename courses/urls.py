from django.urls    import path
from courses.views  import CourseView, CategoryView, VideoPlayer, VideoLayoutView

urlpatterns = [
    path('/', CourseView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/<path>', VideoPlayer.as_view()),
    path('/video/<int:course_id>', VideoLayoutView.as_view())
]