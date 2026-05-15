from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.core.config import settings
from app.models import UserCreate
from tests.utils.user import authentication_token_from_email
from tests.utils.utils import random_email, random_lower_string

def test_admin_can_create_user(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password, "role": "member", "is_active": True}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    assert r.json()["email"] == username

def test_manager_cannot_create_user(
    client: TestClient, db: Session
) -> None:
    # 1. Create a manager
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password, role="manager", is_active=True)
    crud.create_user(session=db, user_create=user_in)
    
    # 2. Get their token
    headers = authentication_token_from_email(client=client, email=username, db=db)
    
    # 3. Verify they get a 403 Forbidden when trying to create a user
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=headers,
        json={"email": random_email(), "password": random_lower_string()},
    )
    assert r.status_code == 403

def test_member_cannot_list_users(
    client: TestClient, db: Session
) -> None:
    # 1. Create a member
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password, role="member", is_active=True)
    crud.create_user(session=db, user_create=user_in)
    
    # 2. Get their token
    headers = authentication_token_from_email(client=client, email=username, db=db)
    
    # 3. Verify they get a 403 Forbidden when trying to list users
    r = client.get(
        f"{settings.API_V1_STR}/users/",
        headers=headers,
    )
    assert r.status_code == 403