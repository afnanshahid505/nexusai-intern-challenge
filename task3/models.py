from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class CustomerContext:
    crm_data: Optional[Dict]
    billing_data: Optional[Dict]
    ticket_data: Optional[Dict]
    data_complete: bool
    fetch_time_ms: float