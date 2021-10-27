import json
import re

from django.http.request import HttpRequest
from django.test.client import Client
from courses.views       import VideoPlayer
from django.test         import TestCase

from courses.models import SubCategory, Category, Course, Hashtag 

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

class CategoryViewTest(TestCase):
    def setUp(self):

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
