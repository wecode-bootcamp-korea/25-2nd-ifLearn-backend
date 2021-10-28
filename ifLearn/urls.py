from django.urls   import path, include

urlpatterns = [
    path('courses',include('courses.urls')),
    path('users', include('users.urls'))
]
