# Security Policy

## Supported Versions

This project is actively maintained. Security updates are applied to the latest version. All versions listed below are associated with their corresponding GitHub tag releases.

| Version | Supported |
| ------- | --------- |
| 0.3-DEV | ✅ Yes    |
| 0.2-DEV | ✅ Yes    |
| 0.1-DEV | ✅ Yes    |

---

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly.

**Do not open a public GitHub issue.**

Instead, report it via:

- Email: arjunemithu@gmail.com  
- GitHub Security Advisories (preferred, if enabled)

Please include:

- A description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Any suggested fixes (if available)

You will receive a response within **3–5 business days**.

---

## Security Considerations

### 1. Google Cloud Run Endpoint

This application interacts with a backend hosted on Google Cloud Run for Firestore editing.

**Important safeguards:**

- The Cloud Run URL **must not allow unrestricted public write access**
- Authentication and/or request validation should be enforced
- Avoid exposing sensitive endpoints directly in client-side code where possible

**Recommended protections:**

- Require authenticated requests (e.g., Firebase Auth, OAuth, API Gateway)
- Validate all incoming data on the server
- Use least-privilege IAM roles for Firestore access

---

### 2. Firestore Security

Ensure your Firestore rules:

- Prevent unauthorized reads and writes
- Validate incoming data structure and types
- Restrict access based on authenticated users where applicable

**Example principle:**

```js
allow write: if request.auth != null;