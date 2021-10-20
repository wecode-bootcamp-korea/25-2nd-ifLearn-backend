from django.urls        import path
from carousels.views    import CarourselView

urlpatterns = [
    path('/', CarourselView.as_view())
]