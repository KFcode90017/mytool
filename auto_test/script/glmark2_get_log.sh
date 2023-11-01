#!/bin/bash

# 引数で指定されたコマンドを実行する関数を定義
run_command() {
    local output_file="$1"
    local command="$2"
    "$command" > "$output_file"
    echo "Output saved to $output_file"
}

# 引数の数が正しいかチェック
if [ $# -ne 1 ]; then
    echo "Usage: $0 <command_to_run>"
    exit 1
fi

# セーブするディレクトリに移動
for ((i=1; i<=50; i++))
do
    output_file="output_result_${i}.log"
    run_command "$output_file" "$1"
done

