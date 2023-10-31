#!/bin/bash

# コマンドライン引数でディレクトリを指定
source_directory="$1"
destination_directory="$2"

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

