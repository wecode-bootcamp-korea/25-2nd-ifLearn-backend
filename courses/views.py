import os
import re
import mimetypes
import jwt
from wsgiref.util           import FileWrapper
from django.http            import JsonResponse, StreamingHttpResponse
from django.http.response   import HttpResponse
from django.views           import View 
from django.db.models       import Q, Avg, Case, Value, When

from ifLearn.settings       import SECRET_KEY, ALGORITHM
from courses.models         import Category, Course, Hashtag, Lecture, LectureCompletion
from users.models           import User


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
        # 띄어쓰기를 엄격하게 하지 않기 위해 \s* 을 계속 붙임
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
            return JsonResponse({"MEESAGE" : "No file"}, status=400)

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

class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        hashtags   = Hashtag.objects.all()

        result = [{
            "id"           : category.id,
            "name"         : category.name,
            "sub_category" : [{
                "id"   : subcategory.id,
                "name" : subcategory.name,
                "tags"  : [{
                    "id"   : hashtag.id,
                    "name" : hashtag.name,

                    } for hashtag in hashtags]
                } for subcategory in category.sub_categories.all()] 
            } for category in categories]
        
        return JsonResponse({"result" : result}, status = 200)


class VideoLayoutView(View) :
    def get_user_id(self,request) :
        if "Authorization" in request.headers :
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            login_user_id= User.objects.get(id=payload['id']).id
            return login_user_id

        else : return -1

    # 8000/course/course_id
    def get(self, request, course_id) :
        user_id = self.get_user_id(request)
        course = Course.objects.annotate(lectures_count = Count("sections__lecture")).prefetch_related('sections', Prefetch('sections__lecture', queryset=Lecture.objects.annotate(
            is_finished=Case(When(lecture_completion_by_lecture__user_id=user_id, then=Value(1)),
                             default=Value(0))))).get(id = course_id)

        result = {
            "course_id" : course.id,
            "course_name" : course.name,
            "period" : course.learning_period_month,
            "section_length" : int(course.lectures_count),
            "section_list" : [{
                "section_id" : S.id,
                "section_name" : S.name,
                "lecture_list" : [{
                    "lecture_id" : L.id,
                    "lecture_name" : L.name,
                    "lecture_video_url" : L.storage_path,
                    "lecture_runtime" : L.play_time,
                    "finished" : L.is_finished
                } for L in S.lecture.all()]
            }for S in course.sections.all()]
        }

        return JsonResponse(result)



class LectureDetail(View) :
    def get_user_id(self,request) :
        if "Authorization" in request.headers :
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            login_user_id= User.objects.get(id=payload['id']).id
            return login_user_id

        else : return False

    def get(self,request,lecture_id) :
        lecture         = Lecture.objects.get(id=lecture_id)
        user_id         = self.get_user_id(request)
        finish_queryset = LectureCompletion.objects.values('user_id', 'lecture_id'
        ).filter(user_id=user_id,lecture_id=lecture_id)

        return JsonResponse({
            "lecture_id"        : lecture.id,
            "lecture_name"      : lecture.name,
            "lecture_video_url" : lecture.storage_path,
            "lecture_runtime"   : lecture.play_time,
            "finished"          : int(finish_queryset.exists())
        }, status= 200)
