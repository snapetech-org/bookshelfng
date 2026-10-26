FROM docker.io/snapetech/bookshelfng:hardcover-v0.4.21.77

HEALTHCHECK --interval=30s --timeout=5s --start-period=2m --retries=5 \
    CMD curl --fail --silent --max-time 5 http://127.0.0.1:8787/ping | jq -e '.status == "OK"' >/dev/null || exit 1
