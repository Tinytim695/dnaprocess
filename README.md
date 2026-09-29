# DNAProcess

Local Linux process fingerprinting and snapshot diffing.

DNAProcess reads Linux /proc information and builds a compact process fingerprint. It does not inject into, stop, kill or modify the target process.

FEATURES
- executable path and SHA-256
- command line
- UID/GID/PPID/state
- current working directory
- root directory
- open-file descriptor count
- memory-map count
- JSON snapshots
- snapshot-to-snapshot diff

INSTALL
1. git clone https://github.com/Tinytim695/dnaprocess.git
2. cd dnaprocess
3. chmod +x dnaprocess
4. sudo install -m 0755 dnaprocess /usr/local/bin/dnaprocess

USAGE
dnaprocess snapshot 1234 > before.json
dnaprocess snapshot 1234 > after.json
dnaprocess diff before.json after.json

Some /proc fields can be unavailable without permission.

No network probing, telemetry or uploads.

License: MIT
