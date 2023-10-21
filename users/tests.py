
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Scholar
from courses.models import *

# Create your tests here.
class UsersTestCase(TestCase):
    # Create User, Scholar objects
    def setUp(self): 
        user1 = User.objects.create_user(username="user1", password="password1")
        admin1 = User.objects.create_user(username="admin1", password="password1", is_staff=True)
        scholar1 = Scholar.objects.create(ID=user1, scholar_name="sname1", scholar_email="schl1@example.com")
        
    # Testing User Object String     
    def test_user_str(self): 
        sc1 = Scholar.objects.get(scholar_name="sname1")
        self.assertEqual(sc1.__str__(), "user1 : sname1")

    # Testiing User ID
    def test_user_id(self): 
        sc1 = Scholar.objects.get(scholar_name="sname1")
        self.assertEqual(sc1.get_id(), "user1")

    # Testing User name
    def test_get_name(self): 
        sc1 = Scholar.objects.get(scholar_name="sname1")
        self.assertEqual(sc1.get_name(), "sname1")

    # Testing User Email
    def test_get_email(self): 
        sc1 = Scholar.objects.get(scholar_name="sname1")
        self.assertEqual(sc1.get_email(), "schl1@example.com")

    # Testing Anonymous Login
    def test_anonymous_login(self): 
        c = Client()
        response = c.get(reverse('login_view'))
        self.assertEqual(response.status_code, 200)

    # Testing User Login
    def test_user_login(self): 
        c = Client()
        c.login(username="user1", password="password1")
        response = c.get(reverse('login_view'))
        self.assertEqual(response.status_code, 200)

    # Testing User Login Success 
    def test_user_login_success(self): 
        c = Client()
        response = c.post(reverse('login_view'), {'username':'user1', 'password':'password1'})
        self.assertEqual(response.status_code, 200)


    # Testing Admin Login
    def test_admin_login(self): 
        c = Client()
        c.login(username="admin1", password="password1")
        response = c.get(reverse('login_view'))
        self.assertEqual(response.status_code, 200)

    # Testing Admin Login Success
    def test_admin_login_success(self): 
        c = Client()
        response = c.post(reverse('login_view'), {'username':'admin1', 'password':'password1'})
        self.assertEqual(response.status_code, 200)

    # Testing Wrong Password Login
    def test_wrongpass_login(self): 
        c = Client()
        response = c.post(reverse('login_view'), {'username':'user1', 'password':'wrongpass'})
        self.assertEqual(response.status_code, 200)

    # Tesing Invalid Login
    def test_invalid_login(self): 
        c = Client()
        response = c.post(reverse('login_view'), {'username':'user1'})
        self.assertEqual(response.status_code, 200)

    # Testing Logout
    def test_logout(self): 
        c = Client()
        c.login(username="user1", password="password1")
        response = c.post(reverse('logout_view'))
        self.assertEqual(response.status_code, 302)