import pytest
import requests

# Define the URL of your running Flask app
API_URL = "http://127.0.0.1:5000"  # Replace with your actual API URL


# Test case: Check if the API route to get users returns a 200 status code.
def test_retrieve_user_status_code():
    response = requests.get(f"{API_URL}/fetchuser")
    assert response.status_code == 200


# Test case: Check if the API route to get users returns JSON data.
def test_retrieve_user_json():
    response = requests.get(f"{API_URL}/fetchuser")
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type.lower()
    result = response.json()
    print("API Response Data:")
    print(result)


# Test case: Check if the API route to get users returns a list of users.
def test_retrieve_user_data():
    response = requests.get(f"{API_URL}/fetchuser")
    data = response.json()
    assert "test_records" in data
    assert isinstance(data["test_records"], list)
    result = response.json()
    print("API Response Data:")
    print(data)


# Define the URL of your running Flask app
API_URL = "http://127.0.0.1:5000"  # Replace with your actual API URL


# Test case: Check if the API route to create a user returns JSON data and print the data.
def test_create_user_json_and_print_data():
    # Create a new user (adjust the request as needed)
    new_user_data = {
        "user_id": "666",
        "name": "Avichal",
        "email":"avi@gmail.com",
        "age":"30",
        "address":"",
        "password":"123456",
        "confirm_password":"123456",
        "phone":"6578909878"
    }
    response = requests.post(f"{API_URL}/adduser", json=new_user_data)

    # Check if the status code is 200 OK or a suitable code for successful creation
    assert response.status_code in [200, 201]  # Adjust as per your API

    # Check if the Content-Type header indicates JSON data
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type.lower()

    # Print the JSON data for inspection
    data = response.json()
    print("Create User Response Data:")
    print(data)


# Test case: Check if the API route to update a user returns JSON data and print the data.
def test_update_user_json_and_print_data():
    # Update an existing user (adjust the request as needed)
    updated_user_data = {
        "user_id": "1234",
        "name": "Akash"
    }
    response = requests.put(f"{API_URL}/updateuser", json=updated_user_data)

    # Check if the status code is 200 OK or a suitable code for successful update
    assert response.status_code in [200, 204]  # Adjust as per your API

    # Check if the Content-Type header indicates JSON data
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type.lower()

    # Print the JSON data for inspection
    data = response.json()
    print("Update User Response Data:")
    print(data)


# Add more test cases as needed for other API routes and functionality.

if __name__ == "__main__":
    pytest.main()
