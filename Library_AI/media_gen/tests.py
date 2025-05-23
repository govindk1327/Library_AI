import os
import hashlib
from django.test import TestCase
from unittest.mock import patch
from media_gen.image_generator import generate_image

class ImageGeneratorTest(TestCase):
    @patch("media_gen.image_generator.requests.post")
    def test_generate_image_success(self, mock_post):
      
        mock_post.return_value.status_code = 200
        mock_post.return_value.content = b"fake_image_data"

        prompt = "Test prompt"
        test_dir = "test_images"
        image_path = generate_image(prompt, save_dir=test_dir)

        self.assertTrue(os.path.exists(image_path))

        
        os.remove(image_path)
        os.rmdir(test_dir)

    @patch("media_gen.image_generator.requests.post")
    def test_image_cache(self, mock_post):
 
        mock_post.return_value.status_code = 200
        mock_post.return_value.content = b"fake_image_data"

        prompt = "Caching test"
        test_dir = "test_images"
        image_path1 = generate_image(prompt, save_dir=test_dir)
        image_path2 = generate_image(prompt, save_dir=test_dir)

        self.assertEqual(image_path1, image_path2)
        self.assertTrue(os.path.exists(image_path2))

        os.remove(image_path2)
        os.rmdir(test_dir)
