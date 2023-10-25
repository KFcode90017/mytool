import re
import os
import sys
import math
import statistics
from scipy import stats
import matplotlib.pyplot as plt

pattern = r'\[(.*?)\]\s*(.*?)(?:FPS:\s*(\d+)\s+FrameTime:\s*([\d.]+)\s+ms|$)'

if len(sys.argv) < 4 or sys.argv[2] != "-s":
    print("ログファイルのディレクトリとシーンの番号を引数として指定してください。")
    sys.exit(1)

directory = sys.argv[1]
scene_number = int(sys.argv[3])

summary = {}

for filename in os.listdir(directory):
    if filename.endswith(".log"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            log = file.read()
            matches = re.findall(pattern, log)

            for match in matches:
                scene_option = (match[0], match[1])  # シーンとオプションをタプルに結合
                frame_time = float(match[3])

                if scene_option not in summary:
                    summary[scene_option] = [frame_time]
                else:
                    summary[scene_option].append(frame_time)

scene_options = list(summary.keys())

if scene_number < 1 or scene_number > len(scene_options):
    print("指定されたシーンが存在しません。")
    sys.exit(1)

selected_scene_option = scene_options[scene_number - 1]
frame_times = summary[selected_scene_option]
scene, option = selected_scene_option

print(f"ディレクトリ数: {len(os.listdir(directory))}")
print(f"データ数: {len(frame_times)}")
# average
average_frame_time = sum(frame_times) / len(frame_times)
print("frame_times:")
for i, time in enumerate(frame_times, start=1):
    print(f"{os.listdir(directory)[i-1]}: {time}")

# standard deviation
square_diffs = [(x - average_frame_time) ** 2 for x in frame_times]
variance = sum(square_diffs) / len(square_diffs)
std_dev = math.sqrt(variance)
# median
median_frame_time = statistics.median(frame_times)

# Shapiro-Wilk検定
shapiro_stat, shapiro_p = stats.shapiro(frame_times)

# アンダーソン-ダーリング検定
anderson_stat, anderson_critical, anderson_significance = stats.anderson(frame_times, dist='norm')

# コルモゴロフ-スミルノフ検定
ks_stat, ks_p = stats.kstest(frame_times, 'norm') 

if shapiro_p > 0.05:
    shapiro_normality = "OK"
else:
    shapiro_normality = "NOT"

if all(anderson_significance > 0.05):
    anderson_normality = "OK"
else:
    anderson_normality = "NOT"

if ks_p > 0.05:
    ks_normality = "OK"
else:
    ks_normality = "NOT"

print(f"Scene: {scene}, Option: {option}")
print(f"Average FrameTime: {average_frame_time:.3f} ms")
print(f"Median FrameTime: {median_frame_time:.3f} ms")
print(f"Standard Deviation: {std_dev:.3f} ms")
print(f"Shapiro-Wilk Test: p-value = {shapiro_p:.3f}")
print(f"Shapiro-Wilk Test: {shapiro_normality}")
print(f"Anderson-Darling Test: statistic = {anderson_stat:.3f}")
print(f"Anderson-Darling: {anderson_normality}")
print(f"Kolmogorov-Smirnov Test: p-value = {ks_p:.3f}")
print(f"Kolmogorov-Smirnov: {ks_normality}")


# ヒストグラムを描画
plt.hist(frame_times, bins=20)
plt.xlabel("FrameTime (ms)")
plt.ylabel("Frequency")
plt.title(f"FrameTime Histogram for {scene} - {option}")
plt.show()
