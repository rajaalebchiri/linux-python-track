#!/bin/bash

echo "hello from system monitor"

# get CPU usage
get_cpu_usage() {
    cpu_usage=$(top -l 1 | grep "CPU usage" | awk -F'[:,]' '{print $2}' | awk '{print 100 - $NF"%"}')
    echo "$cpu_usage"
}

get_cpu_usage