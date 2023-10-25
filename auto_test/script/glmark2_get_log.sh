#!/bin/bash

#セーブするディレクトリに移動
for ((i=1; i<=100; i++))
do
    output_file="glmark2_result_${i}.log"
    glmark2-es2-wayland > "$output_file"
    echo "Output saved to $output_file"
done

