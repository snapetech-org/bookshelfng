---
category: security
audience: operators
area: dependencies
action: none
breaking: false
---
Frontend and .NET dependency audits are clear for the final source branch. The frontend build and lint dependency `braces` now rejects nesting deeper than 256 levels while upstream has no published fix for the recursive parser advisory.
