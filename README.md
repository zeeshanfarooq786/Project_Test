# Inventory Management System - Technical Assessment

A real-time inventory purchase management system built with **Laravel 11**, **Livewire 3**, and **Alpine.js**.

## 🚀 Key Features

- **Dynamic Purchase Form:** Add/Remove rows on the fly without page reloads.
- **Reactive Totals:** Real-time calculation of subtotals and grand totals using Alpine.js.
- **RBAC (Role-Based Access Control):** 
    - **Admin:** Full CRUD access, duplicate prevention logic, and data migration tools.
    - **User:** View-only access to purchase history.
- **Data Integrity:** Prevents duplicate Item + Brand combinations within a single purchase.
- **Legacy Migration:** Custom Artisan command to normalize and import legacy array data into the new schema.

## 🛠 Tech Stack
- **Backend:** Laravel 11 (PHP 8.2+)
- **Frontend:** Livewire 3, Alpine.js, Tailwind CSS
- **Database:** MySQL (Normalized Schema)

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/zeeshanfarooq786/Project_Test.git](https://github.com/zeeshanfarooq786/Project_Test.git)
   cd Project_Test