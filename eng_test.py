import pandas as pd
import gradio as gr


# ランダムに単語を選択する関数
def get_random_word():
    df = pd.read_csv('dict.csv')
    random_row = df.sample(n=1).iloc[0]
    english_word = random_row['英語']
    japanese_word = random_row['日本語']
    return english_word, japanese_word

# 翻訳をテストする関数
def test_translation(user_input, correct_translation):
    if user_input == correct_translation:
        return "正解⭕!"
    else:
        return f"不正解❌! 正しい答え:{correct_translation}"

# Gradioインターフェースを定義
english_word, correct_translation = get_random_word()

with gr.Blocks() as demo:
    gr.Markdown("# 単語テスト！")
    
    # ランダムに選ばれた英単語を表示
    english_word_label = gr.Label(value=english_word)
    
    # ユーザーの入力を受け付けるテキストボックス
    user_input = gr.Textbox(label="日本語をいれてね")
    
    # 正しい翻訳を隠しフィールドに保持
    correct_answer_hidden = gr.Textbox(value=correct_translation, visible=False)
    
    with gr.Row():
        submit_btn = gr.Button("こたえあわせ🎈",variant="primary")
        question_btn = gr.Button("問題を作成🔮")
    
    # 結果を表示するラベル
    output = gr.Label()
    
    question_btn.click(get_random_word, [], [english_word_label, correct_answer_hidden])
    # ボタンがクリックされたときに翻訳をテストする
    submit_btn.click(test_translation, inputs=[user_input, correct_answer_hidden], outputs=output)

# Gradioインターフェースを起動
demo.launch()