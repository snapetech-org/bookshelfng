---
category: security
audience: operators
area: ci
action: none
breaking: false
---
Separate tag-triggered release builds from manual publisher recovery. Release publication now validates and stages build inputs from a successful tag run, while recovery uses only assets from an already-published release. Internal runtime-pack build inputs are excluded from public release assets.
