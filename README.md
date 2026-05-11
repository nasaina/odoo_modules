# Odoo 19 — Bank Audit Module

Containerized Odoo 19 environment with a custom module for managing bank audit missions.

## Tech Stack

| Component | Version |
|-----------|---------|
| Odoo      | 19      |
| PostgreSQL | 15     |
| Docker Compose | v2 |

## Project Structure

```
odoo/
├── custom_addons/
│   └── audit_bancaire/           # Custom module
│       ├── models/
│       │   └── models.py         # audit.mission model
│       ├── views/
│       │   └── views.xml         # Form and list views
│       ├── report/
│       │   └── audit_mission_report.xml  # QWeb PDF template
│       ├── security/
│       │   └── ir.model.access.csv       # Access rights
│       └── __manifest__.py
├── config_odoo/
│   └── odoo.conf                 # Odoo configuration (addons_path, db, etc.)
├── docs/
│   └── troubleshooting.md        # Troubleshooting guide
├── docker-compose.yml
├── Makefile
└── README.md
```

## Quick Start

```bash
# 1. Start the containers
make up

# 2. Initialize the database (first time only)
make init

# 3. Access Odoo
# http://localhost:8029
# Login: admin / admin
```

## Make Commands

| Command | Description |
|---------|-------------|
| `make up` | Start containers in detached mode |
| `make down` | Stop containers |
| `make restart` | Restart all services |
| `make clean` | Stop containers and remove local images |
| `make fclean` | Full cleanup (containers + volumes + all data) |
| `make re` | `fclean` + `up` + `init` |
| `make init` | Initialize the Odoo database |

> ⚠️ `make fclean` and `make re` **permanently delete all data**.

## Module: audit_bancaire

### Model `audit.mission`

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Mission reference (required) |
| `date_audit` | Date | Audit start date |
| `date_fin` | Date | End date (auto-filled on completion) |
| `entite_audit` | Char | Audited branch or department |
| `auditeur_id` | Many2one | Assigned auditor (defaults to current user) |
| `statut` | Selection | `draft` → `in_progress` → `done` |
| `observations` | Text | Audit conclusion |

### Workflow

```
[Draft] --"Start Audit"--> [In Progress] --"Finalize Audit"--> [Done]
                                                                   |
                                                         "Reset to Draft"
                                                         "Generate PDF"
```

### Install / Update the Module

1. Go to **Apps** → search for `audit_bancaire`
2. Click **Install** or **Update**
3. The **Audit Bancaire** menu appears in the main navigation

> If the module does not appear: **Apps** → **Update Apps List** → remove the "Apps" filter → search for `audit_bancaire`.

## Adding a Custom Module

1. Create a folder inside `custom_addons/`
2. Restart Odoo: `make restart`
3. In Odoo: **Apps** → **Update Apps List**
4. Install the module

## Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md) for common errors:
- 500 error on startup (uninitialized database)
- Module not found in Apps list
- Volume permission errors
- Odoo version upgrade (17 → 19)

## Odoo 19 Breaking Changes

| Change | Old syntax | New syntax |
|--------|-----------|------------|
| List view tag | `<tree>` | `<list>` |
| Conditional visibility | `states="draft"` | `invisible="statut != 'draft'"` |
| Dynamic attributes | `attrs="{...}"` | Direct `invisible=`, `required=`, `readonly=` |
