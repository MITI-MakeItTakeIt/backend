from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.

class UserInfoCheckAPITest(APITestCase):
    def setUp(self):
        get_user_model().objects.create(
            email="TestUser@Testuser.com",
            nickname="Testuser",
            password="Testuser1234#"
        )
    
    def test_givenNonexistingUserEmail_whenCheckUserInfo_thenReturn200(self):
        # given
        url = reverse('user-info-check') + "?type=checkEmail&key=nonExistingEmail@user.com"
        
        # when
        response = self.client.get(url, format='json')
        response_data = response.json()
        
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('is_available', response_data['data'])
        self.assertEqual(1, response_data['data']['is_available'])
        self.assertIn('message', response_data['data'])
        self.assertEqual("사용 가능한 이메일입니다.", response_data['data']['message'])
    
    def test_givenNonexistingUserNickname_whenCheckUserInfo_thenReturn200(self):
        # given
        url = reverse('user-info-check') + "?type=checkNickname&key=nonExistingNickname"

        # when
        response = self.client.get(url, format='json')
        
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('is_available', response_data['data'])
        self.assertEqual(1, response_data['data']['is_available'])
        self.assertIn('message', response_data['data'])
        self.assertEqual("사용 가능한 닉네임입니다.", response_data['data']['message'])

    def test_givenExistingEmail_whenCheckUserInfo_thenReturn200(self):
        # given
        url = reverse('user-info-check') + "?type=checkEmail&key=TestUser@Testuser.com"
        
        # when
        response = self.client.get(url, format='json')
        response_data = response.json()
        
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('is_available', response_data['data'])
        self.assertEqual(0, response_data['data']['is_available'])
        self.assertIn('message', response_data['data'])
        self.assertEqual("사용중인 닉네임입니다.", response_data['data']['message'])
        # when
        
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
