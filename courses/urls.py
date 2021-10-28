from django.urls    import path
from courses.views  import VideoPlayer, CategoryListView, VideoLayoutView, LectureDetail

urlpatterns = [
    path('/categories', CategoryListView.as_view()),
    path('/video/<int:course_id>', VideoLayoutView.as_view()),
    path('/video/detail/<int:lecture_id>', LectureDetail.as_view()),
    path('/<path>', VideoPlayer.as_view())
]
