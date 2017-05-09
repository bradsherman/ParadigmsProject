#!/bin/bash

# replace ip in src/client.py with current ip of server
cl="./src/client.py"
script="./src/get_ip.py"

echo "finding current ip..."
ip=$($script)
echo "ip = ${ip}"
echo "replacing ip"
sed -ri "s/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/${ip}/g" $cl
echo "ip replaced!"
