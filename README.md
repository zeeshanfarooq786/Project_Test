# Inventory Management System - Technical Assessment



A professional inventory purchase management system built with **Laravel 11**, **Livewire 3**, and **Alpine.js**. This project demonstrates full-stack proficiency, real-time reactivity, and secure database architecture.



## 🚀 Key Features



*   **Dynamic Purchase Form:** Add or remove rows on the fly using Livewire and Alpine.js without page reloads.

*   **Reactive Totals:** Real-time calculation of subtotals and grand totals handled client-side for maximum performance.

*   **Role-Based Access Control (RBAC):** 

    *   **Admin:** Full access to create/edit/delete purchases and run the legacy migration command.

    *   **User:** Read-only access to the purchase history.

*   **Data Integrity:** Implemented logic to prevent duplicate **Item + Brand** combinations within a single purchase.

*   **Legacy Data Migration:** A custom, idempotent Artisan command that normalizes and imports legacy array data while creating missing Items or Brands automatically.



## 🛠 Tech Stack



*   **Backend:** PHP 8.2+ / Laravel 11.x

*   **Frontend:** Livewire 3.x, Alpine.js 3.x, Tailwind CSS

*   **Database:** MySQL (Normalized Schema)



## 📦 Installation & Setup



1.  **Clone the repository:**

    ```bash

    git clone [https://github.com/zeeshanfarooq786/Project_Test.git](https://github.com/zeeshanfarooq786/Project_Test.git)

    cd Project_Test

    ```



2.  **Install Dependencies:**

    ```bash

    composer install

    npm install && npm run build

    ```



3.  **Environment Setup:**

    ```bash

    copy .env.example .env

    php artisan key:generate

*> **Note:** Please open the `.env` file and configure your DB_DATABASE, DB_USERNAME, and DB_PASSWORD.*

Database Migration & Seeding:

php artisan migrate --seed

*This command will set up the database tables and create the default test users listed below.*



## 👤 Access Credentials



| Role | Email | Password |

| :--- | :--- | :--- |

| **Admin** | `admin@test.com` | `password` |

| **Standard User** | `user@test.com` | `password` |



## ⚙️ Legacy Migration Command



To run the idempotent migration for legacy data, use:

```bash

php artisan legacy:migrate-purchases
