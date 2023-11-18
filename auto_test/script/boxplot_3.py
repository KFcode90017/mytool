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
args = parser.parse_args()

frame_times_d1 = []
frame_times_d2 = []
frame_times_d3 = []

extract_frametimes(args.d1, frame_times_d1)
extract_frametimes(args.d2, frame_times_d2)
extract_frametimes(args.d3, frame_times_d3)


def compute_statistics(frame_times):
    mean = statistics.mean(frame_times)
    median = statistics.median(frame_times)
    stddev = statistics.stdev(frame_times)
    return mean, median, stddev

mean_d1, median_d1, stddev_d1 = compute_statistics(frame_times_d1)
mean_d2, median_d2, stddev_d2 = compute_statistics(frame_times_d2)
mean_d3, median_d3, stddev_d3 = compute_statistics(frame_times_d3)

print('d1-modification frame_times: mean=%f, median=%f, stdev=%f' % (mean_d1, median_d1, stddev_d1))
print('d2-modification frame_times: mean=%f, median=%f, stdev=%f' % (mean_d2, median_d2, stddev_d2))
print('d3-modification frame_times: mean=%f, median=%f, stdev=%f' % (mean_d3, median_d3, stddev_d3))
print("\n")
print('d1-1s=%f' %(mean_d1+1*stddev_d1))
print('d1-2s=%f' %(mean_d1+2*stddev_d1))
print('d1-3s=%f' %(mean_d1+3*stddev_d1))
print("\n")
print('d2/d1 =%f ' % (median_d2/median_d1))

# Shapiro-Wilk検定
shapiro_stat1, shapiro_p1 = stats.shapiro(frame_times_d1)
shapiro_stat2, shapiro_p2 = stats.shapiro(frame_times_d2)
shapiro_stat3, shapiro_p3 = stats.shapiro(frame_times_d3)

if shapiro_p1 > 0.05:
    shapiro_normality_d1 = "OK"
else:
    shapiro_normality_d1 = "NOT"
if shapiro_p2 > 0.05:
    shapiro_normality_d2 = "OK"
else:
    shapiro_normality_d2 = "NOT"
if shapiro_p3 > 0.05:
    shapiro_normality_d3 = "OK"
else:
    shapiro_normality_d3 = "NOT"

print(f"Shapiro-Wilk Test_d1: p-value = {shapiro_p1:.3f}")
print(f"Shapiro-Wilk Test_d1: {shapiro_normality_d1}")
print(f"Shapiro-Wilk Test_d2: p-value = {shapiro_p2:.3f}")
print(f"Shapiro-Wilk Test_d2: {shapiro_normality_d2}")
print(f"Shapiro-Wilk Test_d3: p-value = {shapiro_p3:.3f}")
print(f"Shapiro-Wilk Test_d3: {shapiro_normality_d3}")

# アンダーソン-ダーリング検定
anderson_stat1, anderson_critical1, anderson_significance1= stats.anderson(frame_times_d1, dist='norm')
anderson_stat2, anderson_critical2, anderson_significance2= stats.anderson(frame_times_d2, dist='norm')
anderson_stat3, anderson_critical3, anderson_significance3= stats.anderson(frame_times_d3, dist='norm')

if all(anderson_significance1 > 0.05):
    anderson_normality_d1 = "OK"
else:
    anderson_normality_d1 = "NOT"
if all(anderson_significance2 > 0.05):
    anderson_normality_d2 = "OK"
else:
    anderson_normality_d2 = "NOT"
if all(anderson_significance3 > 0.05):
    anderson_normality_d3 = "OK"
else:
    anderson_normality_d3 = "NOT"

print(f"Anderson-Darling Test_d1: statistic = {anderson_stat1:.3f}")
print(f"Anderson-Darling Test_d1: {anderson_normality_d1}")
print(f"Anderson-Darling Test_d2: statistic = {anderson_stat2:.3f}")
print(f"Anderson-Darling Test_d2: {anderson_normality_d2}")
print(f"Anderson-Darling Test_d3: statistic = {anderson_stat3:.3f}")
print(f"Anderson-Darling Test_d3: {anderson_normality_d3}")

# コルモゴロフ-スミルノフ検定
ks_stat1, ks_p1 = stats.kstest(frame_times_d1, 'norm') 
ks_stat2, ks_p2 = stats.kstest(frame_times_d2, 'norm') 
ks_stat3, ks_p3 = stats.kstest(frame_times_d3, 'norm') 

if ks_p1 > 0.05:
    ks_normality1 = "OK"
else:
    ks_normality1 = "NOT"
if ks_p2 > 0.05:
    ks_normality2 = "OK"
else:
    ks_normality2 = "NOT"
if ks_p3 > 0.05:
    ks_normality3 = "OK"
else:
    ks_normality3 = "NOT"

print(f"Kolmogorov-Smirnov Test_d1: p-value = {ks_p1:.3f}")
print(f"Kolmogorov-Smirnov Test_d1: {ks_normality1}")
print(f"Kolmogorov-Smirnov Test_d2: p-value = {ks_p2:.3f}")
print(f"Kolmogorov-Smirnov Test_d2: {ks_normality2}")
print(f"Kolmogorov-Smirnov Test_d3: p-value = {ks_p3:.3f}")
print(f"Kolmogorov-Smirnov Test_d3: {ks_normality3}")
print("\n")

# Calculate t-test
t_stat, t_p = stats.ttest_ind(frame_times_d1, frame_times_d2)
print('t-test d1 vs d2: t=%f, p=%f' % (t_stat, t_p))
t_stat, t_p = stats.ttest_ind(frame_times_d1, frame_times_d3)
print('t-test d1 vs d3: t=%f, p=%f' % (t_stat, t_p))

# Calculate Mann-Whitney U test (equivalent to Wilcoxon rank-sum test)
u_stat, u_p = stats.mannwhitneyu(frame_times_d1, frame_times_d2)
print('Mann-Whitney U test d1 vs d2: U=%f, p=%f' % (u_stat, u_p))
u_stat, u_p = stats.mannwhitneyu(frame_times_d1, frame_times_d3)
print('Mann-Whitney U test d1 vs d3: U=%f, p=%f' % (u_stat, u_p))

# Calculate Wilcoxon signed-rank test
w_stat, w_p = stats.wilcoxon(frame_times_d1, frame_times_d2)
print('Wilcoxon signed-rank test d1 vs d2: W=%f, p=%f' % (w_stat, w_p))
w_stat, w_p = stats.wilcoxon(frame_times_d1, frame_times_d3)
print('Wilcoxon signed-rank test d1 vs d3: W=%f, p=%f' % (w_stat, w_p))

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
data = [frame_times_d1, frame_times_d2, frame_times_d3]
labels = ['d1', 'd2', 'd3']

plt.boxplot(data, labels=labels)
# y軸の上限を設定（上方向に10%の余白を設ける）
plt.ylim(ymax = max(max(frame_times_d1), max(frame_times_d2), max(frame_times_d3)) * 1.03)
plt.yticks(fontsize=10)
#plt.xlabel("Condition")
#plt.ylabel("Frametime", fontsize=14)
#plt.title("Frametime Distribution")
plt.show()

