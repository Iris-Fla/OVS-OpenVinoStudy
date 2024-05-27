import csv

# 日本語と英語の辞書を作成
japanese_english_dict = {
    "こんにちは": "Hello",
    "さようなら": "Goodbye",
    "ありがとう": "Thank you",
    "すみません": "Excuse me",
    "はい": "Yes",
    "いいえ": "No"
}

# 辞書をCSVファイルに保存
with open('dict.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in japanese_english_dict.items():
        writer.writerow([key, value])

print("辞書がCSVファイルに保存されました。")

# 空の辞書を作成
japanese_english_dict_from_file = {}

# CSVファイルから辞書を読み込む
with open('dict.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        japanese_english_dict_from_file[row[0]] = row[1]

# 読み込んだ辞書を表示
print("\nCSVファイルから読み込んだ辞書:")
for key, value in japanese_english_dict_from_file.items():
    print(f"{key}: {value}")
