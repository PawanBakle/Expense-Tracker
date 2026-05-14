Here is a solid, professional README that sounds like it was written by a developer who cares about architecture, not an AI trying to sell a product.

---

# Expense Tracker API

A high-performance, containerized backend engine built with Django and PostgreSQL for managing group-based financial ledgers and settlements.

## Architecture & Database Design

The system is designed around a relational schema to ensure data integrity across complex transaction splits.

```text
UserBase (Custom User)
    ├── created_groups (FK -> Group)
    └── memberships (FK -> GroupMember)

Group
    ├── members (Reverse FK -> GroupMember)
    └── expenses (Reverse FK -> Expense)

GroupMember
    ├── user (FK -> UserBase)
    ├── group (FK -> Group)
    └── role (Admin/Member)

Expense (The Ledger)
    ├── group (FK -> Group)
    ├── paid_by (FK -> UserBase)
    └── split_data (JSON/Related logic for individual shares)

Settlement
    ├── sender (FK -> UserBase)
    ├── receiver (FK -> UserBase)
    └── status (Pending/Completed)

```

## Performance Optimization

The core challenge in group ledgers is the **N+1 query problem**, where fetching a group and its 50+ expenses normally results in 50+ separate database hits.

To solve this, I optimized the `GroupView` detail endpoint using Django’s `prefetch_related`. By fetching all related group members and expense records in a single batch query, the system achieves **O(1) database round-trips**. This ensures that even as a group’s transaction history grows, the API response time remains constant and the database load remains minimal.

## Security & IDOR Neutralization

Security in a financial app is paramount. I implemented strict **Object-Level Authorization** to prevent **Insecure Direct Object Reference (IDOR)** attacks.

Instead of relying solely on global authentication, the backend executes explicit filtering logic on every request. Before any transaction data is serialized, the system cross-references the `request.user` against the specific `GroupMember` table for that resource. If a user is not a verified member of the group, the API returns a `404 Not Found` or `403 Forbidden`, ensuring that private financial data is mathematically isolated between different groups and users.

## Local Setup

### Prerequisites

* Docker & Docker Compose

### Commands

1. Clone the repo and navigate to the root.
2. Build and run the containers:
```bash
docker-compose up --build

```


3. Seed the database with test data (Alice, Bob, and Charlie):
```bash
docker-compose exec web python manage.py seed_db

```


4. Access the API at `http://localhost:8000/api/`.

## Testing

The API is headless. A full Postman collection for verifying the authentication flow and transaction logic is located in the `/postman` directory.

```

```