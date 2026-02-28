import gradio as gr

def hello():
    return "✅ Render fonctionne correctement !"

with gr.Blocks() as app:
    gr.Markdown("# Test Deployment")
    btn = gr.Button("Tester")
    output = gr.Textbox(label="Resultat")

    btn.click(fn=hello, inputs=[], outputs=output)

app.launch(server_name="0.0.0.0", server_port=7860)
