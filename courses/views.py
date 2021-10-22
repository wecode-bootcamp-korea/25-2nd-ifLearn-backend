from django.http    import JsonResponse
from django.views   import View 
from courses.models import Category, Course,SubCategory, CourseHashtag

class CategoryView(View) :
    def get(self,request) :
        subcategory_queryset= SubCategory.objects.values('id','name','category_id')
        category_queryset   = Category.objects.values('name', 'id')
        hashtag_queryset    = CourseHashtag.objects.select_related('hashtag','course').values('course__subcategory_id','hashtag__name','hashtag__id')
        result              = []

        for category in category_queryset :
            result.append({
            category["name"] : [{
                "id" : sub["id"],
                "subcategory" : sub["name"],
                "hashtag" : [mid["hashtag__name"] for mid in hashtag_queryset if mid["course__subcategory_id"] == sub["id"]][:12]
                }
            for sub in subcategory_queryset if sub["category_id"] == category["id"]]
            })

        return JsonResponse({"reuslt" : result})

class CourseView(View) :
    def get(self,request) :
        
        course_queryset = Course.objects.select_related('level','subcategory', 'subcategory__category', 'sharer'
        ).values('id','name','summary','thumbnail_url','price','level__name', 'subcategory__name', 'subcategory__category__name', 'sharer__nickname')
        
        hashtag_queryset    = CourseHashtag.objects.select_related('hashtag','course').values('course__id','hashtag__name','hashtag__id')


        result          = []

        for course in course_queryset :
            result.append(
            {
                "id" : course["id"],
                "thumbnail" : course["thumbnail_url"],
                "title" : course["name"],
                "author" : course["sharer__nickname"],
                "price" : int(course["price"]),
                "summary" : course["summary"],
                "level" : course["level__name"],
                "sub-cateogry" : course["subcategory__name"],
                "category" : course["subcategory__category__name"],
                "star-number" : 0,
                "popular" : 0,
                "hash-tag" : [
                    {"tag_name": tag["hashtag__name"],
                    "tag_id" : tag["hashtag__id"]
                    } for tag in hashtag_queryset if tag["course__id"] == course["id"]
                ]
            })

        return JsonResponse({
            "result" : result
        })