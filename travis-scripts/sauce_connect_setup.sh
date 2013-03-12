#!/bin/bash

CONNECT_URL="http://saucelabs.com/downloads/Sauce-Connect-latest.zip"
STARTUP_TIMEOUT=90
CONNECT_DIR="/tmp/sauce-connect-$RANDOM"
CONNECT_DOWNLOAD="Sauce_Connect.zip"
READY_FILE="connect-ready-$RANDOM"

if [ -n "$TRAVIS" ] && [ -n "$TRAVIS_JOB_NUMBER" ]; then
    if [ -z $(which java) ]; then
        # If running on travis, install Java
        echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections
        echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections
        sudo add-apt-repository -y ppa:webupd8team/java
        sudo apt-get update -qq
        sudo apt-get install -qq oracle-java7-installer
    fi
    # If running on travis, use a tunnel identifier
    TUNNEL_IDENTIFIER="--tunnel-identifier $TRAVIS_JOB_NUMBER"
else
    TUNNEL_IDENTIFIER=""
fi

# Get Connect and start it
mkdir -p $CONNECT_DIR
cd $CONNECT_DIR
curl $CONNECT_URL > $CONNECT_DOWNLOAD
unzip $CONNECT_DOWNLOAD
java -jar Sauce-Connect.jar --readyfile $READY_FILE \
    $TUNNEL_IDENTIFIER \
    $SAUCE_USERNAME $SAUCE_ACCESS_KEY &

# Wait for Connect to be ready before exiting
while [ ! -f $READY_FILE ]; do
  sleep .5
done
