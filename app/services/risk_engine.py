def compute_risk_score(credit_score: int, income: float, amount: float) -> int:
    """
    Deterministic rule-based risk scoring.

    Returns an integer risk score where lower is better (0-100 scale).
    Rules (example):
      - Start at 50
      - Adjust by credit score: higher credit reduces risk
      - Adjust by debt ratio proxy: amount/income
      - Caps applied
    """
    score = 50

    # credit score contribution
    if credit_score >= 750:
        score -= 20
    elif credit_score >= 700:
        score -= 10
    elif credit_score >= 650:
        score += 0
    else:
        score += 15

    # debt-to-income proxy
    if income <= 0:
        score += 40
    else:
        dti = amount / (income + 1e-6)
        if dti < 0.2:
            score -= 10
        elif dti < 0.35:
            score += 0
        else:
            score += 20

    # loan size cap relative to income
    if amount > income * 10:
        score += 20

    # normalize
    score = max(0, min(100, int(score)))
    return score
