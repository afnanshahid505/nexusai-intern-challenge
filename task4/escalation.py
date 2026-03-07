from typing import Tuple
from task3.models import CustomerContext


def should_escalate(
    context: CustomerContext,
    confidence_score: float,
    sentiment_score: float,
    intent: str
) -> Tuple[bool, str]:

    # Rule 1
    if confidence_score < 0.65:
        return True, "low_confidence"

    # Rule 2
    if sentiment_score < -0.6:
        return True, "angry_customer"

    # Rule 3
    complaints = context.ticket_data.get("complaints", [])

    for complaint in complaints:
        if complaints.count(complaint) >= 3:
            return True, "repeat_complaint"

    # Rule 4
    if intent == "service_cancellation":
        return True, "service_cancellation"

    # Rule 5
    if (
        context.crm_data.get("vip") is True
        and context.billing_data
        and context.billing_data.get("status") == "overdue"
    ):
        return True, "vip_overdue"

    # Rule 6
    if not context.data_complete and confidence_score < 0.80:
        return True, "incomplete_data"

    return False, "ai_can_handle"