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

4.  **Analytics Engine (Pandas / AI Engine):**
    - Integrated into the Flask backend.
    - Processes raw user data (e.g., browser history, app usage logs) to extract meaningful patterns.
    - **Session Detection Engine:** Uses a strategy pattern (currently `RuleBasedClassifier`) to group raw events into semantic sessions (e.g., "Deep Work", "Entertainment"). This is designed to be easily swappable with ML models in the future without changing the API contract.
    - **Productivity Scoring Engine:** Pipeline of sub-engines (Focus, Consistency, Discipline) that evaluate `BehaviorSession` groupings and output quantitative normalized scores (0-100). Includes an `InsightEngine` for generating NLP-like behavioral analysis.
    - **Habit Detection Engine:** Core behavioral reasoning layer that uses sequential pattern mining, threshold-based routine detection, and trigger analysis to automatically categorize and score user routines. Built to seamlessly integrate with future Sequence Models, Association Rule Mining, and Time Series Models.
    - **Behavior Correlation Engine:** Statistical layer designed to quantify the relationship between behavioral factors (e.g., Music, Session Length) and productivity outcomes (e.g., Focus, Consistency). Employs Pearson calculations to establish significance levels (p-value proxies) and acts as the causal reasoning foundation. The interface boundary is explicitly designed so `RelationshipAnalyzer` can be swapped from mathematical heuristics to ML Predictive Models (like Random Forests for feature importance) without altering downstream APIs.
    - **Procrastination Detection Engine:** The primary vulnerability assessment module. It detects distraction loops, focus disruption (via rapid context switching), and circadian dysfunction. Employs heuristics to estimate cognitive time lost and aggregates severity. Serves as the foundation for future behavioral interventions and AI coaching layers.
    - **Burnout Risk Engine:** The platform's first predictive intelligence layer. It aggregates data from all underlying engines to assess workload, recovery ratios, focus degradation, context switching, and volatility over a defined time window. Uses configurable weights (`burnout_config.py`) to output a unified Risk Score (0-100) and actionable recovery recommendations. Ready to ingest ML models for early intervention.
    - **Focus Prediction Engine:** Forecasts future high-focus windows and optimal productivity blocks based on historical behavioral patterns, sleep cycles, and daily routines. Uses chronotype analysis, fatigue adjustment, and historical day-of-week trends to identify optimal times. Designed to be easily upgraded from rolling averages to advanced Time Series Forecasting (ARIMA/Prophet).
    - **Behavioral Trajectory Engine:** Unifies macro-trend detection, dynamic goal tracking, and long-term consistency forecasting. Uses rolling 14-day and 30-day windows to detect macro shifts (e.g., chronotype shifting). Calculates dynamic required run-rates for active goals and models streak survival probabilities based on historical failure points. Caches 30-day aggregations to minimize database load. Exposes an API designed for tool-use by future AI Investigators. Designed to be easily upgraded from rolling averages to advanced Time Series Forecasting (ARIMA/Prophet).

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
