import gradio as gr

from controller import Controller

css = """
.gradio-container {
    height: 100vh !important;
    max-width: 100vw !important;
    padding: 0 !important;
    margin: 0 !important;
}

#chatbot {
    flex-grow: 1 !important;
    height: calc(100vh - 120px) !important;
    max-height: calc(100vh - 120px) !important;
    overflow: auto !important;
}

#textbox {
    flex-shrink: 0 !important;
}

.gradio-container > div {
    height: 100vh !important;
}
"""


def launch_ui(controller: Controller):
    fn = lambda message, history: controller.answer_on_request(message)
    with gr.Blocks(css=css, fill_width=True) as demo:
        gr.ChatInterface(
            fn=fn,
            title="Code assistant Q&A Chat",
            description="Ask about Ultralytics code",
            examples=[
                "How does YOLO predictor work?",
                "What is the training loss function?",
                "Show dataset class"
            ],
            cache_examples=False
        )

    demo.launch(server_name="0.0.0.0",
                server_port=3005,
                share=True,
                show_error=True,
                quiet=False)
