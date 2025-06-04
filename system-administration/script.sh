#!/usr/bin/env bash

name="John"
age=30


echo "hello $name you are $age years old"

echo "I'm in $(pwd)"

echo "I'm in `pwd`"

if [[ -z "$string" ]]; then
    echo "string is empty"
fi

get_name() {
    echo "$1"
}

echo "My name is $(get_name john)" >> data.txt

mpstat