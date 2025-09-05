# entrypoint.sh
#!/bin/bash
set -e

<<<<<<< HEAD

# hand off to the CMD (gunicorn)
=======
# Just hand off to CMD (gunicorn); the Cloud SQL Auth proxy sidecar is already running
>>>>>>> b516b51 (Remove manual v1 Cloud SQL proxy; rely on Cloud Run v2 sidecar)
exec "$@"

