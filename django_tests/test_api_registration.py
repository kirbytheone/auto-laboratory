import pytest
from accounts.api.serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
def test_reg_serializer_normalizes_email():
    serializer = UserRegistrationSerializer(
        data={
            "username": "User",
            "email": "User@Example.COM",
            "password": "StrongPassword123!",
            "password_confirmation": "StrongPassword123!",
        }
    )

    serializer.is_valid(raise_exception=True)
    assert serializer.validated_data['email'] == 'user@example.com'

@pytest.mark.django_db
def test_reg_serializer_rejects_duplicate_email_case_insensitively(create_user):
    create_user(
        username='existing_user',
        email='User@Example.com',
        password='StrongPassword123!',
    )
    serializer = UserRegistrationSerializer(
        data={
            'username': 'new_user',
            'email': 'user@example.com',
            'password': 'StrongPassword123!',
            'password_confirmation': 'StrongPassword123!',
        }
    )

    assert serializer.is_valid() is False
    assert 'email' in serializer.errors

@pytest.mark.django_db
def test_reg_serializer_accepts_matching_passwords():
    serializer = UserRegistrationSerializer(
        data={
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'StrongPassword123!',
            'password_confirmation': 'StrongPassword123!',
        }
    )

    assert serializer.is_valid() is True

@pytest.mark.django_db
def test_reg_serializer_rejects_password_mismatch():
    serializer = UserRegistrationSerializer(
        data={
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'StrongPassword123!',
            'password_confirmation': 'DifferentPassword123!',
        }
    )

    assert serializer.is_valid() is False
    assert 'password_confirmation' in serializer.errors
    assert User.objects.filter(username="new_user").exists() is False

@pytest.mark.django_db
def test_reg_serializer_rejects_weak_password():
    serializer = UserRegistrationSerializer(
        data={
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'password',
            'password_confirmation': 'password',
        }
    )

    assert serializer.is_valid() is False
    assert 'password' in serializer.errors
    assert User.objects.filter(username="new_user").exists() is False

@pytest.mark.django_db
def test_reg_serializer_creates_user_with_hashed_password():
    serializer = UserRegistrationSerializer(
        data={
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'StrongPassword123!',
            'password_confirmation': 'StrongPassword123!',
        }
    )
    
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    
    assert user.username == 'new_user'
    assert user.email == 'new_user@example.com'
    assert user.check_password('StrongPassword123!') is True
    
@pytest.mark.django_db
def test_reg_serializer_does_not_expose_password_fields():
    serializer = UserRegistrationSerializer(
        data={
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "StrongPassword123!",
            "password_confirmation": "StrongPassword123!",
        }
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    assert 'password' not in serializer.data
    assert 'password_confirmation' not in serializer.data

@pytest.mark.django_db
def test_user_can_register_via_api(api_client):
    response = api_client.post(
        reverse('api-register'),
        {
            'username': 'api_user',
            'email': 'api_user@example.com',
            'password': 'StrongPassword123!',
            'password_confirmation': 'StrongPassword123!',
        },
        format='json',
    )

    assert response.status_code == 201
    assert response.data['username'] == 'api_user'
    assert response.data['email'] == 'api_user@example.com'
    assert 'password' not in response.data
    assert 'password_confirmation' not in response.data

@pytest.mark.django_db
def test_api_registration_rejects_duplicate_username(api_client, create_user):
    create_user(
        username='existing_user',
        email='existing@example.com',
        password='StrongPassword123!',
    )
    
    response = api_client.post(
        reverse('api-register'),
        {
            'username': 'existing_user',
            'email': 'new@example.com',
            'password': 'StrongPassword123!',
            'password_confirmation': 'StrongPassword123!',
        },
        fromat='json',
    )
    
    assert response.status_code == 400
    assert 'username' in response.data
    
@pytest.mark.django_db
def test_api_registration_rejects_duplicate_email_case_insensitively(api_client, create_user):
    create_user(
        username="existing_user",
        email="User@Example.com",
        password="StrongPassword123!",
    )

    response = api_client.post(
        reverse('api-register'),
        {
            'username': 'new_user',
            'email': 'user@example.com',
            'password': 'StrongPassword123!',
            'password_confirmation': 'StrongPassword123!',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'email' in response.data
    assert User.objects.filter(username="new_user").exists() is False

@pytest.mark.django_db
def test_api_registration_rejects_password_mismatch(api_client):
    response = api_client.post(
        reverse('api-register'),
        {
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'StrongPassword123!',
            'password_confirmation': 'DifferentPassword123!'
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'password_confirmation' in response.data
    assert User.objects.filter(username="new_user").exists() is False

@pytest.mark.django_db
def test_api_registration_rejects_weak_password(api_client):
    response = api_client.post(
        reverse('api-register'),
        {
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'password',
            'password_confirmation': 'password',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'password' in response.data
    assert User.objects.filter(username="new_user").exists() is False

@pytest.mark.django_db
def test_api_registration_rejects_invalid_email(api_client):
    response = api_client.post(
        reverse('api-register'),
        {
            'username': 'new_user',
            'email': 'not-an-email',
            'password': 'StrongPassword123!',
            'password_confirmation': 'StrongPassword123!',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'email' in response.data
    assert User.objects.filter(username="new_user").exists() is False

@pytest.mark.django_db
def test_api_registration_rejects_missing_required_fields(api_client):
    response = api_client.post(
        reverse('api-register'),
        {
            'username': 'new_user',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'email' in response.data
    assert 'password' in response.data
    assert 'password_confirmation' in response.data
    assert User.objects.filter(username="new_user").exists() is False

@pytest.mark.django_db
def test_register_user_can_obtain_jwt_and_access_task_api(api_client):
    register_response = api_client.post(
        reverse('api-register'),
        {
            'username': 'jwt_user',
            'email': 'jwt_user@example.com',
            'password': 'StrongPassword123!',
            'password_confirmation': 'StrongPassword123!',
        },
        format='json',
    )

    assert register_response.status_code == 201

    token_response = api_client.post(
        reverse('token_obtain_pair'),
        {
            'username': 'jwt_user',
            'password': 'StrongPassword123!',
        },
        format='json',
    )

    assert token_response.status_code == 200
    assert 'access' in token_response.data
    assert 'refresh' in token_response.data

    access_token = token_response.data['access']

    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {access_token}'
    )
    response = api_client.get(
        reverse('api-task-list')
    )

    assert response.status_code == 200




























