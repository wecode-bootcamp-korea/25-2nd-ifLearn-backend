import os
import re
import mimetypes
import jwt
from wsgiref.util           import FileWrapper
from django.http            import JsonResponse, StreamingHttpResponse
from django.http.response   import HttpResponse
from django.views           import View 
from django.db.models       import Q, Avg

from ifLearn.settings       import SECRET_KEY, ALGORITHM

from courses.models         import Category, Course, SubCategory , Hashtag, Lecture, LectureCompletion
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
                "tags" : [{
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
                ).values("lecture_id", "lecture__section__course__id"
                ).filter(lecture__section__course__id=course_id, user_id=user_id)

            finish_list = [F["lecture_id"] for F in finish_queryset]

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
            course_get = Course.objects.filter(id=course_id)
            if not course_get.exists() :
                return JsonResponse({"MESSAGE" : "invalid_course_id"}, status=400)
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
        
class CourseListView(View):
    def get(self, request, category_id = None, sub_category_id = None):

        page   = request.GET.get('page', 1)
        level  = request.GET.getlist('level', None)
        search = request.GET.get('search', None)

        sub_category_q = Q()
        course_q       = Q()

        if category_id:
            sub_category_q.add(Q(category_id = category_id), sub_category_q.AND)
        
        if sub_category_id:
            sub_category_q.add(Q(id = sub_category_id), sub_category_q.AND)

        if level:
            course_q.add(Q(level__in = level), course_q.AND)

        if search:
            course_q.add(Q(name__icontains = search), course_q.AND)

        sub_categories = SubCategory.objects.filter(sub_category_q).prefetch_related('courses_by_subcategory')

        result = []

        for sub_category in sub_categories:
            for course in sub_category.courses_by_subcategory.filter(course_q):

                result.append({
                    "id": course.id,
                    "thumbnail": course.thumbnail_url,
                    "title": course.name,
                    "author" :course.sharer.nickname,
                    "price": course.price,
                    "summary": course.summary,
                    "level": course.level.name,
                    "star-number" : course.review_by_course.aggregate(star=Avg('stars'))['star'],
                })

        return JsonResponse({"result" : result}, status = 200)

class CourseView(View):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id = course_id)
        
        except Course.DoesNotExist:
            return JsonResponse({"message" : "DOES_NOT_EXIST"}, status = 200)

        result = {
            "id"      : course.id,
            "name"    : course.name,
            "summary" : course.summary,
            "detail"  : course.detail,
            "thumbnail"   : course.thumbnail_url,
            "price"       : course.price,
            "subcategory" : course.subcategory.name,
            "category"    : course.subcategory.category.name,
            "course_info" : [{
                "id"      : info.id,
                "name"    : info.name,
                "info_type_id": info.info_type_id
            } for info in course.course_info_by_course.all()],
            "sections"    : [{
                "id"      : section.id,
                "name"    : section.name,
                "lectures": [{
                    "id"  : lecture.id,
                    "name"  : lecture.name,
                    "play_time"    : lecture.play_time,
                    "storage_key"  : lecture.storage_key,
                    "storage_path" : lecture.storage_path,
                } for lecture in section.lecture.all()],
            } for section in course.sections.all()],
            "level"  : course.level.name,
            "stars"  : course.review_by_course.aggregate(star=Avg('stars'))['star'],
            "people" : len(course.order_item_by_course.all()),
        }

        return JsonResponse({"result" : result}, status = 200)
