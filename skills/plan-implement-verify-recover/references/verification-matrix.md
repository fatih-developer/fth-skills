# Verification Matrix

Select checks based on changed behavior. Do not run every available check
without considering relevance, runtime, and risk.

| Change type | Minimum verification | Additional verification |
|---|---|---|
| Documentation | Format and link checks | Render or preview when layout matters |
| Configuration | Parse or load validation | Startup test |
| Pure function | Targeted unit test | Property or edge-case tests |
| UI component | Typecheck and component test | Visual or browser verification |
| API handler | Targeted API test | Integration and contract tests |
| Public API | Contract and compatibility tests | Consumer verification |
| Database query | Query validation | Representative data test |
| Migration | Migration test | Rollback and data integrity check |
| Authentication | Targeted auth tests | Integration and security review |
| Authorization | Positive and negative permission tests | Privilege-boundary review |
| Security fix | Regression test | Fresh semantic security review |
| Dependency update | Build and affected tests | Changelog and compatibility review |
| Refactoring | Existing behavioral tests | Broader regression tests |
| Performance change | Correctness test | Before-and-after measurement |

Start with the fastest relevant check. Expand verification when risk, affected
surface, or initial results justify it.

## Evidence Quality

Prefer evidence in this order:

1. Reproduced behavior or passing automated test.
2. Successful build, typecheck, lint, or integration check.
3. Deterministic tool output or runtime log.
4. Focused semantic diff review.
5. Reasoned assessment when execution is unavailable.

Do not present a lower-quality signal as stronger proof. State proof gaps
explicitly.
