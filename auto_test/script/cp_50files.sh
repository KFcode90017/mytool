#!/bin/bash

source_directory="/home/kohzu/work/auto_test/glmark2_10000frame"  # glmark2_result_1.logからglmark2_result_100.logが格納されているディレクトリ
destination_directory="/home/kohzu/work/auto_test/50files"  # 1から50までのファイルをコピーするディレクトリ

for i in {1..50}; do
  source_file="$source_directory/glmark2_result_$i.log"
  destination_file="$destination_directory/glmark2_result_$i.log"
  
  # ファイルをコピー
  if [ -f "$source_file" ]; then
    cp "$source_file" "$destination_file"
    echo "ファイル $source_file を $destination_file にコピーしました。"
  else
    echo "ファイル $source_file が見つかりません。"
  fi
done

