# ECHO-7: launch, accessibility, and security test plan

This checklist records what must be tested before treating the archive as production-ready. Static source checks are useful, but they are not a substitute for browser-based testing.

## Current feature boundaries

- GitHub Pages serves a static site and curated public JSON.
- Research records created or imported in the browser are stored in that browser's local storage.
- Local records are not sent to GitHub and are not shared with other visitors.
- The geographic explorer is a schematic of approximate reference areas, not a precision map or a claim that coordinates are independently surveyed.
- Claim assessment labels are qualitative research aids. Domain count is not proof of source independence.

## Browser acceptance checklist

### Responsive layout
- [ ] Test 320 px, 375 px, 768 px, 1024 px, and desktop widths.
- [ ] Confirm navigation, filters, map labels, dossier modal, and forms do not create horizontal overflow.
- [ ] Check text zoom to 200% and browser high-contrast/dark mode behavior.

### Keyboard and assistive technology
- [ ] Navigate all controls using Tab, Shift+Tab, Enter, Space, and Escape.
- [ ] Verify visible focus indicators and logical focus order.
- [ ] Confirm modal open/close behavior and focus return.
- [ ] Confirm filters and import status are announced by assistive technology.
- [ ] Check headings, form labels, button names, color contrast, and SVG labels with a screen reader.

### Database workflow
- [ ] Import a valid exported JSON file; export it again and compare record counts.
- [ ] Try malformed JSON, empty records, duplicate titles, duplicate IDs, invalid kinds, invalid years, long fields, invalid URLs, and non-HTTP URL schemes.
- [ ] Try files over 2 MB and arrays over 2,000 records.
- [ ] Confirm rejected rows are reported and valid rows are retained.
- [ ] Confirm local storage errors do not crash the rest of the site.
- [ ] Verify CSV escaping with commas, quotes, and newlines.
- [ ] Confirm reset affects only local additions, never curated seed records.

### Dossiers and source links
- [ ] Open every case dossier and every related-record link.
- [ ] Check source links for HTTP errors, redirects, changed titles, and primary-source availability.
- [ ] Verify external links use safe target/rel attributes.
- [ ] Check that missing sources and unresolved status remain visible.

### Published site
- [ ] Open the GitHub Pages URL in a clean browser profile and on a mobile device.
- [ ] Confirm relative paths load the JSON and schema.
- [ ] Confirm the live deployment reflects the expected commit.
- [ ] Review GitHub Actions run logs and fix failures; a missing status is not a passing test.

## Source review workflow

For each major historical case:
1. Locate the earliest available contemporaneous document or recording.
2. Record the original publisher/creator, publication date, archive URL, and retrieval date.
3. Distinguish direct observation, testimony relayed by another person, official interpretation, and later retelling.
4. Record credible alternative explanations and what evidence would distinguish them.
5. Track source dependency: copied reporting or multiple witnesses repeating one account must not be counted as independent corroboration.
6. Preserve uncertainty and note unavailable originals; do not fill gaps with inference.

## Security and data integrity
- Treat every imported file and source URL as untrusted input.
- Never execute imported content or render it as raw HTML.
- Do not commit private personal data, credentials, tokens, or unredacted witness contact information.
- Review source changes and database schema changes before merging.
