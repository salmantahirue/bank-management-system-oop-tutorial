# Banking Management System - Project Requirements

## Project Overview
Build a terminal-based Banking Management System in Python using Object-Oriented Programming. All data must be stored in a JSON file.

## Core Requirements

### 1. User Management
- Users can register with a username and password
- Passwords must be hashed before storage
- Users can log in with their credentials
- Username must be unique

### 2. Account Types
- Support two account types: Savings Account and Current Account
- Each user has one account created during registration
- Initial balance is 0
- Savings Account: Cannot withdraw below 0 (no overdraft)
- Current Account: Can withdraw up to -500 (overdraft limit)

### 3. Banking Operations
- Deposit Money: Users can deposit positive amounts
- Withdraw Money: Users can withdraw based on account type rules
- Balance Inquiry: Users can check their current balance
- All operations must validate amounts (positive values, sufficient funds)

### 4. Transaction History
- Record every deposit and withdrawal
- Each transaction stores: transaction ID, account ID, type (DEPOSIT/WITHDRAW), amount, timestamp
- Users can view their complete transaction history
- Transactions are immutable (cannot be edited or deleted)

### 5. Data Storage
- All data must be stored in a single JSON file
- Data persists across program restarts
- JSON file structure: users array, accounts array, transactions array

### 6. User Interface
- Terminal/Command Line Interface (CLI)
- Menu-driven system with clear options
- User-friendly prompts and error messages
- Display formatted output for balance and transactions

## Technical Requirements

### OOP Implementation
- Use classes for User, Account, and Transaction
- Implement inheritance: SavingsAccount and CurrentAccount inherit from a base Account class
- Use abstraction: Account should be an abstract base class
- Implement polymorphism: withdraw() method behaves differently for Savings and Current accounts
- Use encapsulation: Protect balance from direct modification
- Create custom exception classes for error handling

### File Handling
- Read from and write to JSON file safely
- Handle file not found scenarios
- Handle corrupted JSON data gracefully

### Validation
- Validate all user inputs
- Prevent negative deposits
- Enforce account-specific withdrawal rules
- Show clear error messages for invalid operations

## Deliverables
1. Complete Python project with proper file structure
2. Working terminal-based application
3. JSON file for data persistence
4. Code demonstrating OOP concepts (inheritance, polymorphism, encapsulation, abstraction)

## Evaluation Criteria
- Correct implementation of OOP concepts
- Clean code structure and organization
- Proper error handling
- Data persistence working correctly
- All requirements implemented and functional

## Notes
- Focus on clean OOP design
- Code should be readable and well-commented
- No external databases required (JSON file only)
- No web framework required (terminal interface only)
