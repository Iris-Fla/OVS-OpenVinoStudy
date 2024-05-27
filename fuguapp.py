import gradio as gr
from translator import EnJaTranslator, JaEnTranslator

en_translator = EnJaTranslator()
ja_translator = JaEnTranslator()

def en_translate(text):
    return en_translator(text)

def ja_translate(text):
    return ja_translator(text)

with gr.Blocks() as demo:
    with gr.Tab("単語検索,辞書"):
        with gr.Accordion("英語から日本語へ翻訳", open=False):
            with gr.Row():
                with gr.Column():
                    input_text = gr.Textbox(lines=3, label="英語をいれてね")
                out = gr.Textbox(label="結果")
            btn = gr.Button()
            btn.click(
                en_translate,
                [input_text],
                out,
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


try:
    demo.launch()
except Exception:
    print("Exception")