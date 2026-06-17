def calculate_risk_score(amount: int):
    if amount >= 100000:
        return 90

    if amount >= 50000:
        return 70

    if amount >= 10000:
        return 40

    return 10