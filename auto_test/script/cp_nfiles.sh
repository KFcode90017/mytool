#!/bin/bash

# コマンドライン引数でディレクトリを指定
n_cp_file="$1"
source_directory="$2"
destination_directory="$3"

for i in $(seq 1 $n_cp_file); do
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

