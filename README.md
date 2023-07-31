# Respiratory Imbalance Predictor Backend API

This is the backend API for the Respiratory Imbalance Predictor web application. The API is built using Flask and is responsible for handling user login, registration, prediction, and retrieving past data. It is currently hosted on Render at [https://respiratory-backend.onrender.com](https://respiratory-backend.onrender.com).

## Getting Started

The backend API is already hosted on Render, and you can access it using the following base URL: [https://respiratory-backend.onrender.com](https://respiratory-backend.onrender.com)

To interact with the backend API, you need to use the frontend React.js project, which is available on GitHub: [https://github.com/JosephSamuel2022/Respiratory-Imbalance-Front-End](https://github.com/JosephSamuel2022/Respiratory-Imbalance-Front-End)

The React.js project communicates with this backend API to handle user interactions and display the predicted respiratory imbalance.

## API Endpoints

The following endpoints are available:

- `POST /api/login`: Handles user login. Expects `pid` (Patient ID) and `password` in the request payload.

- `POST /api/signup`: Handles user registration. Expects `pid`, `dob`, `gender`, `password`, and `name` in the request payload.

- `POST /api/predict`: Makes predictions for respiratory imbalance based on user inputs. Expects various health parameters in the request payload.

- `POST /api/pastdata`: Retrieves past medical data for a specific user. Expects `patientId` in the request payload.

- `POST /api/info`: Retrieves basic information about a specific user. Expects `pid` (Patient ID) in the request payload.

- `POST /api/forgot`: Allows users to reset their password if they have forgotten it. Expects `patientId`, `dob`, and `newPassword` in the request payload.

## Technology Stack

- Flask: A micro web framework for building web applications.
- MongoDB: A NoSQL database used to store user data and medical history.
- Flask-CORS: A Flask extension to handle Cross-Origin Resource Sharing.
- Matplotlib: A library for creating interactive visualizations and plots.

## Deployment

The backend API is deployed on Render, which provides a secure and scalable hosting platform for web applications. To deploy updates to the backend, you can push changes to the main branch of this repository. Render will automatically build and deploy the updated version.

## Contact

For any inquiries or support, please contact [josephsamuelm2021@gmail.com](mailto:josephsamuelm2021@gmail.com).
