# project
# **Turf Booking API**
API Base URL: https://project1-otd3.onrender.com

Introduction
This API enables users to register, log in, and fetch information about available turfs, supporting a seamless turf booking system. It offers endpoints for user management and turf details, including location-based searches.

# API Endpoints
1. Default Route
Endpoint: /

Method: GET

Description: Returns a default response to confirm the API is running.

2. User Registration
Endpoint: /user

Method: POST

Description: Registers a new user.

Request Body Example:

json
Copy
Edit
{
  "username": "JohnDoe",
  "email": "john@example.com",
  "password": "securepassword"
}
3. User Login
Endpoint: /login

Method: POST

Description: Authenticates the user and returns login confirmation.

Request Body Example:

json
Copy
Edit
{
  "email": "john@example.com",
  "password": "securepassword"
}
4. Add a Turf
Endpoint: /turf

Method: POST

Description: Adds a new turf to the system.

Request Body Example:

json
Copy
Edit
{
  "turf_name": "Green Valley",
  "turf_city": "Chennai",
  "turf_latitude": "12.9716",
  "turf_longitude": "77.5946",
  ...
}
5. Get Turf by ID
Endpoint: /getturf/<int:id>

Method: GET

Description: Retrieves details of a specific turf by its ID.

6. Get Turf by Location
Endpoint: /getloc/<str:lat>/<str:long>

Method: GET

Description: Retrieves turfs based on latitude and longitude.

# 🧑‍💻 How to Use
Clone the repository:

  git clone <repo-url>
  cd <repo-directory>

Install dependencies:

  npm install

or for Django:

  pip install -r requirements.txt

Run the server:

  npm start

or for Django:

  python manage.py runserver


# Turf Model Fields
| Field Name           | Type    | Description                                            |
| -------------------- | ------- | ------------------------------------------------------ |
| `id`                 | Integer | Unique identifier for the turf                         |
| `turf_name`          | String  | Name of the turf                                       |
| `turf_address`       | String  | Address of the turf                                    |
| `turf_city`          | String  | City where the turf is located                         |
| `turf_state`         | String  | State where the turf is located                        |
| `turf_zip_code`      | String  | ZIP code of the turf                                   |
| `turf_latitude`      | Decimal | Latitude of the turf location                          |
| `turf_longitude`     | Decimal | Longitude of the turf location                         |
| `turf_type`          | String  | Type of turf (indoor/outdoor)                          |
| `surface_type`       | String  | Surface type of the turf                               |
| `size`               | String  | Turf size (e.g., 5-a-side, 7-a-side)                   |
| `capacity`           | Integer | Maximum player capacity                                |
| `status`             | Integer | Status indicator (1: Verified, 2: Blocked, 3: Pending) |
| `opening_time`       | Time    | Opening time of the turf                               |
| `closing_time`       | Time    | Closing time of the turf                               |
| `closed_days`        | String  | Days when the turf is closed                           |
| `hourly_rate`        | Decimal | Rate per hour for booking                              |
| `peak_hour_rate`     | Decimal | Special rate for peak hours (if applicable)            |
| `discount`           | Decimal | Discount percentage (if applicable)                    |
| `owner_name`         | String  | Name of the turf owner                                 |
| `turf_contact_phone` | String  | Contact phone number of the owner                      |
| `turf_contact_email` | String  | Contact email of the owner                             |
| `images`             | List    | List of image URLs for the turf                        |

# Conclusion
This API facilitates turf booking by offering endpoints for user registration, login, turf details retrieval, and location-based searches.

