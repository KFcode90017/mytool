import os
import re
import argparse
import statistics
from scipy import stats
import matplotlib.pyplot as plt

pattern = re.compile(r'FrameTime: (\d+.\d+) ms')

def extract_frametimes(directory, frame_times):
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                log = file.read()
                matches = re.findall(pattern, log)

                frame_times_1_file = []
                for match in matches:
                    frametime = float(match)
                    frame_times_1_file.append(frametime)

                if frame_times_1_file:
                    avg_time = sum(frame_times_1_file) / len(frame_times_1_file)
                    frame_times.append(avg_time)

parser = argparse.ArgumentParser(description='Process log directories.')
parser.add_argument('-d1', required=True, help='Directory of log files for d1.')
parser.add_argument('-d2', required=True, help='Directory of log files for d2.')
parser.add_argument('-d3', required=True, help='Directory of log files for d3.')
parser.add_argument('-d4', required=True, help='Directory of log files for d4.')
args = parser.parse_args()

frame_times_d1 = []
frame_times_d2 = []
frame_times_d3 = []
frame_times_d4 = []

extract_frametimes(args.d1, frame_times_d1)
extract_frametimes(args.d2, frame_times_d2)
extract_frametimes(args.d3, frame_times_d3)
extract_frametimes(args.d4, frame_times_d4)


def compute_statistics(frame_times):
    mean = statistics.mean(frame_times)
    median = statistics.median(frame_times)
    stddev = statistics.stdev(frame_times)
    return mean, median, stddev

mean_d1, median_d1, stddev_d1 = compute_statistics(frame_times_d1)
mean_d2, median_d2, stddev_d2 = compute_statistics(frame_times_d2)

print('d1-modification frame_times: mean=%f, median=%f, stdev=%f' % (mean_d1, median_d1, stddev_d1))
print('Post-modification frame_times: mean=%f, median=%f, stdev=%f' % (mean_d2, median_d2, stddev_d2))
print('post/d1 =%f ' % (median_d2/median_d1))

# Shapiro-Wilk検定
shapiro_stat, shapiro_p = stats.shapiro(frame_times_d1)

# アンダーソン-ダーリング検定
anderson_stat, anderson_critical, anderson_significance = stats.anderson(frame_times_d1, dist='norm')

# コルモゴロフ-スミルノフ検定
ks_stat, ks_p = stats.kstest(frame_times_d1, 'norm') 

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

print(f"Shapiro-Wilk Test: p-value = {shapiro_p:.3f}")
print(f"Shapiro-Wilk Test: {shapiro_normality}")
print(f"Anderson-Darling Test: statistic = {anderson_stat:.3f}")
print(f"Anderson-Darling: {anderson_normality}")
print(f"Kolmogorov-Smirnov Test: p-value = {ks_p:.3f}")
print(f"Kolmogorov-Smirnov: {ks_normality}")
# Calculate t-test
t_stat, t_p = stats.ttest_ind(frame_times_d1, frame_times_d2)
print('t-test: t=%f, p=%f' % (t_stat, t_p))

# Calculate Mann-Whitney U test (equivalent to Wilcoxon rank-sum test)
u_stat, u_p = stats.mannwhitneyu(frame_times_d1, frame_times_d2)
print('Mann-Whitney U test: U=%f, p=%f' % (u_stat, u_p))

# Calculate Wilcoxon signed-rank test
w_stat, w_p = stats.wilcoxon(frame_times_d1, frame_times_d2)
print('Wilcoxon signed-rank test: W=%f, p=%f' % (w_stat, w_p))

##ヒストグラム
#plt.hist(frame_times_d1, bins=50, alpha=0.5, label='d1')
#plt.hist(frame_times_d2, bins=50, alpha=0.5, label='d2')
##plt.axvline(mean_d1, color='r', linestyle='dashed', lid2idth=1, label='Mean (d1)')
##plt.axvline(median_d1, color='g', linestyle='dotted', lid2idth=1, label='Median (d1)')
#plt.xlabel("FPS")
#plt.ylabel("Frequency")
#plt.title(f"FPS Histogram")
#plt.legend(loc='upper left')
#plt.show()

# ボックスプロットを描画
data = [frame_times_d1, frame_times_d2, frame_times_d3, frame_times_d4]
labels = ['d1', 'd2', 'd3', 'd4']

plt.boxplot(data, labels=labels)
plt.xlabel("Condition")
plt.ylabel("Frametime")
plt.title("Frametime Distribution")
plt.show()

