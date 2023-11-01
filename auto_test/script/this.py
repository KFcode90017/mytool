import os
import re
import argparse
import statistics
from scipy import stats
import matplotlib.pyplot as plt

# Pattern to search for glmark2 Score
pattern = r'glmark2 Score: (\d+)'

def extract_scores(directory, scores):
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                log = file.read()
                matches = re.findall(pattern, log)

                for match in matches:
                    score = float(match) # Convert the score to float
                    scores.append(score)

# Setup command-line argument parsing
parser = argparse.ArgumentParser(description='Process log directories.')
parser.add_argument('-p', '--pre', required=True, help='Directory of log files before modification.')
parser.add_argument('-n', '--new', required=True, help='Directory of log files after modification.')
args = parser.parse_args()

# Initialize scores list
scores_pre = []
scores_new = []

# Populate pre_scores and new_scores arrays
extract_scores(args.pre, scores_pre)
extract_scores(args.new, scores_new)

def compute_statistics(scores):
    mean = statistics.mean(scores)
    median = statistics.median(scores)
    stddev = statistics.stdev(scores)
    return mean, median, stddev

mean_pre, median_pre, stddev_pre = compute_statistics(scores_pre)
mean_new, median_new, stddev_new = compute_statistics(scores_new)

print('Pre-modification scores: mean=%f, median=%f, stdev=%f' % (mean_pre, median_pre, stddev_pre))
print('Post-modification scores: mean=%f, median=%f, stdev=%f' % (mean_new, median_new, stddev_new))
print('post/pre =%f ' % (median_new/median_pre))

# Shapiro-Wilk検定
shapiro_stat, shapiro_p = stats.shapiro(scores_pre)

# アンダーソン-ダーリング検定
anderson_stat, anderson_critical, anderson_significance = stats.anderson(scores_pre, dist='norm')

# コルモゴロフ-スミルノフ検定
ks_stat, ks_p = stats.kstest(scores_pre, 'norm') 

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
t_stat, t_p = stats.ttest_ind(scores_pre, scores_new)
print('t-test: t=%f, p=%f' % (t_stat, t_p))

# Calculate Mann-Whitney U test (equivalent to Wilcoxon rank-sum test)
u_stat, u_p = stats.mannwhitneyu(scores_pre, scores_new)
print('Mann-Whitney U test: U=%f, p=%f' % (u_stat, u_p))

# Calculate Wilcoxon signed-rank test
w_stat, w_p = stats.wilcoxon(scores_pre, scores_new)
print('Wilcoxon signed-rank test: W=%f, p=%f' % (w_stat, w_p))


print('\n')
print(scores_pre)
print('\n')
print(scores_new)

#ヒストグラム
plt.hist(scores_pre, bins=100, alpha=0.5, label='pre')
plt.hist(scores_new, bins=100, alpha=0.5, label='new')
plt.axvline(mean_pre, color='r', linestyle='dashed', linewidth=1, label='Mean (Pre)')
plt.axvline(median_pre, color='g', linestyle='dotted', linewidth=1, label='Median (Pre)')
plt.xlabel("FPS")
plt.ylabel("Frequency")
plt.title(f"FPS Histogram")
plt.legend(loc='upper left')
plt.show()

