# Task 2: Kubernetes Network Policy Implementation

## Scenario

A multi-tenant SaaS platform requires network isolation between customer environments.  
Each tenant’s services must be isolated from others, with exceptions for shared services like authentication and logging.

The deployment consists of 3 services:

1. **Frontend**
   - Runs in `frontend` namespace
   - Labels: `app=frontend`, `env=prod`
   - Listens on port `80`
   - Needs to access the **Backend** on port `8080`

2. **Backend**
   - Runs in `backend` namespace
   - Labels: `app=backend`, `env=prod`
   - Listens on port `8080`
   - Needs to access the **Database** on port `5432`

3. **Database**
   - Runs in `backend` namespace
   - Labels: `app=database`, `env=prod`
   - Listens on port `5432`
   - Must only accept connections from the **Backend**

Additionally:
- All pods must be able to communicate with **monitoring services** in the `monitoring` namespace on port `9020`
- All **unnecessary traffic must be blocked**

---

## Deliverables

This folder includes three Kubernetes NetworkPolicy YAML files:

| File | Description |
|------|-------------|
| `frontend-network-policy.yaml` | Allows frontend pods to egress only to backend pods on port 8080 and to monitoring on port 9020 |
| `backend-network-policy.yaml` | Allows ingress from frontend on port 8080, egress to database (5432) and monitoring (9020) |
| `database-network-policy.yaml` | Restricts ingress to database pods, allowing only backend pods on port 5432 |

---

## Security Logic

The policies are designed to:

- Enforce strict traffic flow (frontend → backend → database)
- Prevent unauthorized access (e.g., frontend directly accessing the database)
- Allow observability through egress to monitoring
- Block all other traffic implicitly

---

## Assumptions

- Namespaces `frontend`, `backend`, and `monitoring` exist and have appropriate `name` labels for namespaceSelector matching
- Pods are labeled exactly as described in the task (`app` and `env` labels)
- Monitoring pods have a label `app=monitoring-app`