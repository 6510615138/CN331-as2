from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse 
from django.contrib.auth.models import User
from django.db.models import Max
from .models import Course, Register
from users.models import Scholar

# Create your tests here.
class CoursesTestCase(TestCase):
    # Create Course, User, Scholar, Register objects
    def setUp(self): 
        course1 = Course.objects.create(ID="CN330", course_name="Computer Application Developments", course_lecturer="-", course_des="-", course_seat=2)
        course2 = Course.objects.create(ID="CN331", course_name="Software Engineering", course_lecturer="-", course_des="-", course_seat=1)

        user1 = User.objects.create_user(username="user1", password="password1")
        user2 = User.objects.create_user(username="user2", password="password2")
        admin = User.objects.create_user(username="admin1", password="password1", is_staff=True)

        scholar1 = Scholar.objects.create(ID=user1, scholar_name="sname1", scholar_email="schl1@example.com")
        scholar2 = Scholar.objects.create(ID=user2, scholar_name="sname2", scholar_email="schl2@example.com")

        course1.course_seat -= 1
        course1.course_status = False 
        register1 = Register.objects.create(reg_scholar_id = user1, reg_course_id = course1)


    # For Course
    # Testing Course Object String 
    def test_course_str(self): 
        test_course = Course.objects.get(course_name="Computer Application Developments")
        self.assertEqual(str(test_course), f'{test_course.ID} : {test_course.course_name} Seat :{test_course.course_seat}' )

    # # Testing Invalid Subject Page 
    # def test_invalid_subject_page(self):
    #     id_max = Course.objects.all().aggregate(Max("ID"))['ID']
    #     c = Client()
    #     response = c.get(reverse('course_page', args=(id_max+1,)))
    #     self.assertEqual(response.status_code, 404)

    # For User
    # Testing Index
    def test_index_page(self): 
        c = Client()
        c.login(username="user1", password="password1")
        response = c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    # Testing User Page
    def test_user_page(self):
        c = Client()
        c.login(username="user1", password="password1")
        response = c.get(reverse('user_page'))
        self.assertEqual(response.status_code, 200)

    # Testing Request Quota
    def test_course_request_quota(self):
        c = Client()
        c.login(username="user2", password="password2")
        response = c.post(reverse('request_quota'), {"reg_course_id" : "CN330"})
        self.assertEqual(response.status_code, 200)

    # Testing Cancel Quota
    def test_course_cancel_quota(self): 
        c = Client()
        c.login(username="user1", password="password1")
        response = c.post(reverse('cancel_quota'), {"reg_scholar_id" : "user1", "reg_course_id" : "CN330"})
        self.assertEqual(response.status_code, 200)

    # Testing Board Page
    def test_board_page(self): 
        c = Client()
        c.login(username="user2", password="password2")
        response = c.get(reverse('board_page'))
        self.assertEqual(response.status_code, 200)

    # For Admin 
    # Testing Admin User Page
    def test_admin_user_page(self): 
        c = Client()
        c.login(username="admin1", password="password1")
        response = c.get(reverse('user_page'))
        self.assertEqual(response.status_code, 200)

    # Testing Admin Course Page
    def test_admin_course_page(self): 
        c = Client()
        c.login(username="admin1", password="password1")
        response = c.get(reverse('course_page'))
        self.assertEqual(response.status_code, 200)

    # Testing Admin Management Page
    def test_admin_management_page(self): 
        c = Client()
        c.login(username="admin1", password="password1")
        response = c.get(reverse('management'))
        self.assertEqual(response.status_code, 200)