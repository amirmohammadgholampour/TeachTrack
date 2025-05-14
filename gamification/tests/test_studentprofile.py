import pytest 
from rest_framework.test import APIClient 
from rest_framework import status 
from gamification.models import StudentProfile
from user.models import User 

@pytest.mark.django_db
class TestGetStudentProfileView:
    def test_if_user_unauthenticated_return_401(self):
        # Arrange 
        client = APIClient()

        # Act 
        response = client.get(
            "/gamification/student-profile/",
            {
                "username": "test_student1",
            }
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_usertype_is_not_student_or_admin_return_403(self):
        # Arrange 
        user = User.objects.create_user(
            username="test_teacher1",
            password="string1234",
            user_type="teacher",
            email="teacher@domain.com",
            phone_number="09309500547",
            national_code="0960031122" 
        )
        client = APIClient()
        client.force_authenticate(user=user)
        # Act 
        response = client.get(
            "/gamification/student-profile/"
        )

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_usertype_is_student_or_admin_return_200(self):
        # Arrange 
        user = User.objects.create_user(
            username="test_student1",
            password="string1234",
            user_type="student",
            email="student@domain.com",
            phone_number="09309500547",
            national_code="0960031122" 
        )
        client = APIClient()
        client.force_authenticate(user=user)

        # Act 
        response = client.get(
            "/gamification/student-profile/"
        )

        # Assert
        response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
class TestPostStudentProfileView:
    def test_if_usertype_is_not_admin_return_403(self):
        # Arrange 
        user = User.objects.create_user(
            username="test_student1",
            password="string1234",
            user_type="student",
            email="student@domain.com",
            phone_number="09309500547",
            national_code="0960031122" 
        )
        client = APIClient()
        client.force_authenticate(user=user)

        # Act 
        response = client.post(
            "/gamification/student-profile/",
        {
            "students": 2,
            "total_point": 50,
            "level": 5
        }
        )

        # Assert
        response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_usertype_is_admin_return_201(self):
        # Arrange 
        user = User.objects.create_user(
            username="test_admin1",
            password="admin1234",
            user_type="admin",
            email="admin@gmail.com",
            phone_number="09309500547",
            national_code="0960031122" 
        )
        client = APIClient()
        client.force_authenticate(user=user)

        # Act 
        response = client.post(
            "/gamification/student-profile/",
        {
            "students": 2,
            "total_point": 50,
            "level": 5
        }
        )

        # Assert
        response.status_code == status.HTTP_201_CREATED
    
    def test_if_user_enter_invalid_data_return_400(self):
        # Arrange 
        user = User.objects.create_user(
            username="test_admin1",
            password="admin1234",
            user_type="admin",
            email="admin@gmail.com",
            phone_number="09309500547",
            national_code="0960031122" 
        )
        client = APIClient()
        client.force_authenticate(user=user)

        # Act 
        response = client.post(
            "/gamification/student-profile/",
        {
            "students": 0,
            "total_point": 50,
            "level": 5
        }
        )

        # Assert
        response.status_code == status.HTTP_400_BAD_REQUEST
        