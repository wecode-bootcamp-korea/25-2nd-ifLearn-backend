import os
import re
import mimetypes
import jwt
from ifLearn.settings import SECRET_KEY, ALGORITHM

from wsgiref.util   import FileWrapper
from django.http    import JsonResponse, StreamingHttpResponse
from django.http.response import HttpResponse
from django.views   import View 
from courses.models import Category, Course, SubCategory, CourseHashtag, Lecture, LectureCompletion
from django.db      import connection
from users.models   import User

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
        ).values('id','name','summary','thumbnail_url','price','level__name', 'subcategory__name', 'subcategory__category__name', 'sharer__nickname')[:100]
        
        course_ids = [c["id"] for c in course_queryset]

        hashtag_queryset    = CourseHashtag.objects.select_related('hashtag','course').values('course__id','hashtag__name','hashtag__id').filter(course__id__in = course_ids)
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

class RangeFileWrapper:
    def __init__(self, file, blksize=8192, offset=0, length=None):
        self.file = file
        self.file.seek(offset, 0)
        self.remaining = length
        self.blksize = blksize

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.file.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.file.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


class VideoPlayer(View) :    
    def get_content_type(self,path) :
        content_type = mimetypes.guess_type(path)[0]
        content_type = content_type or 'application/octet-stream'
        
        return content_type


    def get_http_range(self,request) :
        range_header =request.META.get('HTTP_RANGE', '').strip()
        # 띄어쓰기를 엄격하게 하지 않기 위해 \s* 을 계속 붙
        range_match = re.match(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)',range_header, re.I)
        return range_match


    def get_range(self,size,range_match) :
        first_byte, last_byte = range_match.groups()
        first_byte  = int(first_byte) if first_byte else 0
        last_byte   = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        
        return first_byte, last_byte


    def get(self,request,path) :
        if not os.path.isfile(path) :
            return JsonResponse({"MEESAGE" : "No file"}, status=204)

        size         = os.path.getsize(path)
        range_match  = self.get_http_range(request)
        content_type = self.get_content_type(path)
        video_file   = open(path, 'rb')
        
        if range_match :
            first_byte, last_byte   = self.get_range(size,range_match)
            length                  = last_byte - first_byte + 1
            resp                    = StreamingHttpResponse(RangeFileWrapper(video_file, offset=first_byte, length=length), status=206, content_type=content_type)
            resp['Content-Length']  = str(length)
            resp['Content-Range']   = f'bytes {first_byte}-{last_byte}/{size}'    
        else:
            resp = HttpResponse(FileWrapper(video_file), content_type=content_type)
            resp['Content-Length'] = str(size)    
        
        resp['Accept-Ranges'] = 'bytes'
        
        return resp
    

class VideoLayoutView(View) :
    def get_user_id(self,request) :
        if "HTTP_Authorization" in request.META :
            access_token = request.META.get('HTTP_Authorization')
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            login_user_id= User.objects.get(id=payload['id']).id
            return login_user_id

        else : return False
    
    def get_S_list(self,lectures) :
        try :
            S_id_list = [(L["section__id"],L["section__name"]) for L in lectures]
            S_id_list = list(set(S_id_list))
            S_id_list.sort()
            return S_id_list
        except KeyError :
            return False

    def check_user_finished_lecture(self,course_id, result,user_id) :
        try :
            finish_queryset = LectureCompletion.objects.select_related("lecture__section__course"
                ).values("id", "lecture__section__course__id"
                ).filter(lecture__section__course__id=course_id
                ).filter(user_id=user_id)


            finish_list = [F["id"] for F in finish_queryset]

            for section in result["section_list"] :
                for lecture in section["lecture_list"] :
                    if lecture["lecture_id"] in finish_list :
                        lecture["finished"] = 1
            
            return (True, result)
        except KeyError :
            return (False, "Key error in result")

    key_match = {
        "course_id" : "section__course__id",
        "course_name" : "section__course__name",
        "period" : "section__course__learning_period_month",
        "setion_id" : "section__id",
        "section_name" : "section__name",
        "lecture_id" : "id",
        "lecture_name" : "name",
        "lecture_video_url" : "storage_path",
        "lecture_runtime" : "play_time"
    }

    def get(self,request,course_id) :
        lectures    = Lecture.objects.select_related('section', 'section__course').values(
            *[self.key_match[key] for key in self.key_match]
            ).prefetch_related('lecture_completion_by_lecture'
            ).filter(section__course__id=course_id)
        
        if lectures.count() == 0 :
            return JsonResponse({"MESSAGE" : "no_lecture_in_course"}, status=400)

        
        S_id_list   = self.get_S_list(lectures)
        _L          = lectures[0]
        
        result = {
            "course_id"      : _L[self.key_match["course_id"]],
            "course_name"    : _L[self.key_match["course_name"]],
            "period"         : _L[self.key_match["period"]],
            "section_legnth" : len(lectures),
            "section_list"   : [{
                "setion_id"     : S[0],
                "section_name"  : S[1],
                "lecture_list"  : [{
                    "lecture_id"        : L[self.key_match["lecture_id"]],
                    "lecture_name"      : L[self.key_match["lecture_name"]],
                    "lecture_video_url" : L[self.key_match["lecture_video_url"]],
                    "lecture_runtime"   : L[self.key_match["lecture_runtime"]],
                    "finished"          : 0
                } for L in lectures if L["section__id"] == S[0]]
            } for S in S_id_list]
        }

        user_id = self.get_user_id(request)
        if user_id : 
            boolean, message = self.check_user_finished_lecture(course_id, result, user_id)
            if boolean :
                result = message

        print(connection.queries)

        return JsonResponse(result)

class LectureDetail(View) :
    def get(self,request,lecture_id) :

        lecture = Lecture.objects.get(id=lecture_id)

        return JsonResponse({
            "lecture_id": lecture.id,
            "lecture_name": lecture.name,
            "lecture_video_url": lecture.storage_path,
            "lecture_runtime": lecture.play_time,
            "finished": 0
        }, status= 200)
