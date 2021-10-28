from django.http.request import HttpRequest
from django.test import TestCase
from courses.models import Category, Lecture, LectureCompletion, Level, Section, Course, SubCategory
from courses.views import VideoLayoutView
from users.models   import User

class VideoLayoutTest(TestCase) :
    test_inst = VideoLayoutView()


    def setUp(self):
        User.objects.create(
            nickname    = "test_name",
            password    = "$2b$12$AQoRYPlTRX4twve49AIsQemJCohgtAL.TGja7jsoGcKCaCUYzUune",
            email       = "test1@sample.com",
            phone_number='010-0000-0000',
            introduce   = '',
            sharer      = 1            
        )
        
        Category.objects.create(
            name        = "test_cate"
        )

        SubCategory.objects.create(
            name        = "test_subcate",
            category_id = 1
        )

        Level.objects.create(
            name        = "test_level"
        )

        Course.objects.create(
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
            name        = "test_section",
            objectives  = "blank",
            priority    = 1,
            course_id   = 1
        )

        Lecture.objects.create(
            name         = "test_lecture",
            storage_key  = "blank",
            storage_path = "https://www.naver.com",
            priority     = 1,
            play_time    = 120,
            section_id   = 1      
        )

        LectureCompletion.objects.create(
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
        print(1)
        test_req  = HttpRequest()
        test_req.META["Authorization"] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.jSxa98uKu7i-QAszAY0wdZVh3VrriKqvh12cSWEQZ_w'
        self.assertEqual(self.test_inst.get_user_id(test_req), 1)