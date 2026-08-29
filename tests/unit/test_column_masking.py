import pytest
from data_engine.governance.column_masking_engine import ColumnMaskingEngine, MaskingStrategy


def test_column_masking_strategies():
    engine = ColumnMaskingEngine()
    engine.add_masking_rule("email", "ANALYST", MaskingStrategy.EMAIL_OBFUSCATE)
    engine.add_masking_rule("ssn", "ANALYST", MaskingStrategy.FULL_REDACT)
    engine.add_masking_rule("card_number", "ANALYST", MaskingStrategy.CREDIT_CARD_PARTIAL)

    raw_row = {
        "user_id": "U-101",
        "email": "sarah.connor@cyberdyne.com",
        "ssn": "123-45-6789",
        "card_number": "4111-2222-3333-4444",
        "amount": 500.0,
    }

    # Analyst sees masked fields
    analyst_view = engine.mask_row(raw_row, user_role="ANALYST")
    assert analyst_view["email"] == "s***r@cyberdyne.com"
    assert analyst_view["ssn"] == "******"
    assert analyst_view["card_number"] == "****-****-****-4444"
    assert analyst_view["user_id"] == "U-101"
    assert analyst_view["amount"] == 500.0

    # Compliance officer sees raw data
    compliance_view = engine.mask_row(raw_row, user_role="COMPLIANCE_OFFICER")
    assert compliance_view["ssn"] == "123-45-6789"
    assert compliance_view["email"] == "sarah.connor@cyberdyne.com"
