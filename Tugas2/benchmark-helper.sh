#!/bin/bash

read -p "Enter URL: " urls_string
urls=(${urls_string})

read -p "Enter number of requests: " requests_string
requests=(${requests_string})

con_levels=(1 5 10 20 40)

for url in "${urls[@]}"; do
    for con in "${con_levels[@]}"; do
        for req in "${requests[@]}"; do
            if [ $con -gt $req ]; then
                continue
            fi

            echo "Benchmarking $url with $con connections and $req requests"
            ab -n $req -c $con $url > "results/ab-${con}-${req}-${url##*/}.txt"
            sleep 1
        done

        echo ""
    done
done