#!/bin/sh
xte 'sleep 10' 'key F11' 'mousemove 0 0' -x:0 &
epiphany-browser nobodieswatching.html --display=:0
