import pytest
from task4.escalation import should_escalate
from task3.models import CustomerContext


def create_context(vip=False, billing_status="paid", complaints=None, data_complete=True):

    if complaints is None:
        complaints = ["slow_internet"]

    return CustomerContext(
        crm_data={"vip": vip},
        billing_data={"status": billing_status},
        ticket_data={"complaints": complaints},
        data_complete=data_complete,
        fetch_time_ms=200
    )


def test_low_confidence():
    """Escalate when AI confidence is below 0.65."""
    context = create_context()
    result = should_escalate(context, 0.5, 0.1, "internet_issue")
    assert result == (True, "low_confidence")


def test_angry_customer():
    """Escalate when sentiment score indicates angry customer."""
    context = create_context()
    result = should_escalate(context, 0.9, -0.8, "internet_issue")
    assert result == (True, "angry_customer")


def test_repeat_complaint():
    """Escalate when same complaint appears three or more times."""
    complaints = ["slow_internet", "slow_internet", "slow_internet"]
    context = create_context(complaints=complaints)
    result = should_escalate(context, 0.9, 0.1, "internet_issue")
    assert result == (True, "repeat_complaint")


def test_service_cancellation():
    """Escalate immediately when intent is service cancellation."""
    context = create_context()
    result = should_escalate(context, 0.95, 0.2, "service_cancellation")
    assert result == (True, "service_cancellation")


def test_vip_overdue():
    """Escalate when customer is VIP and billing is overdue."""
    context = create_context(vip=True, billing_status="overdue")
    result = should_escalate(context, 0.9, 0.1, "billing_issue")
    assert result == (True, "vip_overdue")


def test_incomplete_data_low_confidence():
    """Escalate when data is incomplete and confidence is below 0.80."""
    context = create_context(data_complete=False)
    result = should_escalate(context, 0.7, 0.1, "internet_issue")
    assert result == (True, "incomplete_data")


def test_ai_can_handle():
    """AI should handle request when none of the escalation rules trigger."""
    context = create_context()
    result = should_escalate(context, 0.95, 0.2, "internet_issue")
    assert result == (False, "ai_can_handle")


def test_multiple_complaints_but_not_three():
    """Edge case: two complaints should not trigger repeat complaint escalation."""
    complaints = ["slow_internet", "slow_internet"]
    context = create_context(complaints=complaints)
    result = should_escalate(context, 0.9, 0.1, "internet_issue")
    assert result == (False, "ai_can_handle")