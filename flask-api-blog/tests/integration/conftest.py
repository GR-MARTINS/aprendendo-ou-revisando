import pytest
from src.app import create_app, db
from src.models.user import User
from src.models.role import Role


# scope='funcion' or 'module' or 'class' or 'package' or 'session'
# default scope='function'
@pytest.fixture()
def app():
    app = create_app(environment="testing")

    # other setup can go here
    with app.app_context():
        db.create_all()

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.rollback()
        db.drop_all()


@pytest.fixture()
def create_admin_role(client):
    payload = {"name": "admin"}
    response = client.post("/roles/", json=payload)
    return response


@pytest.fixture()
def create_default_role(client):
    payload = {"name": "default"}
    response = client.post("/roles/", json=payload)
    return response


@pytest.fixture()
def get_admin_role(db_session, create_admin_role):
    create_admin_role
    query = db.select(Role).where(Role.name == "admin")
    role = db_session.execute(query).scalar()
    return role


@pytest.fixture()
def get_default_role(db_session, create_default_role):
    create_default_role
    query = db.select(Role).where(Role.name == "default")
    role = db_session.execute(query).scalar()
    return role


@pytest.fixture()
def create_admin_user(client, get_admin_role):
    role = get_admin_role
    payload = {
        "first_name": "Naruto",
        "last_name": "Uzumaki",
        "username": "uzumaki_naruto",
        "email": "email@email.com",
        "password": "1234",
        "date_of_birth": "1995-11-26",
        "role_id": role.id,
        "gender": "male",
    }

    response = client.post("/users/", json=payload)
    return response

@pytest.fixture()
def create_default_user(client, get_default_role):
    role = get_default_role
    payload = {
        "first_name": "Boruto",
        "last_name": "Uzumaki",
        "username": "uzumaki_boruto",
        "email": "email@email.com",
        "password": "1234",
        "date_of_birth": "1995-11-26",
        "role_id": role.id,
        "gender": "male",
    }

    response = client.post("/users/", json=payload)
    return response

@pytest.fixture()
def get_admin_user(db_session, create_admin_user):
    create_admin_user
    query = db.select(User).where(User.username == "uzumaki_naruto")
    user = db_session.execute(query).scalar()
    return user

@pytest.fixture()
def get_default_user(db_session, create_default_user):
    create_default_user
    query = db.select(User).where(User.username == "uzumaki_boruto")
    user = db_session.execute(query).scalar()
    return user

@pytest.fixture()
def get_admin_access_token(client, get_admin_user):
    user = get_admin_user

    payload = {
        "username": user.username,
        "password": "1234"
    }

    response = client.post("/auth/login", json=payload)

    return response