## 1. Business Problem (Ads Optimization)

### Context
Advertising platforms operate under fixed budgets and must select the most valuable ads from a large candidate pool in real time.

### Problem Statement
Given a fixed advertising budget and a set of candidate ads with costs, priorities, and expected performance, the system automatically selects the optimal subset of ads that maximizes expected conversion value while respecting budget and latency constraints.

### Decision Scope
- Decides which ads to select and how to allocate budget.
- Does not handle ad creation or audience targeting.

### Success Metrics
- Total conversion value
- Budget utilization
- End-to-end latency
- A/B uplift

### Constraints
- Must not exceed budget
- Must be stateless and low-latency
- Must handle invalid inputs safely


## 2. Decision Definition & API Behavior

### Decision
The system decides which ads should be selected at a given moment based on the provided ads and total budget.

### Input
- `ads`: List of ads with `ad_id` and `cost`
- `total_budget`: Maximum budget allowed

### Output
- `selected_ads`: Ads chosen by the system
- `total_cost`: Budget used by selected ads

### Behavior
- If required inputs are missing → return a clear error message
- If inputs are invalid → return a safe error
- If no ad fits the budget → return an empty selection (not an error)

## 3. Core Decision Logic (Phase 3)

This phase implements the core inference pipeline of the system using clean, modular Python code.

### Components Implemented

- **Input Validation**
  - Validates presence and correctness of ads and budget
  - Prevents invalid or unsafe inputs from reaching decision logic

- **Rule-Based Optimization (Baseline)**
  - Selects ads within the given budget using a deterministic greedy approach
  - Serves as a baseline before introducing ML-based optimization

- **Decision Service (Orchestration Layer)**
  - Combines validation and optimization into a single decision flow
  - Returns safe, structured responses for both valid and error cases

### Outcome

At the end of this phase, the system can:
- Safely accept inputs
- Handle edge cases gracefully
- Produce correct ad-selection decisions without ML or APIs

This establishes a stable foundation for API integration and ML-based optimization in later phases.

## 4. API Layer (Phase 4)

In this phase, the core decision engine was exposed via a thin FastAPI layer to make the system usable by external services.

### API Endpoint

- **POST `/decide-ads`**
  - Accepts a list of ads and a total budget
  - Returns selected ads and total cost used

### Design Principles

- The API layer contains no business or optimization logic
- All decision-making is delegated to the service layer
- Clean HTTP status codes are used:
  - `200 OK` for valid decisions
  - `400 Bad Request` for invalid inputs

### Outcome

The system can now be integrated with any backend through a simple HTTP interface while keeping the inference pipeline fully isolated and maintainable.

## 5. LOGIC+ Improvements (Phase 5)

Before introducing ML, the rule-based optimizer was enhanced to improve decision quality.

### Enhancements
- Ads are sorted by business priority (high to low)
- Within the same priority, ads are sorted by cost (low to high)
- Maintains deterministic, explainable behavior

### Outcome
The system produces higher-quality, business-aligned decisions
while remaining simple, fast, and fully explainable.

## 6. Machine Learning Training Pipeline (Phase 6)

After improving the rule-based optimizer, a machine learning training pipeline was introduced to learn patterns from historical ad performance data.

### Objective
To build a **reproducible and modular ML training pipeline** that can generate a predictive model without affecting the live inference system.

### Key Design Principles
- Training and inference are strictly separated
- Feature engineering logic is shared across training and inference
- ML artifacts are treated as runtime outputs, not source code

### Training Pipeline Structure
training/
├── steps/
│ ├── train_model.py
│ ├── evaluate_model.py
│ └── save_model.py
├── pipeline/
│ └── run_training_pipeline.py


### Workflow
1. Historical ad performance data is generated
2. Features are engineered consistently
3. The model is trained and evaluated
4. A trained model in artifact is produced locally

### Notes
- The trained model file (`value_model.pkl`) is intentionally excluded from version control
- The training pipeline can be re-run at any time to regenerate the model

This phase establishes a **production-aligned ML foundation**.

---

## 7. Hybrid ML Inference System (Phase 7)

In this phase, the trained ML model is integrated into the FastAPI inference system using a **hybrid optimization approach**.

### Core Idea
Machine learning is introduced as an **assistive signal**, while business rules retain final control over decisions.

---

### Optimizer Versions

#### Optimizer v1 – Rule-Based
- Uses deterministic business rules
- Fully explainable and predictable
- Acts as a safe fallback mechanism

#### Optimizer v2 – Hybrid ML
- Uses the ML model to predict a value score for each ad
- Combines ML score with business signals such as:
  - ad priority
  - cost penalty
- Produces a final hybrid score used for ranking ads

---

### Decision Service (Central Control Layer)

A dedicated decision service is responsible for:
- Validating incoming requests
- Selecting the optimizer version (v1 or v2)
- Keeping the API layer independent of optimization logic

This design enables:
- Safe ML rollout
- Easy rollback to rule-based logic
- Future A/B testing support

---

### Hybrid Scoring Logic (Conceptual)

The final ranking score is calculated by combining the ML prediction with business rules, ensuring that machine learning assists decision-making without fully controlling it.

final_score = (ML score × weight) + (priority influence) − (cost penalty)

- The ML score provides a predictive signal based on historical performance
- Priority ensures business-critical ads are favored
- Cost penalty prevents expensive ads from dominating the selection

This hybrid approach ensures decisions remain safe, explainable, and aligned with business objectives.

Even if ML predictions are imperfect, the final decision remains stable and interpretable because business rules retain control.


---

### Running the Inference API

Start the server:

```bash
uvicorn app.main:app --reload
