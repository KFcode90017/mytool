#!/bin/bash

for ((i=1; i<=100; i++))
do
    output_file="glmark2_result_${i}.log"
    glmark2-es2 > "$output_file"
    echo "Output saved to $output_file"
done

