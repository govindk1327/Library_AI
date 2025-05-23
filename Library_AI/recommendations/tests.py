from django.test import TestCase
from recommendations.pipeline import extract_title

class ClovaPipelineTest(TestCase):
    def test_extract_title_from_clova(self):
        sample = "1. **해리 포터 시리즈**: 마법과 모험이 가득한 이야기입니다."
        title = extract_title(sample)
        self.assertIn("해리 포터", title)
