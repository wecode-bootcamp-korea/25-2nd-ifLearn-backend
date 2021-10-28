from django.urls    import path

from courses.views  import VideoPlayer, CategoryListView, VideoLayoutView, LectureDetail, CourseView, CourseListView

urlpatterns = [
    path('/categories', CategoryListView.as_view()),
    path('/video/<int:course_id>', VideoLayoutView.as_view()),
    path('/video/detail/<int:lecture_id>', LectureDetail.as_view()),
    path(
        '/all', 
        CourseListView.as_view(),
        name = 'all'
    ),
    path(
        '/<int:category_id>', 
        CourseListView.as_view(),
        name = 'category'
    ),
    path(
        '/<int:category_id>/<int:sub_category_id>', 
        CourseListView.as_view(),
        name = 'sub_category'
    ),
    path('/course/<int:course_id>', CourseView.as_view()),
    path('/<path>', VideoPlayer.as_view()),
]

