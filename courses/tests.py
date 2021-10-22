import unittest
import json
import re

from django.http.request import HttpRequest
from courses.views  import VideoPlayer

class VideoPlayerTest(unittest.TestCase) :
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

    def test_get_normal(self) :
        path = 'test_video.mp4'
        self.assertEqual(self.test_cls.get(self.test_req, path).content[:20], b'\x00\x00\x00\x18ftypiso6\x00\x00\x00\x01iso6')

    def test_get_no_file(self) :
        path = '!Q2w#E4r'
        # json 끼리 비교가 안되기 대문에 파이썬 데이터로 변경
        self.assertEqual(json.loads(self.test_cls.get(self.test_req, path).content), {"MEESAGE" : "No file"})

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