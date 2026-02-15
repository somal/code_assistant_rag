import gradio as gr


def qa_response(message, history):
    """Simple mock Q&A: provides predefined responses based on keywords."""
    responses = {
        "weather": "The weather is sunny and 22°C today in Tbilisi.",
        "gym": "For gyms in Tbilisi, try Aspria or Green Hall—great for your fitness routine.",
        "python": "Python is excellent for ML; use async for scalable apps like Ray Serve.",
        "llm": "Fine-tune LLMs with LoRA/PEFT on HuggingFace for efficient results.",
        "default": "Interesting question! Tell me more about machine learning or fitness."
    }

    message_lower = message.lower()
    response = next((r for k, r in responses.items() if k in message_lower), responses["default"])

    return response


demo = gr.ChatInterface(
    fn=qa_response,
    title="Code assistant Q&A Chat",
    description="Ask about Ultralytics code",
    examples=[
        "How does YOLO predictor work?",
        "What is the training loss function?",
        "Show dataset class"
    ],
    cache_examples=False
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
