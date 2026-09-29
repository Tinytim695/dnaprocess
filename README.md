# 🧬 DNAProcess

[![Version](https://img.shields.io/badge/version-0.2.0-blue)](VERSION)
[![Python](https://img.shields.io/badge/python-3.9%2B-yellow)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Linux-informational)](#-scope)
[![CI](https://github.com/Tinytim695/dnaprocess/actions/workflows/quality.yml/badge.svg)](https://github.com/Tinytim695/dnaprocess/actions/workflows/quality.yml)
[![License](https://img.shields.io/badge/license-MIT-informational)](LICENSE)

**Local Linux process fingerprinting and snapshot diffing.**

DNAProcess reads the Linux `/proc` filesystem and turns a running process into a portable JSON snapshot. Capture the same process before and after a test, then inspect what changed.

## Captured process DNA

- PID and parent PID
- process name and state
- UID/GID
- thread count
- executable path and SHA-256
- command line
- kernel start-time ticks
- namespace identifiers
- open-file-descriptor count and broad types
- memory-map count and referenced file paths
- a SHA-256 fingerprint of the process record

No process environment is collected.

## Usage

Capture a process:

```bash
dnaprocess snapshot 1234 -o before.json
```

Capture to stdout:

```bash
dnaprocess snapshot 1234
```

Capture again:

```bash
dnaprocess snapshot 1234 -o after.json
```

Compare:

```bash
dnaprocess diff before.json after.json
```

Example output:

```text
Fingerprint: 8d... -> 72...
Changes:
~ threads: 3 -> 5
~ fds.count: 7 -> 9
+ namespaces.mount = 'mnt:[4026531841]'
```

## 🔐 Privacy and safety

DNAProcess is local-only. It has no telemetry, network client, daemon or upload path.

Snapshots can still contain sensitive local details such as command lines, executable paths, namespace identifiers and mapped file paths. Treat snapshot files as local evidence.

It does not attach to, inject into, suspend, kill or modify the target process.

## Scope

Linux `/proc` is required. Some fields may be unavailable without sufficient permissions. Use only on systems and processes you are authorised to inspect.

## License

MIT
