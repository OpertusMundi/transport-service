#!/bin/sh
#set -x
set -e

export FLASK_APP="transport_service"
export SECRET_KEY="$(dd if=/dev/urandom bs=12 count=1 status=none | xxd -p -c 12)"

# Run

exec nosetests $@
