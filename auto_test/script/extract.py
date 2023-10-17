import re
import os
import sys

#pattern = r"\[([^\]]+)\] ([^:]+): FPS: (\d+)"
pattern = r"\[([^\]]+)\] ([^:]+): FPS: (\d+) FrameTime: ([\d.]+) ms"

if len(sys.argv) < 2:
    print("ログファイルのディレクトリを引数として指定してください。")
    sys.exit(1)

directory = sys.argv[1]

for filename in os.listdir(directory):
    if filename.endswith(".log"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            log = file.read()
            matches = re.findall(pattern, log)

            for match in matches:
                scene = match[0]
                option = match[1]
                fps = int(match[2])
                frame_time = float(match[3])
                print(f"File: {filename}, Scene: {scene}, Option: {option}, FPS: {fps}, FrameTime: {frame_time} ms")

