import gradio as gr
import run_seg
import run_stablediffusion
import pandas as pd
import csv
import os
import pandas as pd

from translator import EnJaTranslator, JaEnTranslator

# fuguapp.py
en_translator = EnJaTranslator()
ja_translator = JaEnTranslator()

def en_translate(text):
    return en_translator(text)

def ja_translate(text):
    return ja_translator(text)

#Segapp.py
score = 0 #塗替え割合の初期値
count_seg = 1.0 #ボーナス倍率の初期値

def segmentation(image, text):
    global score,count_seg
    #物体検知の結果を返す
    #retrun pil_image, mask_image, formatted_score
    results = run_seg.run_grounding_sam(image, "seg", text, 0.3, 0.25)
    if results[1] < 0.03:
        count_seg += 0
    else:
        count_seg += 0.2
    score += results[1]*100*round(count_seg, 1)
    if results:
        first_image = results[0][0]
    else:
        first_image = None
    return results[0], gr.update(value=first_image),gr.update(value="# " + str(score) + "Point!"),gr.update(value="## 現在のボーナス倍率" + str(count_seg) + "倍")

def reset():#リセットボタンが押されたときの処理
    global score,count_seg
    score = 0
    count_seg = 1
    return gr.update(value=None),gr.update(value=None),gr.update(value="# スコアを表示するには検索ボタンを押してスタートしてみてね"),gr.update(value="## 現在のボーナス倍率" + str(count_seg) + "%")

#emg_test.py
def random_words():
    # Load the CSV file
    df = pd.read_csv('dict.csv')
    # Select a random row
    random_rows = df.sample(n=5)  # Change n to the number of words you want
    # Get the 'English' column values from the random rows
    random_words = random_rows["英語"].tolist()
    output = ','.join(random_words)
    return output

def get_random_word():
    df = pd.read_csv('dict.csv')
    random_row = df.sample(n=1).iloc[0]
    english_word = random_row['英語']
    japanese_word = random_row['日本語']
    return english_word, japanese_word

english_word, correct_translation = get_random_word()

def test_translation(user_input, correct_translation):
    if user_input == correct_translation:
        return "正解⭕!"
    else:
        return f"不正解❌! 正しい答え:{correct_translation}"


# dict.py

def add_to_csv(japanese, english):
    # 入力されたデータをCSVファイルに追加
    csv_file_path = 'dict.csv'
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([english, japanese])
    # 更新されたCSVファイルを読み込んで返す
    df = pd.read_csv(csv_file_path)
    return df

def display_csv():
    csv_file_path = 'dict.csv'
    # CSVファイルを読み込んで表示
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        return df
    else:
        return pd.DataFrame(columns=["English", "Japanese"])

#run_stablediffusion.py
def generate_from_text(text ,_=gr.Progress(track_tqdm=True)):
    print(text)
    result = run_stablediffusion.ov_pipe(text, negative_prompt="bad quality", num_inference_steps=40, seed=810)
    return result["sample"][0]

