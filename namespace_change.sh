#!/bin/sh

while read -r line; do
    sed 's/moksha/zmqfirewall/g' -i $line
done <<< "`grep -lir "moksha" zmqfirewall`"
