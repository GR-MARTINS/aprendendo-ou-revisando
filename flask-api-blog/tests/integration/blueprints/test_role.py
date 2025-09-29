from http import HTTPStatus

def test_create_role_success(create_admin_role):
    response = create_admin_role
    assert response.json == {"message": "role created"}
    assert response.status_code == HTTPStatus.CREATED