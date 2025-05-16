import pytest
from rest_framework.test import APIClient 
from rest_framework import status
from user.models import User 

@pytest.mark.django_db
class TestGetAttendanceApprovalView:
    def test_if_not_user_authenticated_return_401(self):
        # Arrange 
        client = APIClient()

        # Act 
        response = client.get(
            "/attending/approval/",
            {
                "status":"absent"
            }
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED 
    
    def test_if_usertype_of_user_is_not_admin_or_teacher_return_403(self):
        # Arrange 
        user = User.objects.create_user(
            username="test_student1",
            password="student1234",
            email="student@email.com",
            phone_number="09309540543",
            national_code="0950054422",
            user_type="student"
        )
        client = APIClient()
        client.force_authenticate(user=user)

        # Act 
        response = client.get(
            "/attending/approval/",
        )

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_usertype_is_admin_or_teacher_return_200(self):
        # Arrange 
        user = User.objects.create_user(
            username="test_teacher1",
            password="teacher1234",
            email="teacher@email.com",
            phone_number="09309540543",
            national_code="0950054422",
            user_type="teacher"
        )
        client = APIClient()
        client.force_authenticate(user=user)

        # Act 
        response = client.get(
            "/attending/approval/",
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK

