import re

from django.http.request    import HttpRequest
from django.test.client     import Client
from courses.views          import VideoPlayer
from django.test            import TestCase
from courses.models         import Category, Lecture, LectureCompletion, Level, Section, Course, SubCategory
from users.models           import User
from courses.views          import VideoLayoutView
class VideoPlayerTest(TestCase) :
    test_cls = VideoPlayer()
    test_req = HttpRequest()
    
    def test_get_content_type_noraml(self):
        path = 'test_video.mp4'
        self.assertEqual(self.test_cls.get_content_type(path), 'video/mp4')
    
    def test_get_content_type_wrong_file(self) :
        path = 'test_empty_file'
        self.assertEqual(self.test_cls.get_content_type(path), 'application/octet-stream')

    def test_get_http_range_normal(self) :
        test_req                    = HttpRequest()
        test_req.META['HTTP_RANGE'] = 'bytes = 0-150'
        self.assertEqual(self.test_cls.get_http_range(test_req).group(0), 'bytes = 0-150')

    def test_get_http_range_no_range(self) :
        self.assertEqual(self.test_cls.get_http_range(self.test_req), None)

    def test_get_range_normal(self) :
        size = 300
        range_match = re.match("(\d+)\s(\d*)","0 150")
        self.assertEqual(self.test_cls.get_range(size,range_match), (0,150))

    def test_get_range_out_of_size(self) :
        size = 100
        range_match = re.match("(\d+)\s(\d*)","0 150")
        self.assertEqual(self.test_cls.get_range(size,range_match), (0,100-1))

    def test_get_with_range(self) :
        path = 'test_video.mp4'
        test_req                    = HttpRequest()
        test_req.META['HTTP_RANGE'] = 'bytes = 0-150'
        self.assertEqual(self.test_cls.get(test_req, path).headers["Content-Range"], "bytes 0-150/6165797")

    def test_get_with_range_negative(self) :
        path = 'test_video.mp4'
        test_req                    = HttpRequest()
        test_req.META['HTTP_RANGE'] = 'bytes = -200-150'
        # 마이너스가 붙으면, regex와 match되지 않아 range를 무시한다.
        self.assertEqual(self.test_cls.get(self.test_req, path).content[:20], b'\x00\x00\x00\x18ftypiso6\x00\x00\x00\x01iso6')

    def test_get_normal(self) :
        response = self.client.get('/course/test_video.mp4').content
        self.assertEqual(response[:20], b'\x00\x00\x00\x18ftypiso6\x00\x00\x00\x01iso6')

    def test_get_no_file(self) :
        response = self.client.get('/course/noExistFile.mp4')
        # json 끼리 비교가 안되기 대문에 파이썬 데이터로 변경
        self.assertEqual(response.json(), {"MEESAGE" : "No file"})

class VideoLayoutTest(TestCase) :
    INSTANCE = VideoLayoutView()


    def setUp(self):
        User.objects.create(
            id          = 1,
            nickname    = "test_name",
            email       = "test1@sample.com",
            phone_number= "010-0000-0000",
            introduce   = "",
            sharer      = 1            
        )

        Level.objects.create(
            id          = 1,
            name        = "test_level"
        )
        
        Category.objects.create(
            id          = 1,
            name        = "test_cate"
        )

        SubCategory.objects.create(
            id          = 1,
            name        = "test_subcate",
            category_id = 1
        )

        Course.objects.create(
            id                      = 1,
            name                    = "test_course",
            summary                 = "summary",
            detail                  = "detail",
            thumbnail_url           = "url",
            visible                 = 1,
            price                   = 77000,
            learning_period_month   = 999,
            level_id                = 1,
            sharer_id               = 1,
            subcategory_id          = 1
        )

        Course.objects.create(
            id                      = 999,
            name                    = "test_course",
            summary                 = "summary",
            detail                  = "detail",
            thumbnail_url           = "url",
            visible                 = 1,
            price                   = 77000,
            learning_period_month   = 999,
            level_id                = 1,
            sharer_id               = 1,
            subcategory_id          = 1
        )

        Section.objects.create(
            id          = 1,
            name        = "test_section",
            priority    = 1,
            course_id   = 1
        )

        Lecture.objects.create(
            id           = 1,
            name         = "test_lecture",
            storage_key  = "blank",
            storage_path = "https://www.naver.com",
            priority     = 1,
            play_time    = 120,
            section_id   = 1      
        )

        LectureCompletion.objects.create(
            id          = 1,
            user_id     = 1,
            lecture_id  = 1
        )

    def tearDown(self) :
        User.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Level.objects.all().delete()
        Course.objects.all().delete()
        Section.objects.all().delete()
        Lecture.objects.all().delete()
        LectureCompletion.objects.all().delete()

    def test_success_get_user_id(self) :
        request  = HttpRequest()
        request.META["HTTP_Authorization"] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.jSxa98uKu7i-QAszAY0wdZVh3VrriKqvh12cSWEQZ_w'
        self.assertEqual(self.INSTANCE.get_user_id(request), 1)

    def test_fail_get_user_id_no_token(self) :
        request  = HttpRequest()
        self.assertEqual(self.INSTANCE.get_user_id(request), False)
    
    def test_success_get_S_list(self) :
        lectures = Lecture.objects.select_related("section").values("section__id","section__name")
        self.assertEqual(self.INSTANCE.get_S_list(lectures),[(1,'test_section')])

    def test_fail_get_S_list_key_error(self) :
        lectures = Lecture.objects.select_related("section").values("section__name").filter(id=1)
        self.assertEqual(self.INSTANCE.get_S_list(lectures),False)

    def test_success_check_user_finished_lecture(self) :
        course_id   = 1
        user_id     = 1
        result = {
            "section_list" : [{
                "lecture_list" : [{
                    "lecture_id" : 1,
                    "finished" : 0
                }]
            }]
        }
        self.assertEqual(self.INSTANCE.check_user_finished_lecture(course_id,result,user_id),
            (True,{
                    "section_list" : [{
                        "lecture_list" : [{
                            "lecture_id" : 1,
                            "finished" : 1
                        }]
                    }]
                }))
            
    def test_fail_check_user_finished_lecture(self) :
        course_id   = 1
        user_id     = 1
        result = {}
        self.assertEqual(self.INSTANCE.check_user_finished_lecture(course_id,result, user_id),
        (False, "Key error in result"))

    def test_success_get(self) :
        client = Client()
        resp = client.get('/course/video/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {
            "course_id": 1,
            "course_name": "test_course",
            "period": 999,
            "section_legnth": 1,
            "section_list": [
                {
                    "setion_id": 1,
                    "section_name": "test_section",
                    "lecture_list": [
                        {
                            "lecture_id": 1,
                            "lecture_name": "test_lecture",
                            "lecture_video_url": "https://www.naver.com",
                            "lecture_runtime": 120,
                            "finished": 0
                        }]
                }]
        })

    def test_fail_get_course_index_out_of_range(self) :
        client = Client()
        resp = client.get('/course/video/9999')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {"MESSAGE" : "invalid_course_id"})

    def test_fail_get_course_no_lecture(self) :
        client = Client()
        resp = client.get('/course/video/999')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {"MESSAGE" : "no_lecture_in_course"})
    