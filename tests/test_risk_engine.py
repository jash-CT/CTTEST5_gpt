from app.services.risk_engine import compute_risk_score


def test_high_credit_low_dti():
    # High credit and low debt-to-income should yield a low risk score
    score = compute_risk_score(credit_score=780, income=100000.0, amount=10000.0)
    assert isinstance(score, int)
    assert score == 20


def test_low_credit_high_dti():
    # Low credit and high DTI should have high risk
    score = compute_risk_score(credit_score=600, income=20000.0, amount=10000.0)
    assert isinstance(score, int)
    assert score >= 70


def test_zero_income_high_risk():
    score = compute_risk_score(credit_score=700, income=0.0, amount=5000.0)
    assert score >= 60
