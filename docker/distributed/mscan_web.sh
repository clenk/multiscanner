#!/bin/bash

# Run confd to set configuration
confd -onetime -backend env

# Give apache ownership of the multiscanner directory
chown -R daemon:daemon /opt/multiscanner

# Run Docker CMD
bash -c "$@"
