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
