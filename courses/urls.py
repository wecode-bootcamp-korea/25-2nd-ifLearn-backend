from django.urls    import path
from courses.views  import CourseView, CategoryView

urlpatterns = [
    path('/', CourseView.as_view()),
    path('/category', CategoryView.as_view())
]