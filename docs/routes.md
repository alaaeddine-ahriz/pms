## **API Routes – Fire-Protection PMS**

*REST/JSON, all paths prefixed by /api/v1 (omitted below for brevity). Authentication via Bearer JWT, responses use standard HTTP codes.*

---

### **0 . Common**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| POST | /auth/login | JWT issuance (email + password). |
| POST | /auth/refresh | Refresh token. |
| GET | /health | Liveness / DB ping. |

---

### **1 . Reference Data**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| GET | /devise | List ISO-4217 currencies. |
| GET | /expense-categories | List categories (CARBURANT, …). |
| GET | /statuts/fabrication | List fabrication statuses. |
| GET | /statuts/livraison | List delivery statuses. |
| GET | /statuts/appro | List supply-request statuses. |

*(reference tables are readonly for most roles; admin CRUD optional)*

---

### **2 . Documents**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| POST | /documents | Upload file (multipart/form-data). |
| GET | /documents/{id} | Metadata & signed URL. |
| DELETE | /documents/{id} | Soft-delete. |
| POST | /documents/{id}/tags | Attach tag(s). |
| DELETE | /documents/{id}/tags/{tagId} | Detach tag. |

---

### **3 . Human Resources**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| GET / POST PATCH | /employees /employees/{id} | CRUD employee. |
| POST | /employees/{id}/documents | Attach CIN, permit, … |
| GET / POST PATCH | /tasks /tasks/{id} | CRUD task. |
| POST | /tasks/{id}/assignees | Add assignee. |
| DELETE | /tasks/{id}/assignees/{empId} | Remove. |
| POST | /tasks/{id}/subtasks | Link child task. |
| POST | /tasks/{id}/documents | Attach doc. |

---

### **4 . Fleet (Vehicles)**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| GET / POST PATCH | /vehicles /vehicles/{id} | CRUD vehicle. |
| POST | /vehicles/{id}/km-log | Add odometer log. |
| POST | /vehicles/{id}/drivers | Assign driver (body: employee_id, date_start). |
| PATCH | /vehicles/{id}/drivers/{empId} | Close assignment (date_end). |

---

### **5 . Materials**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| GET / POST PATCH | /materials /materials/{id} | CRUD matériel. |
| POST | /materials/{id}/documents | Attach doc(s). |

---

### **6 . Products & Stock**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| GET / POST PATCH | /products /products/{id} | CRUD product master. |
| POST | /products/{id}/suppliers | Add supplier. |
| DELETE | /products/{id}/suppliers/{entId} | Remove. |
| GET / POST | /articles /articles/{id} | CRUD SKU. |
| GET / POST | /stocks /stocks/{id} | CRUD warehouse / site stock. |
| GET | /stocks/{id}/inventory | Current quantities (view). |
| POST | /stock-moves | Create double-entry move ↔ validates inventory. Body: article_id, src_stock?, dst_stock?, qty, unit_cost, currency, ref_document. |
| GET | /stock-moves/{id} | Detail. |

---

### **7 . Projects**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| GET / POST PATCH | /projects /projects/{id} | CRUD project. |
| POST | /projects/{id}/vehicles | Link vehicle. |
| POST | /projects/{id}/materials | Link matériel. |
| POST | /projects/{id}/documents | Attach doc. |

### **7.1 Project Cash (Caisse)**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| GET | /projects/{id}/cash/balance | Current balance (computed). |
| POST | /projects/{id}/cash/top-up | **Alimentation** : body amount, currency, fx_rate?, memo. |
| POST | /projects/{id}/cash/expense | **Dépense** : body amount, currency, category_id, memo, receipt_document_id. |
| GET | /projects/{id}/cash/ledger | All ledger lines of the caisse (paginated). |

---

### **8 . Manufacturing**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| GET / POST PATCH | /bom /bom/{id} | CRUD nomenclature. |
| POST | /bom/{id}/products | Add component (product_id, qty). |
| GET / POST PATCH | /orders/fabrication /orders/fabrication/{id} | CRUD order. |
| POST | /orders/fabrication/{id}/bom | Link BOM with qty. |
| POST | /orders/fabrication/{id}/documents | Upload photo avancement/réalisation. |
| PATCH | /orders/fabrication/{id}/status | Update production status. |

---

### **9 . Finance – General Ledger**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| GET | /ledger/accounts | List accounts (readonly except admin). |
| POST | /ledger/lines | Generic double-entry line (non-caisse flows). |
| GET | /ledger/lines/{id} | Detail. |

---

### **10 . Logistics – Deliveries**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| GET / POST PATCH | /deliveries /deliveries/{id} | CRUD delivery (wraps two stock moves). |
| PATCH | /deliveries/{id}/status | Update status. |

---

### **11 . Supply Requests (Approvisionnement)**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| GET / POST PATCH | /supply-requests /supply-requests/{id} | CRUD request. |
| POST | /supply-requests/{id}/products | Add line (product_id, qty). |
| POST | /supply-requests/{id}/tracking | Add tracking event (status_id, comment). |

---

### **12 . Admin & Utilities**

| **Verb** | **Path** | **Purpose** |
| --- | --- | --- |
| POST | /admin/users | Create platform user / role binding. |
| GET | /metrics | Prometheus / OpenTelemetry scrape. |

---

### **Conventions**

- **Pagination**: ?page=&page_size= (default 20).
- **Filtering**: ?q= (full-text), ?status=, ?date_from=, ?date_to=.
- **Idempotency**: supply header Idempotency-Key on POST to guarantee safe retries.
- **Soft-delete**: resources expose deleted_at; DELETE sets it, unless query param ?force=true.

These routes cover CRUD and domain-specific actions while keeping the double-entry invariants for stock and cash intact.