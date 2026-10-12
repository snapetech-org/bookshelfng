---
category: fixed
audience: operators
area: testing
action: none
breaking: false
---
Linux direct-download browser tests now use their installed Chromium cache inside the isolated validation task, so required browser cases run consistently without sharing the task's home directory.
