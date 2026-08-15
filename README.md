# Authentication & Authorization Service

A reusable authentication and authorization service built with **FastAPI**, designed to act as the identity layer for multiple backend applications.

The service provides centralized user authentication, JWT-based authorization, refresh-token rotation, password recovery, Google OAuth, email verification, and role-based access control.

The frontend is built with **React** and **Material UI**, while the backend and PostgreSQL database are deployed on **Render**, and the frontend is deployed on **Vercel**.

---

## Table of Contents

- [Overview](#overview)
- [Why This Project?](#why-this-project)
- [Key Features](#key-features)
- [Security](#security)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Authentication Flow](#authentication-flow)
- [Refresh Token Rotation](#refresh-token-rotation)
- [Password Reset Flow](#password-reset-flow)
- [Google OAuth Flow](#google-oauth-flow)
- [Role-Based Access Control](#role-based-access-control)
- [API Areas](#api-areas)
- [Environment Configuration](#environment-configuration)
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [CI/CD with GitHub Actions](#cicd-with-github-actions)
- [Security Considerations](#security-considerations)
- [Rate Limiting](#rate-limiting)
- [Testing](#testing)
- [Frontend Authentication State](#frontend-authentication-state)
- [Project Structure](#project-structure)
- [Deployment Environments](#deployment-environments)
- [Reusability](#reusability)
- [Future Improvements](#future-improvements)
- [Development Philosophy](#development-philosophy)
- [Production Stack at a Glance](#production-stack-at-a-glance)
- [Project Goal](#project-goal)

---

## Overview

This project is designed as a **standalone identity service** rather than authentication logic being duplicated across individual backend projects.

Other applications can rely on this service for:

- User registration and login
- JWT authentication
- Access-token validation
- Refresh-token rotation
- Logout and token revocation
- Password reset using OTP
- Email verification
- Google OAuth authentication
- Role-based access control
- Protected user endpoints
- Admin-only endpoints
- Authentication rate limiting

The main goal is to build authentication once and reuse it across future backend projects.

```
                     ┌─────────────────────┐
                     │     React + MUI      │
                     │       Vercel         │
                     └──────────┬──────────┘
                                │
                                │ HTTPS
                                ▼
                     ┌─────────────────────┐
                     │      FastAPI        │
                     │       Render        │
                     │                     │
                     │ Authentication      │
                     │ Authorization       │
                     │ JWT                 │
                     │ OAuth               │
                     │ Password Reset      │
                     │ RBAC                │
                     └──────────┬──────────┘
                                │
                                │ SQLAlchemy
                                ▼
                     ┌─────────────────────┐
                     │     PostgreSQL      │
                     │       Render        │
                     └─────────────────────┘
```

---

## Why This Project?

Authentication is commonly repeated across backend projects. That creates several problems:

- Authentication logic gets duplicated
- Security fixes must be applied to multiple projects
- User management becomes inconsistent
- Token handling differs between applications
- Password-reset implementations get recreated repeatedly
- OAuth integrations have to be maintained separately
- Authorization rules become difficult to standardize

This project solves that by providing a central authentication and identity service. Instead of implementing authentication independently in every application:

```
Project A ─────┐
Project B ─────┤
Project C ─────┼──────> Authentication Service
Project D ─────┤
Project E ─────┘
```

Each backend can use the same identity layer, making authentication easier to maintain, secure, test, and extend.

---

## Key Features

### Authentication
- User signup
- User login
- Password hashing
- Password verification
- JWT access tokens
- Refresh tokens
- Refresh-token rotation
- Logout
- Token revocation

### Account Recovery
- Forgot password
- OTP generation
- OTP hashing
- OTP expiration
- OTP verification
- Password reset
- Used-OTP protection

### Email
- Email verification
- Password-reset emails
- SMTP integration

### Google OAuth
- Google OAuth login
- Google identity verification
- Existing-user lookup
- Automatic user creation for new Google accounts

### Authorization
- Role-based access control
- User role management
- Protected routes
- Admin-only endpoints

Example:

```
User
└── authenticated

Admin
└── authenticated
└── admin permissions
```

---

## Security

- Password hashing
- JWT signature verification
- Refresh-token rotation
- Refresh-token revocation
- Short-lived access tokens
- Expiring password-reset OTPs
- Rate limiting
- Environment-based secrets
- Protected admin routes

---

## Tech Stack

### Backend

| Technology | Purpose |
|---|---|
| FastAPI | REST API framework |
| Python | Backend language |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database interaction |
| JWT | Access-token authentication |
| python-jose | JWT creation and verification |
| Passlib | Password hashing and verification |
| Authlib | Google OAuth integration |
| SlowAPI | API rate limiting |
| SMTP | Email delivery |
| Pytest | Backend testing |

### Frontend

| Technology | Purpose |
|---|---|
| React | Frontend framework |
| Material UI | UI component library |
| Axios | HTTP client |
| React Router | Client-side routing |

### Infrastructure

| Technology | Purpose |
|---|---|
| Render | Backend deployment |
| Render PostgreSQL | Production database |
| Vercel | Frontend deployment |
| GitHub | Source control |
| GitHub Actions | CI/CD |

---

## Architecture

The project follows a layered backend architecture:

```
Request
  │
  ▼
Route
  │
  ▼
Service
  │
  ├── Security
  ├── Token Management
  ├── OAuth
  ├── OTP
  └── Business Logic
  │
  ▼
SQLAlchemy
  │
  ▼
PostgreSQL
```

The frontend communicates with the FastAPI API over HTTPS.

- The **backend** is responsible for authentication, authorization, token management, database operations, OAuth, and email-related workflows.
- The **frontend** is responsible for the user interface and maintaining the authenticated application state.

---

## Authentication Flow

### Signup

```
User
  │
  │ signup
  ▼
FastAPI
  │
  ├── Validate input
  ├── Check existing email
  ├── Hash password
  ├── Create user
  └── Send verification email
  │
  ▼
PostgreSQL
```

### Login

```
User
  │
  │ email + password
  ▼
FastAPI
  │
  ├── Find user
  ├── Verify password
  ├── Create access token
  └── Create refresh token
  │
  ▼
Frontend
```

### Access Token

The frontend sends the access token when accessing protected API endpoints:

```
Authorization: Bearer <access_token>
```

The backend validates the JWT before allowing access to protected resources.

---

## Refresh Token Rotation

Access tokens are intentionally short-lived. When an access token expires, the frontend can use the refresh token to obtain a new token pair.

```
Access Token
  │
  │ expires
  ▼
Refresh Token
  │
  ▼
Validate
  │
  ├── valid ──> revoke old refresh token
  │               │
  │               ▼
  │         create new tokens
  │
  └── invalid ──> authentication required
```

Refresh tokens are stored securely in the database using a hash rather than storing the raw token. This allows individual refresh tokens to be revoked.

---

## Password Reset Flow

Password recovery is handled through an OTP-based workflow.

```
Forgot Password
  │
  ▼
Enter Email
  │
  ▼
Generate OTP
  │
  ▼
Hash OTP
  │
  ▼
Store OTP + Expiry
  │
  ▼
Send OTP via Email
  │
  ▼
Verify OTP
  │
  ▼
Set New Password
  │
  ▼
Mark OTP as Used
```

OTP records are temporary and expire after a configured period.

---

## Google OAuth Flow

Google authentication is handled using Authlib.

```
Frontend
  │
  │ Login with Google
  ▼
FastAPI
  │
  ▼
Google OAuth
  │
  ▼
Google Callback
  │
  ├── Existing user?
  │     │
  │     ├── Yes → Login
  │     │
  │     └── No → Create user
  │
  ▼
Issue JWT tokens
  │
  ▼
Frontend
```

---

## Role-Based Access Control

The service supports role-based authorization. For example:

- `user`
- `admin`

A normal authenticated user can access:

```
GET /me
```

An administrator can access:

```
GET /admin/users
```

Authorization is handled separately from authentication.

- **Authentication** answers: *Who are you?*
- **Authorization** answers: *What are you allowed to do?*

---

## API Areas

The API is organized into authentication, password recovery, OAuth, and user-management areas.

### Authentication
```
POST /signup
POST /login
POST /refresh
POST /logout
```

### Password Reset
```
POST /forgot-password
POST /verify-otp
POST /reset-password
```

### Google OAuth
```
GET /auth/google
GET /auth/google/callback
```

### Users
```
GET /me
GET /admin/users
```

The exact request and response schemas are documented through FastAPI's generated API documentation. When running locally:

```
/api/docs
```

---

## Environment Configuration

The application uses environment variables for configuration and secrets. Sensitive values should never be committed to GitHub.

Typical configuration includes:

```env
DATABASE_URL=

JWT_SECRET_KEY=
JWT_ALGORITHM=

ACCESS_TOKEN_EXPIRE_MINUTES=
REFRESH_TOKEN_EXPIRE_DAYS=

SMTP_HOST=
SMTP_PORT=
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=

FRONTEND_URL=
```

The exact variable names should match the application's `config.py`. An `.env.example` file is included as a reference.

---

## Local Development

### Backend

Clone the repository and create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows**
```bash
.venv\Scripts\activate
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the environment variables using `.env`.

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The API will be available locally at:

```
http://localhost:8000
```

FastAPI documentation:

```
http://localhost:8000/docs
```

### Frontend Development

Install dependencies:

```bash
npm install
```

Configure the frontend environment variables.

Start the development server:

```bash
npm run dev
```

The React application will then run locally. The frontend communicates with the FastAPI backend through the configured API base URL.

### Database

The project uses PostgreSQL with SQLAlchemy. Development can use a local PostgreSQL installation or another PostgreSQL instance. Production uses **Render PostgreSQL**.

The backend connects to PostgreSQL using the configured `DATABASE_URL`.

The database contains the core identity data, including:

- Users
- Refresh Tokens
- Password Reset Records

---

## Production Deployment

The production architecture is intentionally simple.

```
GitHub
  │
  ├───────────────┐
  │               │
  ▼               ▼
Vercel          Render
Frontend        Backend
React + MUI     FastAPI
  │               │
  │               ▼
  │         Render PostgreSQL
  │
  └──── HTTPS ────┘
```

### Frontend

The React application is deployed to **Vercel**. Vercel builds and serves the frontend application.

The frontend contains the production API URL as an environment variable, for example:

```env
VITE_API_URL=https://your-backend.onrender.com
```

### Backend

The FastAPI application is deployed to **Render**. Render runs the production API server and exposes it through HTTPS.

The backend receives its secrets and configuration through Render environment variables.

### Database

PostgreSQL is hosted through **Render PostgreSQL**. The production backend connects to the Render PostgreSQL instance through the configured database connection string.

---

## CI/CD with GitHub Actions

This project uses GitHub Actions instead of Docker-based deployment workflows.

There are two separate workflows:

```
.github/
└── workflows/
    ├── fe-ci.yml
    └── be-ci.yml
```

The workflows keep frontend and backend validation independent.

### Backend CI

The backend CI workflow is responsible for validating the FastAPI application.

Typical backend CI stages:

```
Push / Pull Request
  │
  ▼
Checkout repository
  │
  ▼
Setup Python
  │
  ▼
Install dependencies
  │
  ▼
Run tests
  │
  ▼
CI Passed
```

The backend CI should run automatically when backend-related code changes.

Typical checks include:

- Python environment setup
- Dependency installation
- Automated tests
- Authentication tests
- Password-reset tests
- RBAC tests

A failing test causes the GitHub Actions workflow to fail. This prevents broken backend changes from being treated as production-ready.

### Frontend CI

The frontend CI workflow validates the React application.

Typical flow:

```
Push / Pull Request
  │
  ▼
Checkout repository
  │
  ▼
Setup Node.js
  │
  ▼
Install dependencies
  │
  ▼
Build frontend
  │
  ▼
CI Passed
```

Typical checks include:

- Node.js setup
- Dependency installation
- Frontend build
- Linting, if configured
- Frontend tests, if configured

A failed build causes the GitHub Actions workflow to fail.

### Continuous Deployment

Deployment is handled by the hosting platforms. The overall workflow is:

```
Developer
  │
  ▼
Git Push
  │
  ▼
GitHub
  │
  ├───────────────┐
  │               │
  ▼               ▼
 BE CI           FE CI
  │               │
  ▼               ▼
Render          Vercel
Backend         Frontend
  │
  ▼
Render PostgreSQL
```

The recommended deployment strategy is:

```
Pull Request
  │
  ▼
GitHub Actions
  │
  ├── Backend CI
  └── Frontend CI
  │
  ▼
Merge to main
  │
  ├── Render deploys backend
  └── Vercel deploys frontend
```

This keeps CI responsible for validation while the hosting platforms handle deployment.

### GitHub Actions Responsibilities

The responsibilities are intentionally separated.

| Component | Responsibility |
|---|---|
| GitHub | Source control |
| GitHub Actions | CI |
| Render | Backend deployment |
| Render PostgreSQL | Production database |
| Vercel | Frontend deployment |

GitHub Actions does not need to build or manage Docker containers for this project.

---

## Security Considerations

Authentication infrastructure requires careful handling of sensitive data.

Important rules:

- Never commit `.env` files
- Never commit JWT secrets
- Never commit Google OAuth secrets
- Never commit SMTP passwords
- Never store plaintext passwords
- Never store plaintext refresh tokens
- Never store plaintext password-reset OTPs
- Use HTTPS in production
- Keep access tokens short-lived
- Rotate refresh tokens
- Revoke refresh tokens during logout
- Expire password-reset OTPs
- Prevent OTP reuse
- Rate-limit authentication endpoints
- Protect admin endpoints with RBAC
- Validate all authentication inputs
- Keep production secrets in Render/Vercel environment variables

---

## Rate Limiting

Authentication endpoints are protected using SlowAPI.

Rate limiting is particularly important for endpoints such as:

```
/login
/signup
/forgot-password
/verify-otp
/reset-password
```

This helps reduce:

- Brute-force password attempts
- OTP abuse
- Automated account creation
- Password-reset abuse

Rate limits should be configured according to the application's expected traffic.

---

## Testing

The backend contains tests for the most important authentication workflows.

The test suite covers areas such as:

- Authentication
- Password Reset
- RBAC

Tests should run as part of backend CI. A change should not be considered ready for deployment if the CI test suite fails.

---

## Frontend Authentication State

The frontend maintains authentication state through `AuthContext`.

The authentication context is responsible for concepts such as:

- Current user
- Access token
- Login
- Logout
- Authentication state

Axios interceptors handle API authentication and token-refresh behavior.

Protected pages use `ProtectedRoute` to prevent unauthenticated users from accessing authenticated application routes.

Example:

```
                ┌── Login
                │
User ── Protected ──┤
                │
                └── Dashboard
```

Admin pages additionally depend on the user's role.

---

## Project Structure

The project intentionally does not document a large folder-by-folder tree here. The important architectural separation is:

```
Frontend
  │
  ├── Pages
  ├── Components
  ├── Authentication State
  └── API Client

Backend
  │
  ├── Routes
  ├── Services
  ├── Models
  ├── Schemas
  ├── Security
  └── Database

Infrastructure
  │
  ├── GitHub Actions
  ├── Vercel
  ├── Render
  └── Render PostgreSQL
```

The codebase should remain organized around responsibilities rather than making the README depend on every individual file.

---

## Deployment Environments

The project can be thought of as two environments.

### Development

```
React
  │
  ▼
Local FastAPI
  │
  ▼
Development PostgreSQL
```

### Production

```
Vercel
  │
  ▼
Render FastAPI
  │
  ▼
Render PostgreSQL
```

This separation prevents local development configuration from being mixed with production infrastructure.

---

## Reusability

The main purpose of this project is to make authentication reusable. Future backend projects can integrate with the service instead of implementing authentication independently.

For example:

```
Authentication Service
  │
  ├────────── URL Shortener
  │
  ├────────── E-commerce API
  │
  ├────────── Task Management API
  │
  ├────────── Social Platform API
  │
  └────────── Future Projects
```

This creates a centralized identity layer that can evolve independently of individual applications.

---

## Future Improvements

Possible future improvements include:

- Email verification enforcement
- Account lockout policies
- Device/session management
- Multi-factor authentication
- More granular permissions
- OAuth provider expansion
- Audit logging
- Token/session monitoring
- Admin user management
- Security event logging
- API versioning
- Automated database migrations
- Production monitoring
- Error tracking

These should be introduced based on the requirements of applications consuming the identity service.

---

## Development Philosophy

The project follows a few important principles:

**Authentication should be centralized**
Applications should not repeatedly implement password hashing, JWT validation, refresh-token handling, and OAuth.

**Security should be explicit**
Authentication code should prioritize secure defaults and clear boundaries.

**Services should contain business logic**
Routes should primarily handle HTTP concerns while services contain authentication workflows.

**Frontend and backend should remain independent**
The React application communicates with the FastAPI API through HTTP rather than coupling frontend logic to backend implementation details.

**CI should catch problems before deployment**
GitHub Actions validates changes before they become production deployments.

**Infrastructure should remain simple**
Vercel handles the frontend, Render handles the backend and PostgreSQL, and GitHub Actions handles CI.

---

## Production Stack at a Glance

```
Frontend
React + Material UI
  │
  │ HTTPS
  ▼
Vercel
  │
  │ API requests
  ▼
FastAPI
  │
  ├── JWT
  ├── OAuth
  ├── RBAC
  ├── Password Reset
  ├── OTP
  ├── Rate Limiting
  │
  ▼
SQLAlchemy
  │
  ▼
Render PostgreSQL
```

CI/CD:

```
GitHub
  │
  ├── fe-ci
  │     └── Frontend validation
  │
  └── be-ci
        └── Backend validation

main
  │
  ├── Vercel → Frontend deployment
  │
  └── Render → Backend deployment
```

---

## Project Goal

This service is intended to become the central identity layer for future backend applications.

The objective is not simply to build a login system. The objective is to build a reusable authentication platform that provides a consistent, secure, and maintainable identity layer across multiple applications.

> **Build Authentication Once. Reuse It Everywhere.**
