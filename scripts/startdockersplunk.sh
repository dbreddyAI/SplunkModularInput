#!/usr/bin/env bash

docker run --name splunk --hostname splunk -p 8000:8000 -d -e "SPLUNK_START_ARGS=--accept-license" splunk/splunk

exit
