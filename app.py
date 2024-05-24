import gradio as gr
import run_seg

with gr.Accordion("Advanced options", open=False) as advanced:
    box_threshold = gr.Slider(label="Box Threshold", minimum=0.0, maximum=1.0, value=0.3, step=0.05)
    text_threshold = gr.Slider(label="Text Threshold", minimum=0.0, maximum=1.0, value=0.25, step=0.05)

demo = gr.Interface(
    run_seg.run_grounding_sam,
    [
        gr.Image(),
        gr.Dropdown(["det", "seg"], value="seg", label="task_type"),
        gr.Textbox(value="bears", label="Text Prompt"),
    ],
    additional_inputs=[
        box_threshold,
        text_threshold,
    ],
    outputs=gr.Gallery(preview=True, object_fit="scale-down"),
    examples=[
        [f"{run_seg.ground_dino_dir}/.asset/demo2.jpg", "seg", "dog, forest"],
        [f"{run_seg.ground_dino_dir}/.asset/demo7.jpg", "seg", "horses and clouds"],
    ],
    additional_inputs_accordion=advanced,
)

try:
    demo.launch()
except Exception:
    print("Error?")