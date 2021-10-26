from django.urls    import path
from courses.views  import VideoPlayer

urlpatterns = [
    path('/<path>', VideoPlayer.as_view())
]