import re
import sys

def calculate_and_print_fps(file_path):
    total_fps = 0
    fps_count = 0

    with open(file_path, 'r') as file:
        for line in file:
            match = re.search('FPS: (\d+)', line)
            if match:
                fps_value = int(match.group(1))
                total_fps += fps_value
                fps_count += 1
                print(f'Extracted FPS value: {fps_value}')
    
    fps_average = total_fps / fps_count if fps_count else 0

    return fps_average

# コマンドライン引数からファイルパスを取得して関数を呼び出す
file_path = sys.argv[1]
print(f'The average FPS value is: {calculate_and_print_fps(file_path)}')

