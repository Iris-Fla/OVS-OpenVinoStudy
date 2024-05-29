import pandas as pd

# Load the CSV file
df = pd.read_csv('dict.csv')

# Select a random row
random_rows = df.sample(n=5)  # Change n to the number of words you want

# Get the 'English' column values from the random rows
random_words = random_rows["英語"].tolist()

output = ','.join(random_words)

print(output)