
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User



User = get_user_model()
USER_NAME = 'user'
PWD    =     'something_in_password_#&^#(&*$#$4)'
EMAIL = 'example@email'
FNAME = 'John'
LNAME = 'Doe'


class CreateUserViewTest(TestCase):
 
    def setUp(self):
        user = User.objects.create_user(username=USER_NAME, password=PWD,email=EMAIL)
 

    def test_already_authenticated_signup(self):
        c = Client()
        #user already logged in
        user = authenticate(username=USER_NAME, password=PWD)
        c.login()

        # createUser is called
        response = c.get(reverse('create_user_view'))

        self.assertEqual(response.status_code, 200)

        # get logged out?
        self.assertEqual(c.session.get('_auth_user_id'), None)
    
    def test_createUserForm_valid(self):
        c = Client()

        #('username', 'first_name', 'last_name','email', 'password1', 'password2')
        form_data = {
            'username': USER_NAME,
            'first_name':FNAME,
            'last_name':LNAME,
            'email':EMAIL,
            'password1': PWD,
            'password2': PWD,
        }

        response = c.post(reverse('create_user_view'),form_data,follow=True)

        # Redirect ot user_page?
        self.assertEqual(response.status_code, 200)

        # New user created?
        self.assertTrue(User.objects.filter(username=USER_NAME).exists())

        # Try login new user
        user = authenticate(username=USER_NAME, password=PWD)

        # user is loged in?
        self.assertIsNotNone(user)
        self.assertEqual(user.is_authenticated,True)
        

