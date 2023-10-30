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

# Calculate t-test
t_stat, t_p = stats.ttest_ind(scores_pre, scores_new)
print('t-test: t=%f, p=%f' % (t_stat, t_p))

# Calculate Mann-Whitney U test (equivalent to Wilcoxon rank-sum test)
u_stat, u_p = stats.mannwhitneyu(scores_pre, scores_new)
print('Mann-Whitney U test: U=%f, p=%f' % (u_stat, u_p))

# Calculate Wilcoxon signed-rank test
w_stat, w_p = stats.wilcoxon(scores_pre, scores_new)
print('Wilcoxon signed-rank test: W=%f, p=%f' % (w_stat, w_p))


#ヒストグラム
plt.hist(scores_pre, bins=100)
#plt.hist(scores_new, bins=20)
plt.xlabel("FPS")
plt.ylabel("Frequency")
plt.title(f"FPS Histogram")
plt.show()
