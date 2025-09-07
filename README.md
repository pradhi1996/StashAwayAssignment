# Deposit Plan Allocation

## Problem
At StashAway, customers can create deposit plans (one-time and/or monthly) to allocate incoming deposits into different portfolios.  
This project implements a function:

```
calculateAllocationNumbersPerPortfolio(deposit_plans, deposits)
```
that returns the final allocation of funds amongst the customers portfolios. 

## Assumptions & Design Decisions

Deposit Plans: Each plan specifies absolute amounts per portfolio. We treat these as weights that determine the ratio of allocation.
Combined Weights: For each portfolio, weights from one-time and monthly plans are summed.

Distribution:
Deposits are fully distributed across portfolios in proportion to weights.

If all weights are zero, funds are split equally across all the portfolios.
If no portfolios exist, funds are returned under a single key: {"Unassigned": total}.

Money Handling:
1. All amounts use Python’s Decimal for exact cents. 
2. Allocations are rounded down to cents (0.01).

Any leftover cents are distributed in a deterministic round-robin order across portfolios.
Deterministic: Same input always produces the same output.

## Running the code
1. Clone the repository
2. pip install pytest 
3. Run tests pytest -q
4. Run python3 allocation_portfolios.py to run the main code block functionality

## Notes

1. No database or API layer included — the focus is on core business logic.
2. Code is written to be maintainable and easy to extend if new rules are added.