def random_generate_from_text(text ,_=gr.Progress(track_tqdm=True)):
    r_w = random_words()
    new_text = r_w + text
    print(new_text)
    result = run_stablediffusion.ov_pipe(new_text, negative_prompt="bad quality", num_inference_steps=40, seed=810)
    return result["sample"][0]

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Tab("AI画像生成🤖"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("# StableDiffusion+OpenVino+NPUを用いたAI画像生成🤖")
                text_input = gr.Textbox(lines=3, label="どんな世界を生成する？🌏")
                btn = gr.Button("生成する🎨",variant="primary")
                random_btn = gr.Button("辞書から単語を入れて生成する🔮")
                with gr.Accordion("画像生成の使い方"):
                    gr.Markdown("## 1. 左上のテキストボックスに生成したい要素を入れてね")
                    gr.Markdown("### 例: The beautiful moment of the falling sunset seen from the beach,cloud,sky,sea")
                    gr.Markdown("### (要素毎にカンマ(,)で区切ると生成しやすいよ！)")
                    gr.Markdown("### (英語が分からない時は翻訳システムを使ってね！)")
                    gr.Markdown("### 2. 生成ボタンを押して2分程待てば完成！")
                    gr.Markdown("# 既知のエラー🚨")
                    gr.Markdown("## 単語を入れて生成する際にエラーが出る場合はdict.csvに問題があります")
            out = gr.Image(label="生成結果", type="pil")
            random_btn.click(
                random_generate_from_text,
                [text_input],
                out,)
            btn.click(
                    generate_from_text,
                    [text_input],
                    out,
                )
    with gr.Tab("物体検知ゲーム"):
        with gr.Row():
            with gr.Column():
                input_image = gr.Image(label="画像")
                input_text = gr.Textbox(value="Candy", label="見つけた物を英語で入力してね")
            out = gr.Gallery(preview=True, object_fit="scale-down")
        with gr.Row():
            btn = gr.Button(value="けんさくする🔎",variant="primary")
            reset_btn = gr.Button("別の画像ではじめる🖼")
        with gr.Accordion("ゲームのルール", open=False):
            gr.Markdown("# ゲームのルール👾")
            gr.Markdown("### 1. 左上のボックスをクリックして画像を入れてね")
            gr.Markdown("### 2. 画像の中にある物体を見つけて英語で入力してね")
            gr.Markdown("### (色が塗られた範囲が大きい程スコアが高くなるよ！)")
            gr.Markdown("### 3. 見つけた回数によってボーナス倍率が上がるよ！")
            gr.Markdown("# 高スコアのコツ👑")
            gr.Markdown("## 1. 画像の中にある物体を正確に回答するとボーナス倍率が上がりやすい(色や形,ポーズ,大きさ等で分ける)")
            gr.Markdown("## 2. 一番目立つ物体を最後に回答する")
            gr.Markdown("# 既知のエラー🚨")
            gr.Markdown("## 画像が読み込めない場合は何度か入れ直してみてください")
        with gr.Row():
            gr.Markdown("## ↓この画像でのスコア！🎊↓")
            bonus_scale = gr.Markdown("## 現在のボーナス倍率" + str(count_seg) + "倍✨")
        show_score = gr.Markdown("# スコアを表示するには検索ボタンを押してスタートしてみてね")
        # Button click will process the image and then set the output image as the new input image
        btn.click(
            segmentation,
            inputs=[input_image, input_text],
            outputs=[out, input_image,show_score,bonus_scale]
        )
        reset_btn.click(reset, [], [input_image,out,show_score,bonus_scale])
    with gr.Tab("翻訳システム💬"):
        gr.Markdown("## FuguMTを用いた翻訳システム💬")
        gr.Markdown("### (※分からない単語が出てきた時にお使いください)")
        with gr.Accordion("英語から日本語へ翻訳(en→ja)", open=False):
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
        with gr.Accordion("日本語から英語へ翻訳(ja→en)", open=False):
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
    with gr.Tab("辞書📚"):
        gr.Markdown("## 辞書登録システム📚")
        with gr.Row():
            gr.Markdown("### 辞書に登録する単語をセットで入力してください(※誤入力をした際はdict.csvを編集してください)")
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
    with gr.Tab("単語テスト🔖"):
        gr.Markdown("# 単語テスト！")
        english_word_label = gr.Label(value=english_word)
        user_input = gr.Textbox(label="日本語をいれてね")
        correct_answer_hidden = gr.Textbox(value=correct_translation, visible=False)
        with gr.Row():
            submit_btn = gr.Button("こたえあわせ🎈",variant="primary")
            question_btn = gr.Button("問題を作成🔮")
        output = gr.Label()
        question_btn.click(get_random_word, [], [english_word_label, correct_answer_hidden])
        submit_btn.click(test_translation, inputs=[user_input, correct_answer_hidden], outputs=output)

try:
    demo.launch(debug=True)
except Exception:
    print("Exception")