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
