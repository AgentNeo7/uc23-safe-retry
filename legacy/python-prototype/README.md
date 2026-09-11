# UC23 — Agent Safe Retry

In-memory operation identity and retry simulation. This is a runnable local prototype with bounded checks. Full catalog requirements remain partial or unmet in `requirements.json`. It is not a production integration or differentiated-method release.

## Run

Requires Python 3.13; tested with `/opt/homebrew/bin/python3.13`. Uses only the standard library. From this directory:

```bash
python3.13 tool.py --input examples/input.json --output result.json
python3.13 test_tool.py -v
```

The reference input may intentionally return 1 for a declared failure. Exit 0 means a completed report, including an explicit unknown; it does not mean safety. Exit 1 means a configured check failed. Exit 2 means malformed input or an I/O failure. Output is deterministic JSON. Compare it with `examples/expected.json`. Reports never execute external actions.

## Inputs and checks

`examples/input.json` defines the supported explicit input contract. `examples/cases.json` contains 7 original synthetic scenarios with expected JSON frozen before implementation. Its hash is in `examples/manifest.json`. Tests compare full reports, exercise CLI exit codes, and reject four malformed inputs. `checks.json` preserves command, exit code, output and code hash. Tests passed locally; this tiny corpus is internal validation, not independent review or broad reliability evidence.

## Scope and limits

No durable ledger, worker concurrency, actual service call or exactly-once guarantee. Receipts and capabilities are caller-supplied simulated facts, not verified outcomes.

Malformed-input checks cover only the tested shapes. This is not a hardened untrusted-input service. Input permissions and truth must be established by the caller. Do not supply production credentials. Examples contain synthetic data.

## Baseline and research decision

[Primary source](https://docs.stripe.com/api/idempotent_requests), accessed 2026-09-11. Idempotency keys and parameter consistency already exist; local simulation cannot establish external completion. Publication date/version is unknown unless recorded in `capability.json`; live documentation or main-branch behavior must be pinned before integration. No external product was executed. This source is vendor/maintainer evidence, not independent recognition.

Comparative differentiation is untested. Keep this narrow utility; do not expand on the basis of a passing toy example.

## Release and attribution

This source preview contains local artifacts; no outreach occurred. MIT is applied to original code; full module release gates remain unmet. AI authored this code, tests and documentation. Balaji supplied priorities and constraints; no unobserved implementation work or external recognition is attributed to him. Before a broader release, assign a maintenance owner and address the original requirements and blockers individually.

## Correctness amendment — 2026-09-11

A previous completed state for the same operation/payload now holds for reconciliation when the receipt is unknown, regardless of declared idempotency support. A not-completed receipt conflicting with local completed state also holds. Local state is not authoritative proof of external completion, but it cannot be silently ignored. A genuinely new operation remains separate work.

Version 1 fixtures and checks are preserved. Version 2 adds four regression cases before the fix. The original implementation failed those new checks (`regression-before-fix.json`, exit 1); the fixed implementation passes all seven scenarios plus malformed CLI checks (`checks.json`, exit 0).

## Bounded CLI input — 2026-09-11

The CLI reads at most 2,000,000 bytes and rejects JSON deeper than 32 levels, containers over 1,000 entries, duplicate object keys and nonfinite numbers. Output cannot resolve to the input file, including symlink or existing same-file aliases. These errors exit 2 before writing. Five test methods now include duplicate-key, nesting, byte/container-size, numeric-overflow and overwrite regressions. `checks-before-io-hardening.json` preserves earlier checks; `checks.json` records the new run and source hashes. Decision algorithms and frozen scenario fixtures did not change. These bounds do not constitute a general security audit.

## Source preview status

Experimental offline source; scoped tests passed, full original acceptance is incomplete. See [release status](RELEASE_STATUS.md), [checks](release-checks.json), [requirements](requirements.json) and [attribution](ATTRIBUTION.md). No production, independent-validation or differentiation claim.
