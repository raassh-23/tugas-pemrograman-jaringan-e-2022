#!/bin/bash

urls=(
    'http://172.16.16.101:8889/rfc2616.pdf'
    'http://172.16.16.101:8889/testing.txt'
    'http://172.16.16.101:8889/pokijan.jpg'
)
con_levels=(1 5 10 20)
requests=(10 50 100 500 1000 5000 10000)

for url in "${urls[@]}"; do
    for con in "${con_levels[@]}"; do
        for req in "${requests[@]}"; do
            echo "Benchmarking $url with $con connections and $req requests"
            ab -n $req -c $con $url > "results/ab-${con}-${req}-${url##*/}.txt"
            sleep 1
        done
        echo ""
    done
done