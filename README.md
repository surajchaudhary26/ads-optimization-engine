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
