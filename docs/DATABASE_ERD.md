# CampusFix - Database Entity-Relationship Diagram (ERD) & Schema Specification
**National Taipei University / Software Engineering (Team 04)**  
**Storage Engine**: SQLite 3 (ACID Compliant) | **Database File**: `campusfix.db`

---

## 1. Conceptual Entity-Relationship Diagram (Mermaid)

The diagram below visualizes the persistent `REPORTS` table alongside the domain and lookup entities (`DEMO_USERS`, `LOCATIONS`, `CATEGORIES`):

```mermaid
erDiagram
    %% Core Persistent Table in SQLite
    REPORTS {
        INTEGER id PK "Primary Key (Autoincrement)"
        TEXT report_id UK "Unique Identifier (e.g. CF-1001)"
        TEXT title "Problem Title"
        TEXT location "Campus Building Location"
        TEXT category "Incident Classification"
        TEXT description "Detailed Description"
        TEXT status "Submitted | In Progress | Resolved"
        TEXT resolution_note "Mandatory on Resolution"
        TEXT created_at "Timestamp of Submission"
        TEXT updated_at "Timestamp of Status Update"
    }

    %% Conceptual Lookup / Domain Entities
    LOCATIONS {
        TEXT location_name PK "Campus Building Name"
        TEXT campus_area "Sanxia Main Campus | Taipei Campus"
    }

    CATEGORIES {
        TEXT category_name PK "Equipment | Facility | Wi-Fi | Plumbing"
        TEXT default_priority "Low | Medium | High"
    }

    DEMO_USERS {
        TEXT email PK "student@ntpu.edu.tw | staff@ntpu.edu.tw"
        TEXT role "student | staff"
        TEXT name "Demonstration Account Name"
        TEXT department "CSIE Department | Office of General Affairs"
    }

    %% Relationships
    DEMO_USERS ||--o{ REPORTS : "submits or updates (via session)"
    LOCATIONS ||--o{ REPORTS : "specifies physical location of"
    CATEGORIES ||--o{ REPORTS : "classifies incident type of"
```

---

## 2. Physical SQLite Schema (Data Definition Language)

The physical table is created idempotently on server startup in [`database.py`](file:///C:/Users/phone/.gemini/antigravity/scratch/campusfix/database.py):

```sql
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Submitted',
    resolution_note TEXT DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

### Physical ER Diagram

```mermaid
erDiagram
    REPORTS {
        INTEGER id PK "Primary Key (AUTOINCREMENT)"
        TEXT report_id UK "UNIQUE NOT NULL (e.g. CF-1001)"
        TEXT title "NOT NULL"
        TEXT location "NOT NULL"
        TEXT category "NOT NULL"
        TEXT description "NOT NULL"
        TEXT status "NOT NULL DEFAULT 'Submitted'"
        TEXT resolution_note "DEFAULT ''"
        TEXT created_at "NOT NULL (YYYY-MM-DD HH:MM:SS)"
        TEXT updated_at "NOT NULL (YYYY-MM-DD HH:MM:SS)"
    }
```

---

## 3. Data Dictionary & Field Specifications

| Column Name | SQLite Type | Constraints | Description & Agile Traceability |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Internal database surrogate key for fast index lookups and row addressing. |
| `report_id` | `TEXT` | `UNIQUE NOT NULL` | **CF-12**: Human-readable incident identifier formatted as `CF-1001`, `CF-1002`. Monotonically assigned upon insert. |
| `title` | `TEXT` | `NOT NULL` | **CF-10, CF-11**: Concise problem summary. Validated to prevent empty strings or whitespace-only bypasses. |
| `location` | `TEXT` | `NOT NULL` | **CF-10, CF-22**: Campus building/facility. Used for location filtering dropdown with combined `AND` logic. |
| `category` | `TEXT` | `NOT NULL` | **CF-10**: Problem type (`Classroom Equipment`, `Damaged Facilities`, `Wi-Fi Failures`, `Plumbing & Restroom`, `Other`). |
| `description` | `TEXT` | `NOT NULL` | **CF-10, CF-21**: Detailed description. Indexed and queried case-insensitively using `LOWER(description) LIKE ?`. |
| `status` | `TEXT` | `NOT NULL DEFAULT 'Submitted'` | **CF-14, CF-30**: Lifecycle state. Permitted values strictly: `'Submitted'`, `'In Progress'`, `'Resolved'`. |
| `resolution_note`| `TEXT` | `DEFAULT ''` | **CF-31**: Official staff repair notes. Mandatory (non-empty) when transitioning status to `'Resolved'`. |
| `created_at` | `TEXT` | `NOT NULL` | **CF-13**: ISO timestamp recorded upon submission (`YYYY-MM-DD HH:MM:SS`). |
| `updated_at` | `TEXT` | `NOT NULL` | **CF-30**: ISO timestamp updated whenever staff modifies status or appends notes. |

---

## 4. Lifecycle State Transitions

```mermaid
stateDiagram-v2
    [*] --> Submitted : Student Submits Report (CF-10)
    Submitted --> InProgress : Staff Reviews & Dispatches Work (CF-30)
    InProgress --> Resolved : Staff Completes Repair + Mandatory Note (CF-31)
    Submitted --> Resolved : Direct Resolution + Mandatory Note (CF-31)
    Resolved --> InProgress : Reopened if Issue Persists (Staff Role)
```
