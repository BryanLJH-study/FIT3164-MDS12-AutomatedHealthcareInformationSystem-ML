import unittest
import io
import cv2
import sys
sys.path.append('src/')  # Adjust the relative path as needed
from app import app


class TestPatientHTR(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.valid_image = cv2.imread("docs/test/digital_1.jpg")
        self.invalid_file = cv2.imread("docs/templates/Patient_Registration_v1.docx")
        self.incorrect_template_image = cv2.imread("docs/test/random_form.jpg")

    def test_valid_request(self):
        response = self.app.post('/patient_htr', data={'image': (io.BytesIO(cv2.imencode('.jpg', self.valid_image)[1]), 'valid_image.jpg')})
        self.assertEqual(response.status_code, 200)

    def test_invalid_file(self):
        response = self.app.post('/patient_htr', data={'image': (io.BytesIO(self.invalid_file), 'invalid_image.txt')})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'Invalid file format. Supported formats: jpg, jpeg, png')

    def test_incorrect_template(self):
        response = self.app.post('/patient_htr', data={'image': (io.BytesIO(cv2.imencode('.jpg', self.incorrect_template_image)[1]), 'incorrect_template_image.jpg')})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()