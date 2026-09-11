# UC23 — Salesforce Safe Retry

Durable unique operation-key reservation in Salesforce; duplicates and uncertain completion never authorize retry.

This replaces the generic Python prototype with Salesforce source. API 64.0 is pinned. Each directory is independent. No Python runtime or paid service is required.

## Checks and installation

Run `npm test` with Node 22+. Local tests validate metadata structure and synthetic controls. They do **not** compile or execute Apex.

In an explicitly authorized disposable org, review the source and run:

```sh
sf project deploy start --dry-run --source-dir force-app --test-level RunSpecifiedTests --tests UC23ServiceTest --target-org YOUR_DISPOSABLE_ORG
```

Only after dry-run tests and security review pass, an authorized operator can remove `--dry-run` to install. Assign the included `UC23_Operator` permission set only to designated evaluators. Standard-object CRUD/FLS is intentionally not granted; provision the least access for the test identity. No credentials, org connection or deployment was used to build this package.

## Scope and remaining gates

Apex compilation and execution unverified; requires an authorized disposable Salesforce org and domain-owner acceptance. No independent comparison or field adoption evidence. See `requirements.json` for the five exact original requirements. API limits, negative-permission users, bulk limits, concurrency, actual Flow integration and security review require native checks. A source preview is not a supported release. No EB1A outcome, novelty, independent recognition or final-merits claim follows from these artifacts.

## Evidence and authorship

Fixtures are synthetic and authored by AI. Source records are in `sources.json`. AI authored the implementation; Balaji supplied the Salesforce focus and portfolio direction. His independent technical review and decisions are not yet observed. Treat local results as simulated checks, source inspection as observed, and native behavior as proposed until executed.

## Salesforce-specific boundaries

Operation_Key__c is a unique external ID. Only insert reserves: no upsert, overwrite or duplicate retry. RESERVED_UNCERTAIN does not authorize an external write. A failed insert holds. No reconciliation adapter or receipt completion writer exists; retention and deletion controls need an org owner.

Database reservation failures expose only their Salesforce status code (`errorCode`), never raw database error text. This supports diagnosing permission failures while preserving the HOLD decision.

## Distribution

Salesforce is the primary implementation. Historical Python source is under `legacy/python-prototype`. See `RELEASE_STATUS.md` and `SALESFORCE_VALIDATION.json`. Full acceptance remains partial.
