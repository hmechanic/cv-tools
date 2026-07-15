#!/bin/bash
set -e

# Do not leak the TeX Live build-time frontend setting into user commands.
unset DEBIAN_FRONTEND

if [ $# -eq 0 ]; then
    exec bash
else
    exec "$@"
fi
