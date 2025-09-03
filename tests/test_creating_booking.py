import allure
import requests
import jsonschema

from core.schemas.booking_schemas import BOOKING_CREATED_SCHEMA

from conftest import generate_random_booking_data, booking_dates


@allure.feature("Test creating booking")
@allure.story("Positive test creating booking")
def test_create_booking(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    response = api_client.create_booking(generate_random_booking_data)
    assert response["booking"] == booking_data, "Booking details in request and response do not match"
    jsonschema.validate(response, BOOKING_CREATED_SCHEMA)


@allure.feature("Test creating booking")
@allure.story("Creating booking with wrong request json")
def test_create_booking_wrong_json(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    booking_data['first_name'] = booking_data.pop('firstname') # changing key to wrong key

    try:
        api_client.create_booking(booking_data)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 500, "The server did not return a 500 error"
