import asyncio
import random
import time
from models import CustomerContext
# Mock External System Fetches
async def fetch_crm(phone: str):
    "Simulates CRM system fetch (200–400ms delay)."
    await asyncio.sleep(random.uniform(0.2, 0.4))
    return {
        "phone": phone,
        "name": "John Doe",
        "vip": random.choice([True, False]),
        "plan": "fiber_100mbps"
    }

async def fetch_billing(phone: str):
    "Simulates Billing system fetch (150–350ms delay) with 10% timeout chance."
    await asyncio.sleep(random.uniform(0.15, 0.35))
    # 10% chance of failure
    if random.random() < 0.1:
        raise TimeoutError("Billing system timeout")
    return {
        "phone": phone,
        "status": random.choice(["paid", "overdue"]),
        "last_payment_days": random.randint(1, 40)
    }

async def fetch_ticket_history(phone: str):
    "Simulates Ticket history system fetch (100–300ms delay)."
    await asyncio.sleep(random.uniform(0.1, 0.3))
    return {
        "phone": phone,
        "complaints": [
            "slow_internet",
            "billing_issue",
            "router_restart",
            "network_problem",
            "Wi-Fi_not working",
            "service_outage"
        ]
    }

# Sequential Fetch
async def fetch_sequential(phone: str):
    start = time.perf_counter()
    crm = await fetch_crm(phone)

    try:
        billing = await fetch_billing(phone)
    except TimeoutError:
        print("Warning: billing fetch failed")
        billing = None
    tickets = await fetch_ticket_history(phone)
    end = time.perf_counter()
    fetch_time_ms = (end - start) * 1000
    print(f"Sequential fetch took {fetch_time_ms:.2f} ms")
    return CustomerContext(
        crm_data=crm,
        billing_data=billing,
        ticket_data=tickets,
        data_complete=(billing is not None),
        fetch_time_ms=fetch_time_ms
    )
# Parallel Fetch
async def fetch_parallel(phone: str):
    start = time.perf_counter()
    results = await asyncio.gather(
        fetch_crm(phone),
        fetch_billing(phone),
        fetch_ticket_history(phone),
        return_exceptions=True
    )

    crm, billing, tickets = results
    data_complete = True
    if isinstance(billing, Exception):
        print("Warning: billing fetch failed")
        billing = None
        data_complete = False

    end = time.perf_counter()
    fetch_time_ms = (end - start) * 1000
    print(f"Parallel fetch took {fetch_time_ms:.2f} ms")
    return CustomerContext(
        crm_data=crm,
        billing_data=billing,
        ticket_data=tickets,
        data_complete=data_complete,
        fetch_time_ms=fetch_time_ms
    )

async def main():
    phone = "9876543210"
    print("Running sequential fetch...")
    sequential_context = await fetch_sequential(phone)
    print(sequential_context)
    print("\nRunning parallel fetch...")
    parallel_context = await fetch_parallel(phone)
    print(parallel_context)


if __name__ == "__main__":
    asyncio.run(main())