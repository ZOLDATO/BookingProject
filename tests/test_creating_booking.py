import allure
import pytest
import jsonschema
from requests.exceptions import HTTPError
from pydantic import ValidationError
from core.schemas.booking_schemas import BOOKING_CREATED_SCHEMA

from conftest import generate_random_booking_data
from core.models.booking import BookingResponse


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
    booking_data['first_name'] = booking_data.pop('firstname')  # changing key to wrong key

    with pytest.raises(HTTPError) as except_data:
        api_client.create_booking(booking_data)

    assert except_data.value.response.status_code == 500, "The server did not return a 500 error"


@allure.feature("Test creating booking")
@allure.story("Creating booking and validation response by pydantic")
def test_create_booking_validation_by_pydantic(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response["booking"] == booking_data, "Booking details in request and response do not match"


@allure.feature("Test creating booking")
@allure.story("Creating booking with various parameters - positive tests")
@pytest.mark.parametrize(
    "test_param",
    [
        {"fields": {"totalprice": 1}},  # Positive test - minimal price
        {"fields": {"totalprice": 99999999}},  # Positive test - big price
        {"fields": {"depositpaid": True}},  # Positive test
        {"fields": {"depositpaid": False}},  # Positive test
        {"fields": {"bookingdates": {"checkin": "2025-10-01", "checkout": "2025-10-01"}}},  # Positive test - one day
        {"fields": {"bookingdates": {"checkin": "2025-10-01", "checkout": "2028-06-27"}}},  # Positive test - 1000 days
    ]
)
def test_create_booking_with_valid_parameters(test_param, api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    for key, value in test_param["fields"].items():
        booking_data[key] = value  # changing value

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response["booking"] == booking_data, "Booking details in request and response do not match"


@allure.feature("Test creating booking")
@allure.story("Creating booking with various parameters - negative tests")
@pytest.mark.parametrize(
    "test_param",
    [
        {"fields": {"firstname": 777}},  # Negative test - wrong type of value
        {"fields": {"lastname": 777}},  # Negative test - wrong type of value
        {"fields": {"firstname": 777, "lastname": 777}},  # Negative test - wrong type of value
    ]
)
def test_create_booking_with_wrong_parameters(test_param, api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    for key, value in test_param["fields"].items():
        booking_data[key] = value  # changing value

    with pytest.raises(HTTPError) as except_data:
        response = api_client.create_booking(booking_data)
        print()

    assert except_data.value.response.status_code == 500, "The server did not return a 500 error"
