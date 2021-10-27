from django.urls    import path
from courses.views  import VideoPlayer, CategoryListView

urlpatterns = [
    path('/categories', CategoryListView.as_view()),
    path('/<path>', VideoPlayer.as_view()), #이것도 의논해야함
    ]
