# ECHO-7 research database

## Current architecture

ECHO-7 is currently a static GitHub Pages site. The structured starter catalogue is in `data/records.json`; the interactive DATABASE page builds its seeded index from the curated data arrays in `index.html` and adds user-created entries from browser local storage.

The starter JSON currently contains 103 curated index records across these types:

- Incident cases
- Timeline entries
- Witness / person profiles
- Programs
- Claims and hypotheses
- Source references
- Community and South Carolina research leads

This is a structured starter index, not a complete mirror of external websites and not a claim that all reported events are verified.

## Record shape

Each record contains an `id`, `kind`, `year`, `title`, `location`, `category`, `summary`, `notes`, `sources`, `provenance`, and `evidenceStatus`. A source has a display title and original URL.

## Editing and importing

1. Edit `data/records.json` to add or correct shared starter records.
2. Keep IDs unique and retain the original source URL.
3. Separate a witness's statement from independent corroboration.
4. Use the DATABASE page to add temporary personal research records in your browser.
5. Export JSON regularly if you want to preserve browser-added records. Browser-local additions are not automatically shared or committed to GitHub.
6. The JSON file can be imported into other database tools or used by future backend/API work.

## Next step for a truly shared database

GitHub Pages cannot securely accept writes to the repository from a public browser without a server-side authorization layer. Do not put a GitHub personal access token, database secret, or private API key in `index.html`. A shared multi-user database needs an authenticated backend (for example, Supabase or a small serverless API), access rules, backups, and a moderation strategy. Until that is configured, this project deliberately uses a public read-only catalogue plus local-only personal additions.

## Quality checks

The GitHub Actions workflow `.github/workflows/validate-database.yml` checks the JSON schema, duplicate IDs, source URL formats, and inline JavaScript syntax when relevant files change.
