from decimal import Decimal, ROUND_DOWN
CENTS = Decimal("0.01")
def calculateAllocationNumbersPerPortfolio(deposit_plans, deposits):
    portfolios = dict()
    final_allocations = dict()
    total_deposit = Decimal("0")
    one_time_plan = {}
    monthly_plan = {}
    for deposit_plan in deposit_plans:
        if deposit_plan["type"] == "one_time":
            one_time_plan = deposit_plan.get("allocations", {})
        elif deposit_plan["type"] == "monthly":
            monthly_plan = deposit_plan.get("allocations", {})

    summed_weights = Decimal("0")
    for p in set(one_time_plan) | set(monthly_plan):
        portfolios[p] = Decimal(str(one_time_plan.get(p, 0))) + Decimal(str(monthly_plan.get(p, 0)))
        summed_weights += portfolios[p]

    for deposit in deposits:
        total_deposit += Decimal(str(deposit))

    if not portfolios:
        return {"Unassigned": total_deposit}

    if summed_weights == Decimal("0"):
        n = len(portfolios)
        base = (total_deposit / n).quantize(CENTS, rounding=ROUND_DOWN)
        down = {p: base for p in portfolios}
        return distribute_leftover(down, total_deposit)

    raw = {p: total_deposit * (portfolios[p] / summed_weights) for p in portfolios}
    down = {p: amt.quantize(CENTS, rounding=ROUND_DOWN) for p, amt in raw.items()}
    return distribute_leftover(down, total_deposit)

def distribute_leftover(base_allocs, target_total):
    """
    base_allocs: dict[str, Decimal] already rounded DOWN to cents
    target_total: Decimal total we must hit exactly
    Rule: give one cent to each portfolio in sorted-key order until leftover is 0.
    """
    leftover = target_total - sum(base_allocs.values())
    if leftover <= 0:
        return base_allocs

    rem_cents = int((leftover / CENTS))
    keys = sorted(base_allocs.keys())

    i = 0
    while rem_cents > 0:
        base_allocs[keys[i % len(keys)]] += CENTS
        rem_cents -= 1
        i += 1
    return base_allocs

print(calculateAllocationNumbersPerPortfolio([{"type": "one_time", "allocations": {"High-Risk": 10000, "Retirement": 500}},
                                        {"type": "monthly", "allocations": {"High-Risk": 0, "Retirement": 100}}], [10000, 600]))