import gradio as gr
import run_seg

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
    return results[0], gr.update(value=first_image),gr.update(value="# " + str(score) + "Point!"),gr.update(value="## 現在のボーナス倍率" + str(count_seg) + "%")

def reset():#リセットボタンが押されたときの処理
    global score,count_seg
    score = 0
    count_seg = 1
    return gr.update(value=None),gr.update(value=None),gr.update(value="# スコアを表示するには検索ボタンを押してスタートしてみてね"),gr.update(value="## 現在のボーナス倍率" + str(count_seg) + "%")

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Tab("物体検知ゲーム"):
        with gr.Row():
            with gr.Column():
                input_image = gr.Image(label="画像")
                input_text = gr.Textbox(value="", label="見つけた物を英語で入力してね")
            out = gr.Gallery(preview=True, object_fit="scale-down")
        with gr.Row():
            btn = gr.Button(value="けんさくする🔎",variant="primary")
            reset_btn = gr.Button("別の画像ではじめる🖼")
        with gr.Accordion(value="ゲームのルール", open=False):
            gr.Markdown("# ゲームのルール👾")
            gr.Markdown("### 1. 左上のボックスをクリックして画像を入れてね")
            gr.Markdown("### 2. 画像の中にある物体を見つけて英語で入力してね")
            gr.Markdown("### (色が塗られた範囲が大きい程スコアが高くなるよ！)")
            gr.Markdown("### 3. 見つけた回数によってボーナス倍率が上がるよ！")
            gr.Markdown("# 高スコアのコツ👑")
            gr.Markdown("## 1. 画像の中にある物体を正確に回答するとボーナス倍率が上がりやすい(色や形,ポーズ,大きさ等で分ける)")
            gr.Markdown("## 2. 一番目立つ物体を最後に回答する")
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

try:
    demo.launch()
except Exception as e:
    print("Exception:", e)