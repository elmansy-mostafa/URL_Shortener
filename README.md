# URL_Shortener (2024)

## Overview 

This project is a URL shortening service built using FastAPI, a modern, fast web framework for building APIs with Python. The service allows users to shorten long URLs into shorter, more manageable ones and provides endpoints to redirect, delete, and retrieve these URLs.

## Features 

1. URL Shortening:
   - Users can submit a long URL to be shortened.
   - The system generates a unique key for each URL using a SHA-256 hash and truncates it to 6 characters.
   - The shortened URL is stored in a database along with the original URL.

2. Redirection:
   - Users can navigate to the shortened URL, and the service will redirect them to the original long URL.
   - If the shortened URL key does not exist, the service returns a 404 error.

3. URL Deletion:
   - Users can delete a shortened URL by its unique key.
   - The system removes the corresponding URL record from the database.

4. Persistence and Database Management:
   - Uses SQLAlchemy for ORM (Object-Relational Mapping) and database management.
   - Ensures that database connections are properly managed during application startup and shutdown.

5. Error Handling:
   - Custom exception handling for HTTP errors, providing clear and concise error messages.

## API Endpoints

1. POST /shorten-url/:
   - Endpoint to shorten a long URL.
   - Accepts a JSON payload containing the long URL.
   - Returns the shortened URL along with its key.

2. GET /{key}:
   - Endpoint to redirect to the long URL using the shortened key.
   - Looks up the key in the database and redirects if found.
   - Returns a 404 error if the key does not exist.

3. DELETE /{key}:
   - Endpoint to delete a shortened URL by its key.
   - Removes the URL record from the database if found.
   - Returns a success message upon deletion.


## Project Setup and Dependencies

- FastAPI: For building the API.
- SQLAlchemy: For database interaction.
- Pydantic: For data validation.
- hashlib: For generating unique keys using SHA-256 hashing.

