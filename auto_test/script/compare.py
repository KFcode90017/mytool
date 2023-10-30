import os
import re
import argparse

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

print('Scores from pre-modification directory:', scores_pre)
print('Scores from post-modification directory:', scores_new)

