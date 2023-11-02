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
                    frametime = float(match) # Convert the frametime to float
                    frame_times_1_file.append(frametime)

                # 1つのログファイルのFrameTimeの平均を算出
                if frame_times_1_file:
                    avg_time = sum(frame_times_1_file) / len(frame_times_1_file)
                    frame_times.append(avg_time)

parser = argparse.ArgumentParser(description='Process log directories.')
parser.add_argument('-p', '--pre', required=True, help='Directory of log files before modification.')
parser.add_argument('-n', '--new', required=True, help='Directory of log files after modification.')
args = parser.parse_args()

# Initialize frametimes list
frame_times_pre = []
frame_times_new = []
extract_frametimes(args.pre, frame_times_pre)
extract_frametimes(args.new, frame_times_new)

def compute_statistics(frame_times):
    mean = statistics.mean(frame_times)
    median = statistics.median(frame_times)
    stddev = statistics.stdev(frame_times)
    return mean, median, stddev

mean_pre, median_pre, stddev_pre = compute_statistics(frame_times_pre)
mean_new, median_new, stddev_new = compute_statistics(frame_times_new)

print('Pre-modification frame_times: mean=%f, median=%f, stdev=%f' % (mean_pre, median_pre, stddev_pre))
print('Post-modification frame_times: mean=%f, median=%f, stdev=%f' % (mean_new, median_new, stddev_new))
print('post/pre =%f ' % (median_new/median_pre))

# Shapiro-Wilk検定
shapiro_stat, shapiro_p = stats.shapiro(frame_times_pre)

# アンダーソン-ダーリング検定
anderson_stat, anderson_critical, anderson_significance = stats.anderson(frame_times_pre, dist='norm')

# コルモゴロフ-スミルノフ検定
ks_stat, ks_p = stats.kstest(frame_times_pre, 'norm') 

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
t_stat, t_p = stats.ttest_ind(frame_times_pre, frame_times_new)
print('t-test: t=%f, p=%f' % (t_stat, t_p))

# Calculate Mann-Whitney U test (equivalent to Wilcoxon rank-sum test)
u_stat, u_p = stats.mannwhitneyu(frame_times_pre, frame_times_new)
print('Mann-Whitney U test: U=%f, p=%f' % (u_stat, u_p))

# Calculate Wilcoxon signed-rank test
w_stat, w_p = stats.wilcoxon(frame_times_pre, frame_times_new)
print('Wilcoxon signed-rank test: W=%f, p=%f' % (w_stat, w_p))

#ヒストグラム
plt.hist(frame_times_pre, bins=50, alpha=0.5, label='pre')
plt.hist(frame_times_new, bins=50, alpha=0.5, label='new')
#plt.axvline(mean_pre, color='r', linestyle='dashed', linewidth=1, label='Mean (Pre)')
#plt.axvline(median_pre, color='g', linestyle='dotted', linewidth=1, label='Median (Pre)')
plt.xlabel("FPS")
plt.ylabel("Frequency")
plt.title(f"FPS Histogram")
plt.legend(loc='upper left')
plt.show()

