# Bank Management System (File-Based, OOP-Centric, Full-Stack Learning Project)

This repository is a **learning-first** Bank Management System built to help Python interns practice **Object-Oriented Programming (OOP)** by implementing a real-world project end-to-end.

It includes:
- **Backend**: Python + Flask (simple web server)
- **Frontend**: HTML/CSS/JavaScript (beginner-friendly UI)
- **Storage**: File-based JSON (no database)

> This README is written as a **step-by-step educational guide**.  
> You can use it for revision, mentoring sessions, and portfolio practice.

---

## 1) Project Overview (Simple explanation)

We’re building a tiny “bank” system where users can:
- Create an account and log in (file-based auth)
- Deposit / withdraw money
- Check balance
- View transaction history
- Choose account type (Savings / Current) using **inheritance**

The goal is not “fancy features”. The goal is **clean OOP thinking**: classes, responsibilities, file storage, and a simple UI.

---

## 2) Real-World Problem Understanding

In a real bank, we have:
- Customers (users) with credentials
- Bank accounts (savings/current) with balances
- Rules for deposits/withdrawals (validation, limits, fees)
- Transactions recorded for auditing
- Persistent storage so data survives restarts

Our simplified version keeps the same ideas, but stores everything in JSON files instead of a database.

---

## 3) How an Expert Thinks About This Problem (before writing code)

### Think in “responsibilities”, not “features”

An expert starts by asking:
- What are the real-world “things” (entities)?
- What does each “thing” **know** (data/attributes)?
- What can each “thing” **do** (methods/behavior)?
- Which logic belongs in the entity vs. a service?
- How do we store/retrieve data safely?

### Identify boundaries (separation of concerns)

We split the system into layers:
- **Domain (models)**: pure OOP entities (Account, User, Transaction)
- **Services (business logic)**: operations like login, deposit, withdraw
- **Storage (repositories)**: file read/write logic
- **Web (Flask routes)**: HTTP endpoints and page rendering
- **Frontend**: UI pages + JavaScript to call API endpoints

This is “production-style” thinking, but kept beginner-friendly.

---

## 4) Identifying Classes and Responsibilities

### Core entities (classes)

- **User**
  - **Attributes**: id, username, password_hash, created_at
  - **Behavior**: mostly data; auth rules live in `AuthService`

- **Account (Abstract Base Class)**
  - **Attributes**: account_id, user_id, balance
  - **Methods**: deposit(), withdraw() (rules vary by account type)
  - **Why abstract?** We want a shared contract for all account types.

- **SavingsAccount(Account)** (Inheritance)
  - Example rule: cannot go below 0, optional withdrawal limit

- **CurrentAccount(Account)** (Inheritance)
  - Example rule: allows overdraft up to a limit (polymorphism in withdraw())

- **Transaction**
  - **Attributes**: id, account_id, type, amount, timestamp, note
  - **Why?** Transaction history must be auditable.

### Composition (has-a relationships)

- **BankSystem** (or services) **has** repositories:
  - `UserRepository`, `AccountRepository`, `TransactionRepository`

This is composition: services “use” storage classes instead of inheriting them.

---

## 5) Project Folder Structure Explanation

```
Bank Management System/
├─ backend/                 <-- Python Logic Only
│  ├─ app.py                <-- Flask Entry Point
│  ├─ domain/               <-- Entities (User, Account)
│  ├─ services/             <-- Business Rules
│  └─ storage/              <-- Data Access (JSON)
├─ frontend/                <-- UI Code Only
│  ├─ templates/            <-- HTML Pages
│  └─ static/               <-- CSS & JS
├─ data/
│  └─ bank_data.json
├─ requirements.txt
└─ README.md
```

---

## 6) Step-by-Step Implementation

We will implement in this learning order:

### Step 1: Basic skeleton
- Create folders, empty modules, and a starter Flask app.

### Step 2: Core classes (OOP domain)
- Build `Account` (abstract), `SavingsAccount`, `CurrentAccount`
- Build `User` and `Transaction`
- Add custom exceptions

### Step 3: File storage layer (JSON)
- A safe JSON store helper (read/write)
- Repositories for users, accounts, transactions

### Step 4: Business logic
- Auth service (register/login)
- Account service (deposit/withdraw/balance/history)

### Step 5: Frontend integration
- HTML pages (login/register/dashboard)
- JS fetch calls to backend API endpoints

### Step 6: Testing & usage
- Run server, create user, deposit/withdraw, check history

---

## 7) Common Mistakes Beginners Make (and how to avoid them)

- **Putting everything in one file**
  - Fix: use small modules (domain/services/storage/web).
- **Mixing UI, storage, and business logic**
  - Fix: repositories store, services decide, routes expose.
- **No validations**
  - Fix: validate amount > 0, sufficient funds, etc.
- **Storing plain text passwords**
  - Fix: hash passwords (even for learning projects).
- **No transaction history**
  - Fix: always log deposit/withdraw as transactions.

---

## 8) How to Extend This Project Further

- Admin panel (view all accounts)
- Password reset flows
- Interest calculation for Savings accounts
- Account statement export (CSV)
- Unit tests (pytest) for services
- Better session/auth (tokens, cookies, CSRF protection)

---

## How to Run

### Install

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Start server

```bash
python backend/app.py
```

Open the app in your browser at:
- `http://127.0.0.1:5000`

---

## Data Storage (File-Based)

All data is stored in:
- `data/bank_data.json`

This file contains users, accounts, and transactions in JSON format.

---

## OOP Concepts Covered

- Class & Object
- Constructor (`__init__`)
- Encapsulation (private-ish attributes + methods for safe updates)
- Inheritance (Savings/Current from Account)
- Polymorphism (withdraw rules differ by account type)
- Abstraction (`abc` module)
- Composition (services use repositories)
- SOLID principles (basic separation and single responsibility)
- Exception Handling (custom domain exceptions)
- File Handling (JSON read/write)

---

## Interview Preparation & Assessment

This project includes a comprehensive **Interview Preparation** module to help you prepare for Python OOP interviews.

### Interview Preparation Section

Access detailed interview questions organized by difficulty:
- **Easy**: Fundamental OOP concepts (4 questions)
- **Medium**: Intermediate topics (4 questions)
- **Hard**: Advanced concepts (3 questions)
- **Expert**: Design patterns and architecture (3 questions)

Each question includes:
- Short interview-ready answer
- Detailed explanation
- Real-world analogy
- Python code example
- How it's used in this Bank Management System

**Access:** Navigate to `/learn/interview` in the web interface

### Assessment Test

Take MCQ-based assessments to evaluate your understanding:
- 10 randomly selected questions per test
- Questions from all difficulty levels
- Immediate feedback with explanations
- Score tracking and performance evaluation
- Retake capability for practice

**Access:** Navigate to `/learn/interview/assessment` in the web interface

### Revision Mode

Quick reference section with:
- OOP concept summaries
- Key takeaways
- Common mistakes to avoid
- Interview quick tips
- "Explain in your own words" practice prompts

**Access:** Navigate to `/learn/revision` in the web interface

---

## How to Use for Interview Preparation

1. **Study the Learning Guide**: Start with Introduction → Problem Statement → Expert Design → OOP Concepts
2. **Practice Interview Questions**: Go through questions by difficulty level, study each answer thoroughly
3. **Take Assessment Tests**: Test your knowledge with MCQ assessments
4. **Review Revision Section**: Use quick reference for last-minute preparation
5. **Practice Explaining**: Use the "Explain in your own words" section to practice verbalizing concepts

