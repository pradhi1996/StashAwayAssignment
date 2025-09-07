# tests/test_allocation.py
from decimal import Decimal
from allocation_portfolios import calculateAllocationNumbersPerPortfolio  # adjust import to your module

def D(x):  # helper to convert to Demical
    return Decimal(str(x))

def test_happy_case_example():
    plans = [
        {"type": "one_time", "allocations": {"High-Risk": 10000, "Retirement": 500}},
        {"type": "monthly",  "allocations": {"High-Risk":     0, "Retirement": 100}},
    ]
    res = calculateAllocationNumbersPerPortfolio(plans, [10000, 600])
    assert res["High-Risk"] == D("10000.00")
    assert res["Retirement"] == D("600.00")
    assert sum(res.values()) == D("10600.00")

def test_ratio_split_general():
    plans = [
        {"type": "one_time", "allocations": {"A": 2, "B": 1}},
        {"type": "monthly",  "allocations": {"A": 1, "B": 1}},
    ]
    # weights: A=3, B=2; total=100
    res = calculateAllocationNumbersPerPortfolio(plans, [100])
    assert sum(res.values()) == D("100.00")
    # A should get ~60, B ~40 (allow for cent fix)
    assert res["A"] + res["B"] == D("100.00")
    assert res["A"] >= D("60.00") - D("0.01")  # tolerant by a cent
    assert res["B"] <= D("40.00") + D("0.01")

def test_all_weights_zero_equal_split():
    plans = [
        {"type": "one_time", "allocations": {"A": 0, "B": 0}},
        {"type": "monthly",  "allocations": {"A": 0, "B": 0}},
    ]
    res = calculateAllocationNumbersPerPortfolio(plans, [101])
    assert res["A"] == D("50.50")
    assert res["B"] == D("50.50")
    assert sum(res.values()) == D("101.00")

def test_missing_one_plan():
    plans = [
        {"type": "one_time", "allocations": {"A": 3, "B": 1}},
        # monthly missing
    ]
    res = calculateAllocationNumbersPerPortfolio(plans, [100])
    assert sum(res.values()) == D("100.00")
    # A should be ~75, B ~25
    assert res["A"] >= D("75.00") - D("0.01")
    assert res["B"] <= D("25.00") + D("0.01")

def test_portfolio_only_in_monthly():
    plans = [
        {"type": "monthly", "allocations": {"A": 0, "B": 5, "C": 5}},
    ]
    res = calculateAllocationNumbersPerPortfolio(plans, [10])
    assert sum(res.values()) == D("10.00")
    # B and C should split ~50/50, A should be ~0
    assert res["A"] in (D("0.00"), D("0"))
    assert abs(res["B"] - D("5.00")) <= D("0.01")
    assert abs(res["C"] - D("5.00")) <= D("0.01")

def test_no_portfolios_returns_unassigned():
    plans = []  # no plans at all
    res = calculateAllocationNumbersPerPortfolio(plans, [12.34])
    assert res == {"Unassigned": D("12.34")}

def test_fractional_deposits_and_cents_reconciliation():
    plans = [{"type": "one_time", "allocations": {"X": 1, "Y": 1, "Z": 1}}]
    res = calculateAllocationNumbersPerPortfolio(plans, [0.05])
    # Expect three entries that sum exactly to 0.05 with cents only
    assert sum(res.values()) == D("0.05")
    for v in res.values():
        # each should be multiple of 0.01
        assert (v * 100) == (v * 100).quantize(Decimal("1"))
