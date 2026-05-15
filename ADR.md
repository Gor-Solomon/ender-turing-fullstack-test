## 🏗 Architecture Decision Records (ADRs)

### ADR 001: Dynamic Dependency Injection for RBAC Authorization
**Date:** 2026-05-15
**Status:** Accepted

**Problem:** As the application scales, we need a way to enforce Role-Based Access Control (RBAC) across dozens of FastAPI endpoints. Hardcoding individual role checks inside route handlers violates the Single Responsibility Principle, and creating static dependencies (e.g., `RequireAdmin`, `RequireManager`) leads to code duplication and rigid architecture when new roles are introduced.

**Options Considered:**
1. **Inline Route Checks:** `if user.role != "admin": raise 403`. (High duplication, difficult to audit).
2. **Static Dependencies:** Dedicated functions like `RequireAdmin`. (Requires writing a new function for every new role/combination).
3. **Dynamic Dependency Factory:** A centralized class `VerifyRole(allowed_roles=[...])` injected into the router.

**Decision:** We chose **Option 3 (Dynamic Dependency Factory)**. We implemented a `VerifyRole` dependency that accepts a list of allowed `UserRole` enums. 

**Trade-offs:**
While it requires a slightly deeper understanding of FastAPI's dependency injection system, it makes the routing files entirely self-documenting (e.g., `dependencies=[Depends(VerifyRole([UserRole.ADMIN, UserRole.MANAGER]))]`). Adding a new role requires zero changes to the core security logic, making the system highly extensible.

---

### ADR 002: Backend-Authoritative RBAC with Frontend Progressive Enhancement
**Date:** 2026-05-15
**Status:** Accepted

**Problem:** How should we handle unauthorized access? Relying solely on the frontend to hide pages is inherently insecure, while relying solely on the backend results in a frustrating User Experience (UX) where users constantly click buttons only to receive `403 Forbidden` errors.

**Options Considered:**
1. **Frontend-Only Protection:** Hide UI elements based on state. (Easily bypassed via direct API calls).
2. **Backend-Only Protection:** Block API requests but leave all UI elements visible. (Frustrating UX).
3. **Hybrid Model:** Backend acts as the ultimate source of truth; Frontend adapts the UI based on backend claims.

**Decision:** We chose **Option 3 (Hybrid Model)**. The backend issues a JWT containing the user's ID. The frontend fetches the user's profile (including their verified `role`) from the backend on load. The React UI uses this role to conditionally hide sensitive elements (like the "+ Add User" button or delete actions). Meanwhile, the backend `VerifyRole` dependency acts as the absolute shield, rejecting any unauthorized API requests even if the frontend is bypassed.

**Trade-offs:**
This requires maintaining the "knowledge" of the permission matrix in two places (the React components and the FastAPI routes). However, it provides the ultimate balance of bulletproof security and excellent UX.

---

## 🗺 Authorization Flow Diagram

The following diagram illustrates where Authentication (AuthN) and Authorization (AuthZ) checks occur in the request lifecycle:

```mermaid
sequenceDiagram
    actor User
    participant Frontend as React Client
    participant Router as FastAPI Router
    participant AuthZ as VerifyRole (Dependency)
    participant DB as PostgreSQL

    User->>Frontend: Clicks "Delete User" (If Visible)
    Frontend->>Router: DELETE /api/v1/users/{id}
    
    Note over Router,AuthZ: AuthN & AuthZ Phase
    Router->>AuthZ: Pass JWT Token & Route Requirements
    AuthZ->>DB: Fetch Current User (AuthN)
    DB-->>AuthZ: Return User Object (Role: Manager)
    
    AuthZ->>AuthZ: Check Role against [ADMIN] (AuthZ)
    
    alt Role Not Allowed
        AuthZ-->>Frontend: 403 Forbidden Exception
        Frontend-->>User: Display Error Toast
    else Role Allowed
        AuthZ->>Router: Proceed to Route Logic
        Router->>DB: Execute Delete Query
        DB-->>Router: Success
        Router-->>Frontend: 200 OK
    end