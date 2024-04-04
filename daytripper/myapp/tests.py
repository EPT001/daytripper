from django.test import TestCase,  Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Bookmark
from .forms import UserForm
import unittest
from unittest.mock import patch
from .services import text_search, nearby_search, get_place_details

#test class in views
class TestViews(TestCase):
    #setup test user
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    #is signupPage render signup.html
    def test_signup_page(self):
        response = self.client.get(reverse('myapp:signupPage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/signup.html')
    #is loginPage render loign.html
    def test_login_page(self):
        response = self.client.get(reverse('myapp:loginPage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/login.html')
    #is current_location render search.html
    def test_current_location_page(self):
        response = self.client.get(reverse('myapp:current_location'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/search.html')
    #is selected_place render details.html with test place_id
    def test_selected_place_page(self):
        place_id = 'ChIJj61dQgK6j4AR4GeTYWZsKWw' #random place ID
        response = self.client.get(reverse('myapp:selected_place', kwargs={'placeId': place_id}))
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'myapp/details.html')
    #is user_bookmarks render bookmarks.html
    def test_user_bookmarks_page(self):
        response = self.client.get(reverse('myapp:user_bookmarks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/bookmarks.html')
    # test add and deleting bookmark
    def test_delete_bookmark(self):
        bookmark = Bookmark.objects.create(user=self.user, place_id='some_place_id', place_name='Some Place')
        response = self.client.get(reverse('myapp:delete_bookmark', kwargs={'bookmark_id': bookmark.id}))
        self.assertEqual(response.status_code, 302)  # Redirects after deletion
        self.assertEqual(Bookmark.objects.count(), 0)  # Assuming the bookmark is deleted
    #test user logout 
    def test_logout(self):
        response = self.client.get(reverse('myapp:logout'))
        self.assertEqual(response.status_code, 302)  # Redirects after logout
        self.assertFalse('_auth_user_id' in self.client.session)  # Asserts user is logged out


class TestModels(TestCase):
    #test add bookmark in model
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.bookmark = Bookmark.objects.create(user=self.user, place_id='test_place_id', place_name='Test Place')

    def test_bookmark_creation(self):
        self.assertEqual(self.bookmark.user, self.user)
        self.assertEqual(self.bookmark.place_id, 'test_place_id')
        self.assertEqual(self.bookmark.place_name, 'Test Place')

class TestForms(TestCase):
    #try signup new testuer
    def test_user_form_valid_data(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())
    #try if user input incorrect data
    def test_user_form_invalid_data(self):
        form_data = {
            'username': 'testuser',
            'email': 'invalidemail',  # Invalid email format
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())

#test function in services.py that send data to Google places API
class TestGooglePlacesAPI(TestCase):

    @patch('requests.post')
    def test_text_search(self, mock_post):
        mock_response = {'results': [{'name': 'Place 1'}, {'name': 'Place 2'}]}
        mock_post.return_value.json.return_value = mock_response

        query = 'restaurant'
        response = text_search(query)

        self.assertEqual(response, mock_response)
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_nearby_search(self, mock_post):
        mock_response = {'results': [{'name': 'Place 1'}, {'name': 'Place 2'}]}
        mock_post.return_value.json.return_value = mock_response

        place_type = 'restaurant'
        radius = 1000
        latitude = 40.7128
        longitude = -74.0060
        response = nearby_search(place_type, radius, latitude, longitude)

        self.assertEqual(response, mock_response)
        mock_post.assert_called_once()

    @patch('requests.get')
    def test_get_place_details(self, mock_get):
        mock_response = {'result': {'name': 'Place 1', 'formatted_address': '123 Street'}}
        mock_get.return_value.json.return_value = mock_response

        place_id = 'some_place_id'
        response = get_place_details(place_id)

        self.assertEqual(response, mock_response)
        mock_get.assert_called_once()

if __name__ == '__main__':
    unittest.main()