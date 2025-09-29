# Security Policy

## Supported Versions
The private core is under active development. All branches are expected to follow this policy. Critical fixes must be cherry-picked to release branches before deployment.

## Reporting a Vulnerability
- Use the **Security Report** issue template to open a private advisory, or email **security@unseenadvantage.com**.
- Include enough detail to reproduce the issue. Do not share tenant-identifying data, secrets, or exploit code in public channels.
- We aim to acknowledge reports within 48 hours and provide a remediation plan within 5 business days.

## Disclosure Process
1. Report received via private channel.
2. Security team triages severity, assigns an owner, and creates an internal incident record.
3. Fix is developed, reviewed, and merged with appropriate tests.
4. After mitigation, we notify affected tenants and coordinate disclosure if required.

## Coordinated Disclosure
We appreciate responsible disclosure. Please do not publicly disclose vulnerabilities without written consent from Unseen Advantage.

## Hardening Checklist
Contributors must:
- Follow authentication, authorization, and multi-tenant isolation guidelines.
- Keep secrets in approved secret stores (never in source control).
- Review logs for PII before shipping.
- Run the security & privacy checklist in the pull request template before requesting review.