# 💳 Credit Card Lending System – Django Backend IEC2021125 Sagar Das

This project is a backend application built with **Django** to simulate a **credit card system** that helps users borrow money, repay it in installments (EMIs), and get monthly bills. This was developed as part of the **Bright Money Backend Intern Assignment**.

---

## 📸 Admin Dashboard Preview

Below is a snapshot of the admin panel:

![Admin Panel](Screenshot%202025-05-17%20140303.png)

You can view and manage the following models:
- Users
- Transactions
- Loans
- EMIs
- Payments
- Billings
- Periodic Tasks (for automated scheduling)

---

## ✅ Key Features

### 1. 🧍‍♂️ User Registration & Credit Score Calculation
- A user can register with name, Aadhaar number, email, and income.
- After registration, a **background task** calculates the user's **credit score** using their bank statement data.

### 2. 💰 Loan Approval Based on Credit Score
- If the user has an income ≥ ₹1.5L and credit score ≥ 450, they are auto-approved.
- A virtual credit card is issued with a ₹5000 loan balance.
- EMI plan is created with monthly interest.

### 3. 📥 EMI Payment System
- The system tracks and verifies EMI payments.
- Payments must follow the correct order and amount.
- Prevents skipping or partial payments.

### 4. 🧾 Monthly Billing (Automated)
- A **cron job** checks daily for users needing a new bill.
- Adds principal and interest to the statement.
- Stores the **minimum amount due**.

### 5. 📊 Statement View
- API shows all past and upcoming EMI payments.
- User gets clear insights into their repayment schedule.

---

## ⚙️ How It Works (In Simple Terms)

1. You register a user.
2. The system checks your past transactions.
3. Based on your score, it gives you a credit line.
4. You repay in EMIs.
5. Every month, a bill is auto-generated.
6. You can check your full payment history anytime.

---

## 🚀 Tech Stack

| Tech             | Purpose                            |
|------------------|-------------------------------------|
| Python & Django  | Backend Framework                   |
| Django REST      | APIs for registration, loans, EMI   |
| Celery           | Background task (credit score, bills) |
| Pandas           | CSV transaction parsing             |
| Django Admin     | View and manage all models          |

---

## 🔄 Setup Instructions

1. **Clone the repository**
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## 🧪 API Endpoints (Brief)
1. POST /api/register-user/ → Register new user

2. POST /api/apply-loan/ → Request credit loan

3. POST /api/pay-emi/ → Repay EMI amount

4. GET /api/get-statement/ → See full EMI history

## 📌 Conclusion
 This backend mimics a real-world credit card system. It:

1. Automates approval based on credit data

2. Generates EMI and bills intelligently

3. Tracks all dues & payments

4. Uses a clean admin interface for monitoring

It’s designed for real-time financial systems with extendable architecture.
   
