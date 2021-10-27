from django.urls   import path, include

urlpatterns = [
    path('courses',include('courses.urls')), #의논 해야함
    path('users', include('users.urls'))
]
