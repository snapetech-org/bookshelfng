Subject: StartOS package submission: BookshelfNG

This is an old StartOS submission draft for the BookshelfNG package. It has
not been updated to ChaptarrNG; do not submit it as a current new-install offer.
The final BookshelfNG release is 0.4.21.71. Existing users need the documented
migration path and a separately tested StartOS image update.

Wrapper repository: https://github.com/snapetech-org/bookshelfng-startos
Source repository: https://github.com/snapetech-org/bookshelfng
Image: docker.io/snapetech/bookshelfng:hardcover-v0.4.21.37 (legacy snapshot; final .71 image is available)

The package exposes the web UI on TCP 8787 and persists /config, /books, and
/downloads. The application is licensed under GPL-3.0-only.
