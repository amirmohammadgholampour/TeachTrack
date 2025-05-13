import pytest
from rest_framework.test import APIClient
from rest_framework import status
from user.models import User 

@pytest.mark.django_db
class TestCreateUserView:
    def test_if_valid_data_and_permission_return_201(self):
        # Arrange
        client = APIClient()

        # Act 
        response = client.post(
            "/users/create/",
            {
                "username": "test_student1",
                "password": "string1234",
                "email": "student@example.com",
                "user_type": "student",
                "phone_number": "09309500214",
                "national_code": "0960024455"
            },
            format='json' 
        )

        # Assert 
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data["data"]

    def test_if_user_already_authenticated_return_400(self):
        # Arrange 
        user = User.objects.create_user(
            username = "test_student1",
            password = "string1234",
            email = "student@example.com",
            user_type = "student",
            phone_number = "09309500214",
            national_code = "0960024455"
        )
        client = APIClient()
        client.login(
            username = "test_student1",
            password = "string1234"
        )

        # Act
        response = client.post(
            "/users/create/",
            {
                "username": "test_student1",
                "password": "string1234",
                "email": "student@example.com",
                "user_type": "student",
                "phone_number": "09309500214",
                "national_code": "0960024455"
            },
            format='json'
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.data or "error" in response.data
    
    def test_if_user_sending_invalid_data_return_400(self):
        # Arrange
        client = APIClient()

        # Act
        response = client.post(
            "/users/create/",
            {
                "username": "test_student1",
                "password": "string1234",
                "email": "student@example.com",
                "user_type": "student",
                "phone_number": "0930950214",
                "national_code": "096002455"
            },
            format='json'
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_password_of_admin_is_incorrect_return_403(self):
        # Arrange
        client = APIClient()

        # Act
        response = client.post(
            "/users/create/",
            {
                "username": "test_admin1",
                "password": "string1234",
                "email": "admin@example.com",
                "user_type": "admin",
                "phone_number": "09309500214",
                "national_code": "0960024455"
            },
            format='json' 
        )

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "detail" in response.data or "error" in response.data