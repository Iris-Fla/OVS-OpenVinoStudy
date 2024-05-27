import gradio as gr
import pandas as pd
import csv
import os

# CSVファイルのパスを定義
csv_file_path = 'dict.csv'

# 初回実行時にCSVファイルが存在しない場合、ヘッダーを作成
if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Japanese", "English"])

def add_to_csv(japanese, english):
    # 入力されたデータをCSVファイルに追加
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([japanese, english])
    
    # 更新されたCSVファイルを読み込んで返す
    df = pd.read_csv(csv_file_path)
    return df,gr.update(value=""), gr.update(value="")

def display_csv():
    # CSVファイルを読み込んで表示
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        return df
    else:
        return pd.DataFrame(columns=["Japanese", "English"])

# Gradioインターフェースの作成
with gr.Blocks() as demo:
    gr.Markdown("## 日本語と英語の辞書登録システム")
    with gr.Row():
        gr.Markdown("### 辞書に登録する単語を入力してください(※誤入力をした際はdict.csvを編集してください)")
        japanese_input = gr.Textbox(label="日本語")
        english_input = gr.Textbox(label="英語")

    # 追加ボタン
    add_button = gr.Button("辞書に追加")

    # 追加ボタンが押されたときにadd_to_csv関数を呼び出す
    add_button.click(add_to_csv, inputs=[japanese_input, english_input])
    # 現在のCSVファイルの内容を表示
    gr.Markdown("### 現在の辞書内容")
    btn = gr.Button("辞書を更新する")
    output_display = gr.DataFrame(value=display_csv())
    btn.click(display_csv,outputs=output_display)

demo.launch()