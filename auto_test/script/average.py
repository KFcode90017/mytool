import re
import os
import sys
import math

pattern = r"\[([^\]]+)\] ([^:]+): FPS: \d+ FrameTime: ([\d.]+) ms"

if len(sys.argv) < 2:
    print("ログファイルのディレクトリを引数として指定してください。")
    sys.exit(1)

directory = sys.argv[1]

summary = {}

for filename in os.listdir(directory):
    if filename.endswith(".log"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            log = file.read()
            matches = re.findall(pattern, log)

            for match in matches:
                scene = match[0]
                option = match[1]
                frame_time = float(match[2])

                key = (scene, option)
                if key not in summary:
                    summary[key] = [frame_time]
                else:
                    summary[key].append(frame_time)

for key, frame_times in summary.items():
    scene = key[0]
    option = key[1]
    average_frame_time = sum(frame_times) / len(frame_times)

    # Calculation for standard deviation
    square_diffs = [(x - average_frame_time) ** 2 for x in frame_times]
    variance = sum(square_diffs) / len(square_diffs)
    std_dev = math.sqrt(variance)

    print(f"Scene: {scene}, Option: {option}, Average FrameTime: {average_frame_time:.3f} ms, Standard Deviation: {std_dev:.3f} ms")

