from rest_framework.test import APITestCase

class URLTests(APITestCase):

    urls_to_test = [
        '/api/registration/',
        '/api/login/',
        '/api/token/refresh/',
        '/api/logout/',
    ]

    def test_all_urls_exist(self):
        for url in self.urls_to_test:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, 404, f"URL {url} not found (404)")