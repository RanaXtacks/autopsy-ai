# Initial GitHub Issues

This document outlines the first set of issues to be created in the repository to kickstart development.

## 1. Project Infrastructure
- **[Task] Setup Backend Boilerplate**
  - Initialize Flask app with blueprints.
  - Configure PostgreSQL connection using SQLAlchemy.
  - Set up basic error handling.
- **[Task] Setup Frontend Boilerplate**
  - Initialize React app using Vite.
  - Set up routing (React Router).
  - Add Tailwind CSS for styling.
- **[Task] Dockerize Application**
  - Create Dockerfiles for frontend and backend.
  - Create `docker-compose.yml` for local development.

## 2. Core Features
- **[Feature] User Authentication**
  - Implement JWT-based authentication.
  - Create Sign up / Login forms.
- **[Feature] Data Upload Interface**
  - Create a drag-and-drop component for file uploads (CSV/JSON).
  - Implement backend endpoint to receive and store files securely.
- **[Analytics] Basic Pandas Integration**
  - Create a service layer to process uploaded data using Pandas.
  - Implement a simple "Summary" view for uploaded data.

## 3. Privacy & Security
- **[Security] Data Encryption at Rest**
  - Implement encryption for sensitive database columns.
- **[Privacy] Data Anonymization Utility**
  - Create a utility to strip PII (Personally Identifiable Information) from data before processing.

## 4. Documentation
- **[Doc] API Documentation**
  - Set up Swagger/OpenAPI for Flask endpoints.
- **[Doc] Developer Setup Guide**
  - Detailed instructions for setting up the local environment without Docker.
