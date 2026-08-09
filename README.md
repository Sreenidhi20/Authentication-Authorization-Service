# Authentication-Authorization-Service
I will design an auth service and reuse it as the identity layer across my other backend projects.

**Stack:** FastAPI + PostgreSQL + SQLAlchemy + JWT (python-jose) + passlib + Authlib (Google OAuth) + slowapi (rate limiting)
**Frontend:** React + Tailwind
**Deploy:** Vercel (FE) + Render (BE) — same pattern as the URL Shortener project

---

## Folder structure — Backend

```
auth-service/
├── app/
│   ├── main.py                 # FastAPI app entrypoint, lifespan, router includes
│   ├── config.py                 # env vars: DB URL, JWT secret, SMTP creds, Google OAuth keys
│   ├── database.py                 # SQLAlchemy engine/session
│   ├── models/
│   │   ├── user.py                   # User table (id, name, email, hashed_password, role, is_verified)
│   │   ├── refresh_token.py            # RefreshToken table (token_hash, user_id, expires_at, revoked)
│   │   └── password_reset.py             # PasswordReset table (otp_hash, user_id, expires_at, used)
│   ├── schemas/
│   │   ├── user.py                   # SignupRequest, LoginRequest, UserResponse
│   │   ├── token.py                    # TokenResponse (access_token, refresh_token)
│   │   └── password_reset.py             # ForgotPasswordRequest, VerifyOtpRequest, ResetPasswordRequest
│   ├── routes/
│   │   ├── auth.py                   # /signup, /login, /refresh, /logout
│   │   ├── password_reset.py           # /forgot-password, /verify-otp, /reset-password
│   │   ├── oauth.py                    # /auth/google, /auth/google/callback
│   │   └── users.py                    # /me, /admin/users (RBAC-protected)
│   ├── services/
│   │   ├── auth_service.py             # signup/login logic, password verification
│   │   ├── token_service.py              # JWT creation/verification, refresh token rotation
│   │   ├── otp_service.py                # OTP generation, hashing, email sending
│   │   └── oauth_service.py              # Google OAuth token exchange, user lookup/creation
│   ├── core/
│   │   ├── security.py                 # password hashing helpers, JWT decode dependency
│   │   ├── permissions.py                # RBAC dependency (require_role("admin"))
│   │   └── rate_limit.py                 # slowapi limiter config
│   └── utils/
│       └── email.py                    # SMTP send helper
├── tests/
│   ├── test_auth.py
│   ├── test_password_reset.py
│   └── test_rbac.py
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Folder structure — Frontend

```
auth-frontend/
├── src/
│   ├── pages/
│   │   ├── SignupPage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── ForgotPasswordPage.jsx      # enter email
│   │   ├── VerifyOtpPage.jsx             # enter OTP
│   │   ├── ResetPasswordPage.jsx           # set new password
│   │   ├── DashboardPage.jsx               # protected — shows user info
│   │   └── AdminPage.jsx                     # protected — admin-only, RBAC demo
│   ├── components/
│   │   ├── ProtectedRoute.jsx            # wraps routes, checks auth state
│   │   ├── GoogleSignInButton.jsx
│   │   └── FormInput.jsx
│   ├── context/
│   │   └── AuthContext.jsx               # holds user, access token, login/logout functions
│   ├── services/
│   │   └── api.js                        # axios instance with interceptor for token refresh
│   ├── App.jsx
│   └── main.jsx
├── .env.example
└── package.json
```


