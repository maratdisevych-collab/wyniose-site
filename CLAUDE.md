# Wyniosę website: rules for agents

Site: https://wyniose.pl (Polish home, `/en/`, `/polityka-prywatnosci/`). Owner: Marat Maksimovich. Write to him in Russian and address him formally as "Марат Максимович".

## How publishing works

- **Netlify:** project `silver-muffin-4fedd6`, site id `4a51e6ed-4312-4b48-80f4-cdf2882c9363`. It publishes the `site/` folder of the `main` branch exactly as committed. Netlify runs no build.
- **Pushing to `main` publishes to the live site.** Nothing reaches `main` unless `bash scripts/release.sh` ends with `ALL CHECKS PASSED`.
- **Workflow:** edit `source/` → `bash scripts/release.sh` (rebuilds `site/` from `source/`, then runs `tests/run_all.sh`) → commit `source/` and `site/` together → push. Never edit `site/` by hand.
- **After every push:**
  - wait about 1–2 minutes, then fetch https://wyniose.pl/?v=<timestamp> and confirm the change is live: new `assets/site.js?v=` hash if JS or CSS changed, expected text present;
  - confirm contacts, NIP and the cookie banner are still there.
  - If the live site is wrong, fix forward with `git revert` and push again.
- **Tests:**
  - `tests/consent_test.py`: Consent Mode v2 basic, one conversion per click, no Google requests before consent. Expects 117/117.
  - `tests/security_test.py`: headers, CSP, XSS in the job card, links, framing, secrets scan. Expects 108/108.
  - The sandbox cannot reach Google, so gtag.js is stubbed in the tests.

## Source map

- **`source/i18n.py`:** all texts, PL and EN (UK and RU dictionaries are kept but not built).
- **`source/src/page.html.j2`:** the page template.
- **`source/src/`:**
  - `style.css`
  - `app.js`: contacts, job card, WhatsApp message.
  - `stair.js`: the stairwell animation.
  - `consent.js`: cookie banner, Google Ads conversions.
- **`source/site_config.json`:** phones, e-mail, company data, Google Ads ids. Generates `site/config.js`.
- **`source/static/polityka-prywatnosci.html`:** the privacy policy, in Polish.
- **`source/build.py`:**
  - builds `source/build/dist`; `release.sh` copies it to `site/`;
  - computes CSP hashes and writes `_headers`, `.htaccess`, `_redirects`, `security.txt`, `sitemap.xml`, `robots.txt`.

## Facts that must stay true (do not change without the owner's explicit "да")

**Business**
- Property clearance in Wrocław and up to 70 km:
  - flats, houses, rooms, offices, basements, garages, attics;
  - furniture and junk removal;
  - dismantling, carrying from any floor, loading, transport.
- Everything goes to PSZOK or recycling.
- Free estimate from photos or on site. The price depends on the job and is agreed before work. There is no price list.
- Minimum job is about half a room. Invoices without VAT. Payment in any form.
- Cleaning after clearance is an optional extra.
- The van on the site is a drawing; there is no real photo yet.

**Contacts and company**
- Main phone and WhatsApp: +48 516 721 072 (all main CTAs).
- Second phone: +48 791 645 395. E-mail: kontakt@wyniose.pl.
- Company: Wyniosę Marat Disevych, ul. Krynicka 24, 50-555 Wrocław, NIP 8993068911. No REGON.

**Google Ads**
- Tag AW-18540345955.
- Telefon `AW-18540345955/XIrxCOOG3KsdEOP03IhF`: click on any `tel:` link.
- WhatsApp `AW-18540345955/HsRYCKHHzKsdEOP03IhF`: click on "Wyślij na WhatsApp".
- Both are secondary actions. The primary goal, calls from ads of at least 60 s, lives in Google Ads.

**Consent Mode v2 basic**
- No Google request before consent.
- Defaults are all denied. On consent, update only ad_storage and ad_user_data.
- Never replay clicks made before consent. Copying the job card is never sent to Google.
- No GA4, no GTM, no enhanced conversions.

## Never

- Invent prices, reviews, ratings, licences or certificates, or promise "dziś", "w 24 h", "najtaniej" or any speed or price.
- Create doorway pages or stuff keywords. Copy competitors' texts.
- Touch Google Ads: budget, bids, goals, campaigns. Never click ads; every paid click costs the owner money.
- Weaken security:
  - remove headers;
  - widen the CSP: no wildcards, no 'unsafe-inline' scripts, no 'unsafe-eval';
  - add third-party scripts, fonts or trackers.
- Put passwords, tokens or personal data in the repo.
- Roll back deploys in Netlify, or change Netlify or DNS settings. Fix forward through git.

## Autonomy (owner's decision, 2026-10-28)

The owner allows changes to be published automatically, on one condition: **before anything changes on the live site, he gets a plain-language explanation in Russian.** It covers:
- what changes, in "Было → Будет" form;
- where on the page;
- why;
- what a visitor will notice.

No jargon, no code, no file names in that explanation. Links go at the end.

### Two kinds of changes

**Safe.** Branch name: `proposal/auto-<YYYY-MM-DD>-<topic>`. Covers:
- stale facts corrected from an official source (link it in the commit message);
- Polish or English typos and unnatural wording;
- technical fixes (errors, broken links, performance, accessibility) that keep the design;
- small copy improvements inside existing sections, such as a clearer FAQ answer or a new FAQ item backed by evidence.

**Needs "да".** Branch name: `proposal/ask-<YYYY-MM-DD>-<topic>`. Covers changes to:
- prices or price wording, promises, guarantees, speed;
- the legal text (privacy policy), company data, contacts;
- consent, cookies or tracking;
- new sections or pages, design or layout, removing sections;
- anything that changes the offer.

### Process

1. **Monday, weekly review:** prepares changes but does not publish them.
   - Each change gets its own branch from `main`.
   - Run `bash scripts/release.sh` on the branch. Push the branch only if it ends with `ALL CHECKS PASSED`.
   - The report explains every change in plain Russian and states the deadlines:
     - safe changes go live on Tuesday morning unless he answers "нет";
     - "ask" changes go live only after his "да".
2. **The owner's replies in the weekly conversation**, either for all changes or by number:
   - "да" → merge into `main` now (step 4), publish, verify.
   - "нет" → delete the branch.
3. **Daily check, from Tuesday on:**
   - Picks every `proposal/auto-*` branch at least 12 hours old and merges it into `main` (step 4). Publishes, verifies live, then reports in plain Russian what went live.
   - Never merges `proposal/ask-*`.
   - Deletes any proposal branch older than 14 days with no answer and mentions it.
4. **Merging:**
   - Merge into `main`, then run `bash scripts/release.sh` on `main`. It rebuilds `site/` from the merged `source/`; resolve conflicts in `site/` by rebuilding.
   - Commit the rebuilt `site/` if it changed.
   - Push only after `ALL CHECKS PASSED`. If a merge fails the gate, leave it out and report.
5. **Emergency exception** (this is a restore, not a change):
   - **Trigger:** the live site is broken (down, wrong contacts, consent code missing, foreign content) and a recent commit caused it.
   - **Action:** the daily check reverts that commit at once, publishes, verifies, and tells the owner in plain language what happened.
   - **If the cause is outside the repository** (DNS, Netlify, hijacked account), it only reports.

**Every published change** is reported in the run that published it: what, where, why, commit link.

## Commit messages

English, imperative mood, one line of what changed, then a line of why, with source links where relevant.
