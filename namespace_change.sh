#!/bin/sh

# What are you doing gitignore, youre not a normal file
rm zmqfirewall/.gitignore

while read -r line; do
    sed 's/moksha.firewall/zmqfirewall/g' -i $line
done <<< "`grep -lir "moksha" zmqfirewall`"

