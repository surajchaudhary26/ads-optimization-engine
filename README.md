## 1. Business Problem (Ads Optimization)

### Context
Advertising platforms operate under fixed budgets while running multiple ads simultaneously.  
As the number of candidate ads increases, manually deciding which ads should run becomes inefficient and unreliable.

---

### Problem Statement
Given a fixed advertising budget and a set of candidate ads with different costs, priorities, and expected performance, the system must automatically select the optimal subset of ads that maximizes expected business value while respecting budget, latency, and safety constraints.

---

### Decision Scope
- Decides which ads should be selected and how the budget should be allocated
- Does not handle ad creation, creative design, or audience targeting

---

### Success Metrics
- Total conversion value
- Budget utilization efficiency
- End-to-end decision latency
- Potential A/B uplift

---

### Constraints
- Budget must never be exceeded
- System must remain stateless and low-latency
- Invalid or unsafe inputs must be handled gracefully

---

## 2. Decision Definition & API Behavior

### Decision
At any given request, the system decides which ads should be selected based on the provided ads and total budget.

---

### Input
- `ads`: List of ads containing `ad_id`, `cost`, and business attributes
- `total_budget`: Maximum budget allowed for selection

---

### Output
- `selected_ads`: Ads chosen by the system
- `total_cost`: Budget consumed by the selected ads

---

### Behavior
- Missing required inputs → returns a clear validation error
- Invalid inputs → returns a safe, structured error response
- No ad fits within the budget → returns an empty selection (not treated as an error)

---

## 3. Core Decision Logic (Phase 3)

This phase establishes a stable and ML-independent inference pipeline using clean, modular Python code.

---

### Components Implemented

#### Input Validation
- Ensures presence and correctness of ads and budget
- Prevents invalid data from reaching decision logic

#### Rule-Based Optimization (Baseline)
- Uses a deterministic greedy selection approach
- Guarantees correctness and safety under budget constraints

#### Decision Service (Orchestration Layer)
- Combines validation and optimization into a single flow
- Returns structured responses for both success and failure cases

---

### Outcome
At the end of this phase, the system can:
- Safely accept inputs
- Handle edge cases gracefully
- Produce correct ad-selection decisions without ML or APIs

This phase establishes a solid foundation for API exposure and ML integration.

---

## 4. API Layer (Phase 4)

In this phase, the core decision engine is exposed via a thin FastAPI layer.

---

### API Endpoint
- `POST /decide-ads`
  - Accepts ads and total budget
  - Returns selected ads and total cost

---

### Design Principles
- API layer contains no business or optimization logic
- All decisions are delegated to the service layer
- Clean HTTP semantics:
  - `200 OK` for valid decisions
  - `400 Bad Request` for invalid inputs

---

### Outcome
The system becomes:
- Client-agnostic
- Easily integrable with any frontend or backend
- Cleanly separated between interface and decision logic

---

## 5. Logic+ Improvements (Phase 5)

Before introducing machine learning, the rule-based optimizer was enhanced to improve decision quality.

---

### Enhancements
- Ads are sorted by business priority (high to low)
- Within the same priority, ads are sorted by cost (low to high)
- Maintains deterministic and fully explainable behavior

---

### Outcome
The system produces higher-quality, business-aligned decisions while remaining fast, simple, and predictable.

---

## 6. Machine Learning Training Pipeline (Phase 6)

A separate offline training pipeline was introduced to learn patterns from historical ad performance data.

---

### Objective
To build a reproducible and modular ML training pipeline without impacting live inference.

---

### Key Design Principles
- Training and inference are strictly separated
- Feature engineering logic is shared
- ML artifacts are treated as runtime outputs, not source code

---

### Training Pipeline Structure

training/
├── steps/
│ ├── train_model.py
│ ├── evaluate_model.py
│ └── save_model.py
├── pipeline/
│ └── run_training_pipeline.py



---

### Workflow
1. Historical ad performance data is generated
2. Features are engineered consistently
3. Model is trained and evaluated
4. A trained model artifact is produced locally

---

### Notes
- The trained model file (`value_model.pkl`) is excluded from version control
- The pipeline can be re-run at any time to regenerate artifacts

This phase establishes a production-aligned ML foundation.

---

## 7. Hybrid ML Inference System (Phase 7)

In this phase, machine learning is integrated into the inference system using a hybrid optimization strategy.

---

### Core Idea
Machine learning assists decision-making, while business rules retain final control.

---

### Optimizer Versions

#### Optimizer v1 – Rule-Based
- Fully deterministic and explainable
- Acts as a safe fallback mechanism

#### Optimizer v2 – Hybrid ML
- ML model predicts a value score for each ad
- ML score is combined with business signals such as:
  - ad priority
  - cost penalty
- Produces a final hybrid ranking score

---

### Decision Service (Central Control Layer)
Responsible for:
- Validating incoming requests
- Selecting the optimizer version
- Keeping the API layer independent of optimization logic

This enables safe ML rollout, rollback, and future A/B testing.

---

### Hybrid Scoring Logic (Conceptual)

final_score = (ML_score × weight) + priority_influence − cost_penalty


Machine learning provides adaptability, while business rules ensure stability and explainability.

---

## 8. API Request Schema (Pydantic)

The API uses Pydantic schemas to define a strict and explicit request contract.

---

### Design Principle
The API accepts only raw business inputs.

Included:
- cost
- priority
- clicks
- conversions

Excluded:
- conversion_rate
- ML-engineered features
- derived metrics

This ensures loose coupling between clients and ML logic and allows feature evolution without breaking API contracts.

---

## 9. Documentation & Testing

### Swagger UI
- Interactive API documentation available at `/docs`
- Allows testing endpoints directly from the browser
- Displays request and response schemas automatically

### OpenAPI
- FastAPI automatically generates an OpenAPI specification
- Acts as a formal contract for API consumers and tooling

---

## 10. Networking Basics

- Communication happens over HTTP
- `POST` is used for data-heavy decision requests
- Timeouts prevent clients from waiting indefinitely
- Proper error handling ensures predictable and safe failures

---

## Dockerized Deployment

The inference service is fully containerized using Docker to ensure consistent behavior across environments.

---

### Docker Image
The production-ready image is available on Docker Hub:

ersurajkr/ads-optimization-engine:latest

---

### Run Using Docker
```bash
docker pull ersurajkr/ads-optimization-engine:latest
docker run -p 8000:8000 ersurajkr/ads-optimization-engine:latest

Live Demo (Cloud Deployment)

The application is deployed on Render using the same Docker image.

Live Swagger UI:
https://ads-optimization-engine-latest.onrender.com

This demonstrates a production-ready, stateless ML inference API running in the cloud.

### Final Note

This project is intentionally designed as a decision system rather than just an ML model.
It emphasizes system design, safety, explainability, scalability, and production readiness.