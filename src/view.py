import gradio as gr

from controller import Controller


def launch_ui(controller: Controller):
    fn = lambda message, history: controller.answer_on_request(message)
    demo = gr.ChatInterface(
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
                quiet=False)
