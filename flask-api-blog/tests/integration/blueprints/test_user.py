from http import HTTPStatus


def test_create_user_success(create_admin_user):
    response = create_admin_user
    assert response.json == {"message": "user created"}
    assert response.status_code == HTTPStatus.CREATED
