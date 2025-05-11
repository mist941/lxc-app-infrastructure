#!/bin/bash

cat containers.json | jq -r 'to_entries[] | "\(.key) \(.value)"' | while read -r name id; do
    echo "Enabling bash for $name ($id)"
done
