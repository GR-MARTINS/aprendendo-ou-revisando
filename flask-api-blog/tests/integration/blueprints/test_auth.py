from http import HTTPStatus

def test_login_success(get_admin_access_token):
    response = get_admin_access_token
    assert response.status_code == HTTPStatus.OK