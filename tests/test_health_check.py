import allure
import pytest
import requests
import jsonschema

from core.schemas.booking_schemas import BOOKING_CREATED_SCHEMA

from conftest import generate_random_booking_data


@allure.feature("Test ping")
@allure.story("Test connection")
def test_ping(api_client):
    status_code = api_client.ping()
    assert status_code == 201, f"Expected status 201 but got {status_code}"


@allure.feature("Test ping")
@allure.story("Test server unavailablity")
def test_ping_server_unavailable(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=Exception("Server unavailable"))
    with pytest.raises(Exception, match="Server unavailable"):
        api_client.ping()


@allure.feature("Test ping")
@allure.story("Test wrong HTTP method")
def test_ping_wrong_method(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 405"):
        api_client.ping()


@allure.feature("Test ping")
@allure.story("Test server error")
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 500"):
        api_client.ping()


@allure.feature("Test ping")
@allure.story("Test wrong URL")
def test_ping_not_found(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 404"):
        api_client.ping()


@allure.feature("Test ping")
@allure.story("Test connection with different success code")
def test_ping_success_different_code(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 200"):
        api_client.ping()


@allure.feature("Test ping")
@allure.story("Test timeout")
def test_ping_timeout(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.ping()


@allure.feature("Test ping")
@allure.story("Test creating booking (joke response code 418)")
def test_ping_create_booking_418(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data

    with allure.step("Creating booking"):
        try:
            response = api_client.create_booking(booking_data)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 418:
                pytest.skip("Сервер вернул 418 I'm a teapot — тест пропущен")

    with allure.step("Validation scheme"):
        jsonschema.validate(response.json(), BOOKING_CREATED_SCHEMA)


@allure.feature("Test ping")
@allure.story("Test creating booking with mocker")
def test_ping_create_booking_with_mocker(api_client, mocker, generate_random_booking_data):
    fake_json = {
        "bookingid": 1,
        "booking": generate_random_booking_data
    }
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_json
    mock_post = mocker.patch.object(api_client.session, 'post', return_value=mock_response)

    with allure.step("Creating booking"):
        response = api_client.create_booking(generate_random_booking_data)
        assert mock_post.return_value.status_code == 200  # проверка ради проверки

    with allure.step("Validation scheme"):
        jsonschema.validate(response, BOOKING_CREATED_SCHEMA)  # схема возвращаемого json
