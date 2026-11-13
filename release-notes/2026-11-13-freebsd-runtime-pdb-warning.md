---
category: fixed
audience: operators
area: packaging
action: none
breaking: false
---
The FreeBSD runtime-pack build now handles a duplicate `System.Private.CoreLib.pdb` packaging warning while keeping the symbol file already present in the runtime package. This prevents the warning-as-error from stopping the .NET 10.0.15 FreeBSD pack build.
