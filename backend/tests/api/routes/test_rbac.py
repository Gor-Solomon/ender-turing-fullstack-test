from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models import User, UserCreate
from app import crud
from tests.utils.user import authentication_token_from_email
from tests.utils.utils import random_email, random_lower_string

def test_admin_can_create_user(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # Superuser is admin by default
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password, "role": "member"}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    created_user = r.json()
    assert created_user["email"] == username

def test_member_cannot_list_users(
    client: TestClient, db: Session
) -> None:
    # Create a member user
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password, role="member")
    crud.create_user(session=db, user_create=user_in)
    
    headers = authentication_token_from_email(
        client=client, email=username, db=db
    )
    
    r = client.get(
        f"{settings.API_V1_STR}/users/",
        headers=headers,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "The user doesn't have enough privileges"

def test_member_cannot_view_metrics(
    client: TestClient, db: Session
) -> None:
    # Create a member user
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password, role="member")
    crud.create_user(session=db, user_create=user_in)
    
    headers = authentication_token_from_email(
        client=client, email=username, db=db
    )
    
    r = client.get(
        f"{settings.API_V1_STR}/metrics/",
        headers=headers,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "The user doesn't have enough privileges"
