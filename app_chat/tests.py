from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import UserModel, Request, ChatModel
from rest_framework.authtoken.models import Token

class APITestSetup(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserModel.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.user2 = UserModel.objects.create_user(
            username="testuser2", password="testpassword2", email="test2@example.com"
        )

        self.signup_url = reverse('signup')  # Adjust based on your URL names
        self.signin_url = reverse('signin')
        self.home_url = reverse('home')
        self.get_user_data_url = reverse('get_user_data')
        self.get_all_user_data_url = reverse('get_all_user_data')
        self.send_request_url = reverse('send_request')
        self.request_contact_url = reverse('request_contact')
        self.chat_messages_url = reverse('chat_messages')

class UserTests(APITestSetup):

    def test_user_signup(self):
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "contact": "1234567890"
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_signin(self):
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_get_user_data(self):
        response = self.client.get(self.get_user_data_url, {"id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_get_all_user_data(self):
        response = self.client.get(self.get_all_user_data_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming only one non-superuser exists

class RequestTests(APITestSetup):

    def test_send_request(self):
        data = {
            "req_from": self.user.id,
            "req_to": self.user2.id
        }
        response = self.client.post(self.send_request_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_request(self):
        Request.objects.create(req_from=self.user, req_to=self.user2)
        data = {
            "req_from": self.user.id,
            "req_to": self.user2.id
        }
        response = self.client.post(self.send_request_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_request(self):
        req = Request.objects.create(req_from=self.user, req_to=self.user2)
        response = self.client.get(self.send_request_url, {"req_from": self.user.id, "req_to": self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], req.status)

    def test_get_request_contact(self):
        Request.objects.create(req_from=self.user, req_to=self.user2, status="send")
        response = self.client.get(self.request_contact_url, {"id": self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class ChatTests(APITestSetup):

    def test_send_message(self):
        data = {
            "from_user": self.user.id,
            "to_user": self.user2.id,
            "msg": "Hello!"
        }
        response = self.client.post(self.chat_messages_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_messages(self):
        ChatModel.objects.create(from_user=self.user, to_user=self.user2, msg="Hello!")
        response = self.client.get(self.chat_messages_url, {"from_user": self.user.id, "to_user": self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)

