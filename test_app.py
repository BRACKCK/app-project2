from app import app
import unittest

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
    


    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'WattWise', response.data)

    def test_submit_personal_info(self):
        response = self.client.post('/', data=dict(
            name='Jane',
            email='jane@example.com',
            phone='0700000000'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Assessment', response.data)

    def test_assessment_form_page(self):
        response = self.client.get('/assessment')
        self.assertEqual(response.status_code, 200)

    def test_404_for_invalid_route(self):
        response = self.client.get('/no-such-page')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
