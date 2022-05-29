#!/bin/bash

read -p "Enter URL: " url

read -p "Enter number of requests: " requests_string
requests=(${requests_string})

for req in "${requests[@]}"; do
    con_levels=(1 $((req/4)) $((req/2)) $((3*req/4)) $req)
    
    for con in "${con_levels[@]}"; do
        echo "Benchmarking $url with $con connections and $req requests"
        ab -n $req -c $con $url > "results/ab-${con}-${req}-${url##*/}.txt"
        sleep 1
    done

    echo ""
done