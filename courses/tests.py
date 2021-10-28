import re

from django.http.request    import HttpRequest
from django.test.client     import Client
from django.test            import TestCase

from courses.views          import VideoPlayer, VideoLayoutView
from courses.models         import Category, CourseInfo, InfoType, Lecture, LectureCompletion, Level, Section, Course, SubCategory, Hashtag
from users.models           import User
from eval.models           import Review 
from orders.models import Order, OrderItem

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

class CourseListTest(TestCase):
    def setUp(self):

        user_list = [
            User(
                nickname = 'BnDC',
                email = 'a@naver.com',
                phone_number = '01012345678',
            )
        ]

        User.objects.bulk_create(user_list)
        category_list = [
            Category(
                id  = 1,
                name = 'developing',
            ),
            Category(
                id  = 2,
                name = 'Security',
            ),
            Category(
                id  = 3,
                name = 'Creative',
            ),
            Category(
                id  = 4,
                name = 'Marketing',
            ),
            Category(
                id  = 5,
                name = 'Language',
            ),
            Category(
                id  = 6,
                name = 'Career',
            ),
            Category(
                id  = 7,
                name = 'Culture',
            )
        ]

        Category.objects.bulk_create(category_list)

        subcategory_list = [
            SubCategory(
                id          = 1,
                name        = 'web-develpoing',
                category_id = 1,
            ),
            SubCategory(
                id          = 2,
                name        = 'front-end',
                category_id = 1,
            ),
            SubCategory(
                id          = 3,
                name        = 'back-end',
                category_id = 1,
            ),
            SubCategory(
                id          = 4,
                name        = 'fullstack',
                category_id = 2,
            ),
            SubCategory(
                id          = 5,
                name        = 'mobile',
                category_id = 2,
            ),
            SubCategory(
                id          = 6,
                name        = 'programming-language',
                category_id = 2,
            ),
            SubCategory(
                id          = 7,
                name        = 'data structure',
                category_id = 3,
            )
        ]

        SubCategory.objects.bulk_create(subcategory_list)
        
        Level.objects.bulk_create(
            [
                Level(name = '1'),
                Level(name = '2'),
                Level(name = '3')
            ]
        )

        course_list = [
            Course(
                id = 1,
                name = 'HTML/CSS',
                detail = 'detail 사진 url',
                summary = '요약정리',
                thumbnail_url = 'thumbnail 사진 url',
                visible = 1,
                price = 10000,
                learning_period_month = 999,
                level_id = 1,
                subcategory_id = 1,
                sharer_id = 1,
            ),
            Course(
                id = 2,
                name = 'javascript',
                detail = 'detail 사진 url',
                summary = '요약정리',
                thumbnail_url = 'thumbnail 사진 url',
                visible = 1,
                price = 20000,
                learning_period_month = 999,
                level_id = 1,
                subcategory_id = 1,
                sharer_id = 1,
            ),
            Course(
                id = 3,
                name = 'python',
                detail = 'detail 사진 url',
                summary = '요약',
                thumbnail_url = 'thumbnail 사진 url',
                visible = 1,
                price = 30000,
                learning_period_month = 999,
                level_id = 2,
                subcategory_id = 2,
                sharer_id = 1,
            ),
            Course(
                id = 4,
                name = 'java',
                detail = 'detail 사진 url',
                summary = '요약',
                thumbnail_url = 'thumbnail 사진 url',
                visible = 1,
                price = 30000,
                learning_period_month = 999,
                level_id = 2,
                subcategory_id = 2,
                sharer_id = 1,
            ),
            Course(
                id = 5,
                name = 'django',
                detail = 'detail 사진 url',
                summary = '요약',
                thumbnail_url = 'thumbnail 사진 url',
                visible = 1,
                price = 40000,
                learning_period_month = 999,
                level_id = 3,
                subcategory_id = 3,
                sharer_id = 1,
            ),
            Course(
                id = 6,
                name = 'flask',
                detail = 'detail 사진 url',
                thumbnail_url = 'thumbnail 사진 url',
                visible = 1,
                summary = '요약',
                price = 50000,
                learning_period_month = 999,
                level_id = 3,
                subcategory_id = 3,
                sharer_id = 1,
            ),
            Course(
                id = 7,
                name = '네트워크',
                detail = 'detail 사진 url',
                thumbnail_url = 'thumbnail 사진 url',
                visible = 1,
                summary = '요약',
                price = 60000,
                learning_period_month = 999,
                level_id = 1,
                subcategory_id = 4,
                sharer_id = 1,
            ),
            Course(
                id = 8,
                name = '보안',
                detail = 'detail 사진 url',
                thumbnail_url = 'thumbnail 사진 url',
                summary = '요약',
                visible = 1,
                price = 70000,
                learning_period_month = 999,
                level_id = 1,
                subcategory_id = 4,
                sharer_id = 1,
            ),
            Course(
                id = 9,
                name = 'C언어',
                detail = 'detail 사진 url',
                thumbnail_url = 'thumbnail 사진 url',
                summary = '요약',
                visible = 1,
                price = 90000,
                learning_period_month = 999,
                level_id = 2,
                subcategory_id = 4,
                sharer_id = 1,
            ),
            Course(
                id = 10,
                name = 'C++',
                detail = 'detail 사진 url',
                thumbnail_url = 'thumbnail 사진 url',
                visible = 1,
                price = 100000,
                summary = '요약',
                learning_period_month = 999,
                level_id = 2,
                subcategory_id = 5,
                sharer_id = 1,
            ),
        ]

        Course.objects.bulk_create(course_list)

        Review.objects.bulk_create(
            [
                Review(
                    id        = 1,
                    user_id   = 1,
                    course_id = 1,
                    stars     = 3
                    ),
                Review(
                    id        = 2,
                    user_id   = 1,
                    course_id = 2,
                    stars     = 2,
                )]
        )

    def tearDown(self):
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Hashtag.objects.all().delete()
    
    def test_category_list_get_success(self):
        client = Client()
        response = client.get('/courses/categories', content_type = "application/json")
        self.maxDiff = None
        self.assertEqual(response.json(), {
            "result" : [{
                "id"   : category.id,
                "name" : category.name,
                "sub_category" : [{
                    "id"   : subcategory.id,
                    "name" : subcategory.name,
                    "tags"  : [{
                        "id"   : hashtag.id,
                        "name" : hashtag.name,
                    } for hashtag in Hashtag.objects.all()]
                } for subcategory in category.sub_categories.all()]
            } for category in Category.objects.all()] 
            } 
        )

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
        SubCategory.objects.all().delete()
        Course.objects.all().delete()
        Review.objects.all().delete()
        Level.objects.all().delete()
    
    def test_course_list_get_success(self):
        client = Client()
        response = client.get('/courses/1/1')

        self.maxDiff = None

        self.assertEqual(response.json(), { 
            "result" : [{
                "id"       : 1,
                "thumbnail": 'thumbnail 사진 url',
                "title"    : 'HTML/CSS',
                "author" :'BnDC',
                "price"    : "10000.00",
                "summary"  : '요약정리',
                "level"    : "1",
                "star-number" : 3.0,
                "author" : 'BnDC'
                },

                {
                "id"       : 2,
                "thumbnail": 'thumbnail 사진 url',
                "title"    : 'javascript',
                "price"    : "20000.00",
                "summary"  : '요약정리',
                "star-number"  : 2.0,
                "level"    : "1",
                "author"    : "BnDC",
                }]
            }
        )

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

class CourseViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            nickname = 'UU',
            email    = 'abc@naver.com',
            kakao_id = '1',
        )

        category_list = [
            Category(
                id  = 1,
                name = 'developing',
            ),
            Category(
                id  = 2,
                name = 'Security',
            ),
        ]

        Category.objects.bulk_create(category_list)

        subcategory_list = [
            SubCategory(
                id          = 1,
                name        = 'web-developing',
                category_id = 1,
            ),
            SubCategory(
                id          = 2,
                name        = 'front-end',
                category_id = 1,
            ),
        ]

        SubCategory.objects.bulk_create(subcategory_list)

        level_list = [
            Level(
                id = 1,
                name = '1'
            ),
            Level(
                id =2,
                name = '2'
            ),
            Level(
                id =3,
                name = '3'
            ),
        ]

        Level.objects.bulk_create(level_list)

        Course.objects.create(
            id = 1 ,
            name = "python 기초",
            summary = "기초를 잘 다지자",
            detail = "detail cut",
            thumbnail_url = "thumb",
            visible = 1,
            price = 10000,
            learning_period_month = 999,
            subcategory_id = 1,
            sharer_id = 1,
            level_id = 2,
        )

        hashtag_list = [
            Hashtag(
                id = 1,
                name = 'HTML/CSS'
            ),
            Hashtag(
                id = 2,
                name = 'JavaScript'
            ),
            Hashtag(
                id = 3,
                name = 'Java'
            ),
        ]

        Hashtag.objects.bulk_create(hashtag_list)
        
        
        section_list = [
            Section(
                id =1,
                name = '첫번째',
                #objectives = '1',
                priority = 1,
                course_id = 1,
            ),

            Section(
                id=2,
                name = '두번째',
                #objectives = '2',
                priority = 1,
                course_id = 1,
            )
        ]

        Section.objects.bulk_create(section_list)

        lecture_list = [
            Lecture(
                id = 1 ,
                name = '1강',
                storage_key = '1',
                storage_path = '1',
                priority = 1,
                play_time = 3,
                section_id = 1,
            ),
            Lecture(
                id =2 ,
                name = '2강',
                storage_key = '1',
                storage_path = '1',
                priority = 1,
                play_time = 3,
                section_id = 1,
            ),
            Lecture(
                id =3,
                name = '1강',
                storage_key = '1',
                storage_path = '1',
                priority = 1,
                play_time = 3,
                section_id = 2,
            ),
            Lecture(
                id =4,
                name = '2강',
                storage_key = '1',
                storage_path = '1',
                priority = 1,
                play_time = 3,
                section_id = 2,
            )]
            
        Lecture.objects.bulk_create(lecture_list)

        InfoType.objects.bulk_create([
            InfoType(id=1, name = 'whatolearn'),
            InfoType(id=2, name = 'recommend'),
            InfoType(id=3, name = 'precourse'),
            ]
        )

        CourseInfo.objects.bulk_create([
            CourseInfo(
                id = 1,
                name = '1',
                info_type_id = 1,
                course_id = 1,
            ),
            CourseInfo(
                id = 2,
                name = '2',
                info_type_id = 2,
                course_id = 1,
            ),
            CourseInfo(
                id = 3,
                name = '3',
                info_type_id = 3,
                course_id = 1,
                )
            ]
        )

        Review.objects.create(
                id = 1,
                user_id = 1,
                course_id = 1,
                stars = 1,
        )

        Order.objects.create(
            id = 1,
            user_id = 1,
            #course_id = 1,
        )
        
        OrderItem.objects.create(
            id = 1,
            order_id = 1,
            course_id = 1,
        )

    def tearDown(self):
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Hashtag.objects.all().delete()
    
    def test_course_get_success(self):
        client = Client()
        response = client.get('/courses/course/1', content_type = "application/json")
        
        self.maxDiff = None
        self.assertEqual(response.json(), {
            "result" : {
                "id"      : 1,
                "name"    : "python 기초",
                "summary" : "기초를 잘 다지자",
                "detail"  : "detail cut",
                "thumbnail"   : "thumb",
                "price"       : '10000.00',
                "subcategory" : "web-developing",
                "category"    : "developing",
                "course_info" : [
                    {
                    "id"      : 1,
                    "name"    : "1",
                    "info_type_id": 1
                    },
                    {
                    "id"      : 2,
                    "name"    : "2",
                    "info_type_id": 2 
                    },
                    {
                    "id"      : 3,
                    "name"    : "3",
                    "info_type_id": 3 
                    }
                ],
                "sections"    : [{
                    "id"      : 1,
                    "name"    : '첫번째',
                    "lectures": [{
                        "id"  : 1,
                        "name"  : '1강',
                        "play_time"    : 3,
                        "storage_key"  : '1',
                        "storage_path" : '1',
                    },
                    {
                        "id"  : 2,
                        "name"  : '2강',
                        "play_time"    : 3,
                        "storage_key"  : '1',
                        "storage_path" : '1',
                    }],
                },
                {
                    "id"      : 2,
                    "name"    : '두번째',
                    "lectures": [{
                        "id"  : 3,
                        "name"  : '1강',
                        "play_time"    : 3,
                        "storage_key"  : '1',
                        "storage_path" : '1',
                    },
                    {
                        "id"  : 4,
                        "name"  : '2강',
                        "play_time"    : 3,
                        "storage_key"  : '1',
                        "storage_path" : '1',
                    }]
                }],
                "level"  : '2',
                "stars"  : 1.0,
                "people" : 1,
            }
        })
