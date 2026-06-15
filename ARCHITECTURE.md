# Architecture Overview - Autopsy AI

## System Design

Autopsy AI follows a decoupled client-server architecture, optimized for scalability and privacy.

### Components

1.  **Frontend (React):**
    - A modern, responsive single-page application (SPA).
    - Responsible for data visualization and user interaction.
    - Uses Redux or Context API for state management.
    - Communicates with the backend via RESTful APIs.

2.  **Backend (Flask):**
    - Lightweight and scalable API service.
    - Handles authentication, data processing orchestration, and database interactions.
    - Uses Pandas for complex data analysis and behavioral pattern recognition.
    - Implements privacy-preserving algorithms (e.g., differential privacy where applicable).

3.  **Database (PostgreSQL):**
    - Relational database for storing user profiles, metadata, and processed insights.
    - Optimized for high-read/write performance.

4.  **Analytics Engine (Pandas):**
    - Integrated into the Flask backend.
    - Processes raw user data (e.g., browser history, app usage logs) to extract meaningful patterns.

## Data Flow

1.  User uploads or connects a data source via the **Frontend**.
2.  The **Backend** receives the data and performs initial sanitization.
3.  The **Analytics Engine** (Pandas) processes the data to identify behavior patterns.
4.  Results are stored in **PostgreSQL** and returned to the **Frontend** for visualization.
5.  All raw data is either discarded after processing or stored in an encrypted format.

## Security & Privacy

- **End-to-End Encryption:** Sensitive data is encrypted at rest and in transit.
- **Local Processing:** Option for users to run the analytics engine locally.
- **Data Minimization:** Only essential data is collected and processed.

## Infrastructure

- **Docker:** All components are containerized for consistent development and deployment environments.
- **Nginx (Production):** Acts as a reverse proxy and load balancer.
