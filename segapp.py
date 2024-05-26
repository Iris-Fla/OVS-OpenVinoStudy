import gradio as gr
import run_seg

def segmentation(image, text):
    return run_seg.run_grounding_sam(image, "det", text,0.3,0.25)

with gr.Blocks() as demo:
    with gr.Tab("物体検知"):
        with gr.Row():
            with gr.Column():
                input_image = gr.Image()
                input_text = gr.Textbox(value="Candy", label="Text Prompt")
            out = gr.Gallery(preview=True, object_fit="scale-down")
        btn = gr.Button()
        btn.click(
            segmentation,
            [input_image, input_text],
            out,
        )

try:
    demo.launch()
except Exception:
    print("Exception")