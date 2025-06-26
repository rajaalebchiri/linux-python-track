#!/bin/bash

echo "hello from system monitor"

# get CPU usage
get_cpu_usage() {
    cpu_usage=$(top -l 1 | grep "CPU usage" | awk -F'[:,]' '{print $2}' | awk '{print "CPU Usage: " 100 - $NF"%"}')
    echo "$cpu_usage"
}

get_memory_usage() {
    memory_usage=$(vm_stat | awk '
        /Pages free/      {free=$3}
        /Pages active/    {active=$3}
        /Pages inactive/  {inactive=$3}
        /Pages speculative/ {spec=$3}
        /Pages wired down/ {wired=$3}
        END {
        total=free+active+inactive+spec+wired;
        used=active+inactive+spec+wired;
        printf "Memory Usage: %.2f%%\n", used*100/total
        }')
    echo "$memory_usage"
}

get_disk_usage() {
    disk_usage=$(df -h | awk '$NF=="/"{printf "Disk Usage: %s\n", $5}')
    echo "$disk_usage"
}

get_network_usage() {
    network_usage=$(netstat -ib | awk '$1=="en0"{ined+=$7; outed+=$10} END {printf "Network Usage: In: %.2f KB, Out: %.2f KB\n", ined/1024, outed/1024}')
    echo "$network_usage"
}

get_system_uptime() {
    boot_time_sec=$(sysctl -n kern.boottime | awk '{print $4}' | tr -d ',')
    current_time=$(date +%s)
    uptime_seconds=$((current_time - boot_time_sec))
    uptime_days=$((uptime_seconds / 86400))
    uptime_hours=$(((uptime_seconds % 86400) / 3600))
    uptime_minutes=$(((uptime_seconds % 3600) / 60))
    echo "System Uptime: $uptime_days days, $uptime_hours hours, $uptime_minutes minutes"
}

# Function to display all metrics
display_metrics() {
    echo "=== System Monitoring Tool ==="
    get_cpu_usage
    get_memory_usage
    get_disk_usage
    get_network_usage
    get_system_uptime
}

# Main loop to refresh metrics every 5 seconds
while true; do
    clear
    display_metrics
    sleep 5
done