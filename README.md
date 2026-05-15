# Full Stack FastAPI Template

<a href="https://github.com/fastapi/full-stack-fastapi-template/actions?query=workflow%3A%22Test+Docker+Compose%22" target="_blank"><img src="https://github.com/fastapi/full-stack-fastapi-template/workflows/Test%20Docker%20Compose/badge.svg" alt="Test Docker Compose"></a>
<a href="https://github.com/fastapi/full-stack-fastapi-template/actions?query=workflow%3A%22Test+Backend%22" target="_blank"><img src="https://github.com/fastapi/full-stack-fastapi-template/workflows/Test%20Backend/badge.svg" alt="Test Backend"></a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/full-stack-fastapi-template" target="_blank"><img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/full-stack-fastapi-template.svg" alt="Coverage"></a>

## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
  - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
  - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
- 🚀 [React](https://react.dev) for the frontend.
  - 💃 Using TypeScript, hooks, [Vite](https://vitejs.dev), and other parts of a modern frontend stack.
  - 🎨 [Tailwind CSS](https://tailwindcss.com) and [shadcn/ui](https://ui.shadcn.com) for the frontend components.
  - 🤖 An automatically generated frontend client.
  - 🧪 [Playwright](https://playwright.dev) for End-to-End testing.
  - 🦇 Dark mode support.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT (JSON Web Token) authentication.
- 📫 Email based password recovery.
- 📬 [Mailcatcher](https://mailcatcher.me) for local email testing during development.
- ✅ Tests with [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) as a reverse proxy / load balancer.
- 🚢 Deployment instructions using Docker Compose, including how to set up a frontend Traefik proxy to handle automatic HTTPS certificates.
- 🏭 CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.

### Dashboard Login

[![API docs](img/login.png)](https://github.com/fastapi/full-stack-fastapi-template)

### Dashboard - Admin

[![API docs](img/dashboard.png)](https://github.com/fastapi/full-stack-fastapi-template)

### Dashboard - Items

[![API docs](img/dashboard-items.png)](https://github.com/fastapi/full-stack-fastapi-template)

### Dashboard - Dark Mode

[![API docs](img/dashboard-dark.png)](https://github.com/fastapi/full-stack-fastapi-template)

### Interactive API Documentation

[![API docs](img/docs.png)](https://github.com/fastapi/full-stack-fastapi-template)

## 🔐 Role-Based Access Control (RBAC) Architecture

The project implements a comprehensive RBAC system with three primary roles: **Admin**, **Manager**, and **Member**.

### Permission Matrix

| Action             | Admin | Manager | Member |
|--------------------|-------|---------|--------|
| List all users     | ✓     | ✓       | ✗      |
| Create user        | ✓     | ✗       | ✗      |
| View metrics       | ✓     | ✓       | ✗      |
| Manage own items   | ✓     | ✓       | ✓      |
| Update own profile | ✓     | ✓       | ✓      |
| Update any profile | ✓     | ✗       | ✗      |

### Implementation Approach

**Role Storage and Validation**
User roles are strictly defined at the database layer using a SQLModel Enum (`UserRole`). When a user authenticates, the backend decodes their JWT access token and attaches the fully hydrated user object—including their verified role—to the request state. This ensures that role claims cannot be forged or manipulated by the client. 

**Backend Authorization (Where Checks Live)**
To maintain the Single Responsibility Principle and keep the core route logic clean, authorization checks live entirely within **FastAPI Dependencies**. We implemented a dynamic dependency factory called `VerifyRole`. Instead of hardcoding checks inside the route handlers, we inject the requirement directly into the route decorator (e.g., `dependencies=[Depends(VerifyRole([UserRole.ADMIN]))]`). If a user attempts to access an endpoint outside their scope, the dependency intercepts the request and immediately throws a `403 Forbidden` exception before the route logic ever executes.

**Frontend Capabilities and UX**
The frontend framework learns about user capabilities dynamically upon initialization. Using TanStack Router's `beforeLoad` lifecycle and React Query, the client fetches the current user's profile from `/api/v1/users/me` and hydrates a global `useAuth` hook. The UI then uses this `currentUser.role` state to conditionally render the interface. For example, if a Manager logs in, they are permitted to see the Admin directory table, but the React components for the "+ Add User" button and the row-level Action Menus return `null`, physically removing the capability from the DOM. Direct navigation to protected routes (like `/admin` or `/metrics` for Members) is intercepted by the router, which redirects unauthorized users back to the dashboard.

## How To Use It
You can **just fork or clone** this repository and use it as is.

✨ It just works. ✨

### How to Use a Private Repository

If you want to have a private repository, GitHub won't allow you to simply fork it as it doesn't allow changing the visibility of forks.

But you can do the following:

- Create a new GitHub repo, for example `my-full-stack`.
- Clone this repository manually, set the name with the name of the project you want to use, for example `my-full-stack`:

```bash
git clone git@github.com:fastapi/full-stack-fastapi-template.git my-full-stack

## 👨‍💻 Developer UX & Reviewer Guide

Welcome! We've made it as frictionless as possible to run, evaluate, and test this RBAC implementation locally.

### 1. How to Run Locally
Ensure Docker is running on your machine.
```bash
docker compose up -d --build