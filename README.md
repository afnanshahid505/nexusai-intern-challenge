# Nexus AI Intern Challenge
This repository contains the implementation of the Nexus AI Intern Challenge.  
The project is divided into multiple tasks, each representing a different component of the backend architecture.
# project struture
task1/ # AI Message Handler
task2/ # Database Schema and Repository
task3/ # Parallel Data Fetcher
task4/ # Escalation Decision Engine
ANSWERS.md # Task 5 written answers
README.md
requirements.txt

# Task 1 — AI Message Handler
If you want to run the AI integration in Task 1, create a `.env` file and add your OpenAI, Apikey. 
This component processes customer messages and generates AI responses using an LLM.
Features:
- Async AI request handling
- Timeout protection (10 seconds)
- Rate limit retry logic
- Channel-aware formatting (voice vs chat)
- Structured response object using dataclasses
Run test example:
python -m task1.test_handler

# Task 2 — Database Schema & Repository
This task defines the PostgreSQL schema used to store customer interactions.
Components:
-schema.sql
-repository.py
-analytics.py
The repository supports:
- Saving call records
- Retrieving recent customer interactions
This task focuses on database design and query safety rather than runtime execution.

# Task 3 — Parallel Data Fetcher
This module demonstrates asynchronous parallel fetching of customer context from multiple systems.
Simulated services:
- CRM system
- Billing system
- Ticket history service
Two implementations are provided:
-fetch_sequential()
-fetch_parallel()
Run example:
python -m task3.fetcher

# Task 4 — Escalation Decision Engine
This component determines whether a customer issue should be handled by AI or escalated to a human agent.
Escalation rules include:
- Low AI confidence
- Negative customer sentiment
- Repeated complaints
- Service cancellation requests
- VIP customers with overdue billing
- Incomplete data with low confidence
Unit tests were written using `pytest`.
Run tests:
pytest task4 -v


# Handling Rule Conflicts
When multiple escalation rules could apply simultaneously, rule priority determines the outcome. In this implementation, rules are evaluated sequentially and the first matching rule triggers escalation.
For example, if the AI confidence score is high (0.90) but the detected intent is `service_cancellation`, the system still escalates the case. This is because service cancellation is considered a critical intent that requires human intervention regardless of model confidence. High confidence only means the AI is confident about understanding the request, not that it should resolve it automatically.
Prioritizing critical intents ensures that sensitive situations such as cancellations or repeated failures are handled by human agents. This approach favors customer experience and risk mitigation over automation efficiency.

# Task 5 — Answers for Questions
The answers for the system design questions are provided.

