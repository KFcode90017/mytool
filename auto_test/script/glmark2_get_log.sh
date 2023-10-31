#!/bin/bash

#セーブするディレクトリに移動
for ((i=1; i<=100; i++))
do
    output_file="glmark2_result_${i}.log"
    /home/kohzu/kohzu/github_kohzu/KFcode/mytool/auto_test/glmark2_nframe/DESTDIR/usr/local/bin/glmark2-es2-wayland > "$output_file"
    echo "Output saved to $output_file"
done

