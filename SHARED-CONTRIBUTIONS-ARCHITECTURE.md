# Shared contribution service: implementation requirements

## Current status

**Not implemented.** The current GitHub Pages site is static. Browser-local records are private to that browser profile and are not a shared submission system. Do not describe the current local-storage workflow as public contribution intake.

## Recommended minimum architecture

- Static GitHub Pages frontend.
- Small server-side API (for example, a maintained serverless function) with a managed database.
- Identity provider or GitHub OAuth flow using server-side code exchange; never place client secrets in site JavaScript.
- Private pending-submission table separate from the public curated catalogue.
- Moderation queue with approve, reject, request-changes, and audit-log actions.
- Rate limiting, payload-size limits, schema validation on the server, CSRF/origin checks where applicable, and abuse reporting.
- Automated daily encrypted backups, restore drills, retention policy, and documented incident response.
- Least-privilege service credentials stored only in platform secrets; rotate credentials and audit access.

## Submission lifecycle

1. User signs in and submits a record with source URLs and evidence limitations.
2. API validates type, lengths, URLs, rate limits, and required fields server-side.
3. Submission is stored as pending and is not publicly indexed.
4. Moderator checks source provenance, privacy, defamation risk, duplicates, and evidence framing.
5. Approved record is versioned and published to the curated dataset; rejected records remain private or are deleted under a documented retention policy.
6. Audit events and backups are monitored; maintainers periodically test restore procedures.

## Research integrity rules

- A submission is a lead, not a verified finding.
- Do not accept anonymous allegations as established fact.
- Separate original evidence from commentary and source chains.
- Require location precision labels and prohibit publishing sensitive private addresses.
- Keep counterevidence, uncertainty, and correction history available.
- Provide a takedown/correction channel and a clear privacy notice.

## Deployment gate

Do not enable shared submissions until authentication, server-side validation, moderation, backup restoration, logging, privacy notice, and security review have all been tested. A frontend-only form is not an acceptable substitute.
