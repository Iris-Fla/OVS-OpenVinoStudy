import gradio as gr
import pandas as pd
import csv
import os

from translator import EnJaTranslator, JaEnTranslator

en_translator = EnJaTranslator()
ja_translator = JaEnTranslator()

def en_translate(text):
    return en_translator(text)

def ja_translate(text):
    return ja_translator(text)

# CSVファイルのパスを定義
csv_file_path = 'dict.csv'

def add_to_csv(japanese, english):
    # 入力されたデータをCSVファイルに追加
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([english, japanese])
    # 更新されたCSVファイルを読み込んで返す
    df = pd.read_csv(csv_file_path)
    return df

def display_csv():
    # CSVファイルを読み込んで表示
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        return df
    else:
        return pd.DataFrame(columns=["English", "Japanese"])

with gr.Blocks() as demo:
    with gr.Tab("単語検索,辞書"):
        gr.Markdown("## FuguMTを用いた翻訳システム")
        gr.Markdown("### (※分からない単語が出てきた時にお使いください)")
        with gr.Accordion("英語から日本語へ翻訳", open=False):
            with gr.Row():
                with gr.Column():
                    input_text = gr.Textbox(lines=3, label="英語をいれてね")
                out = gr.Textbox(label="結果")
            btn = gr.Button()
            btn.click(
                en_translate,
                [input_text],
                out
            )
        with gr.Accordion("日本語から英語へ翻訳", open=False):
            with gr.Row():
                with gr.Column():
                    input_text = gr.Textbox(lines=3, label="日本語をいれてね")
                out = gr.Textbox(label="結果")
            btn = gr.Button()
            btn.click(
                ja_translate,
                [input_text],
                out,
            )
    with gr.Tab("辞書"):
        gr.Markdown("## 辞書登録システム")
        with gr.Row():
            gr.Markdown("### 辞書に登録する単語を入力してください(※誤入力をした際はdict.csvを編集してください)")
            english_input = gr.Textbox(label="英語")
            japanese_input = gr.Textbox(label="日本語")
            japanese_input.submit(lambda x: gr.update(value=""),[],[japanese_input,english_input])
        add_button = gr.Button("辞書に追加")
        # 追加ボタンが押されたときにadd_to_csv関数を呼び出す
        add_button.click(add_to_csv, inputs=[japanese_input, english_input])
        add_button.click(lambda x: gr.update(value=''), [],[japanese_input])
        add_button.click(lambda x: gr.update(value=''), [],[english_input])
        # 現在のCSVファイルの内容を表示
        gr.Markdown("### 現在の辞書内容(辞書追加した後は更新してください)")
        btn = gr.Button("辞書を更新する")
        output_display = gr.DataFrame(value=display_csv())
        btn.click(display_csv,outputs=output_display)


try:
    demo.launch()
except Exception:
    print("Exception")