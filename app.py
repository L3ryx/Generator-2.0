import gradio as gr
import os
from openai import OpenAI

# ===============================
# API CONFIG
# ===============================

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# ===============================
# TEST API FUNCTION
# ===============================

def test_api():
    try:
        client.models.list()
        return "✅ API Connected Successfully"
    except Exception as e:
        return f"❌ API Error: {str(e)}"

# ===============================
# PROMPT GENERATOR (INTELLIGENT)
# ===============================

def generate_prompt(gender, random_mode, top_choice,
                    bottom_choice, beach_mode,
                    swimsuit_type, shot_type):

    if gender == "Man":
        beach_mode = False

    system_instruction = """
You are a professional fashion prompt generator.
Generate a unique high realism image prompt.

Rules:
- 800x1000px
- DSLR camera
- 50mm lens
- Cinematic lighting
- Always centered
- Always wearing sunglasses from attached image
- Sunglasses must be main focal point
- Environment must match lifestyle fashion
- Output must be written only in English
"""

    user_instruction = f"""
Gender: {gender}
Random Mode: {random_mode}
Top: {top_choice}
Bottom: {bottom_choice}
Beach Mode: {beach_mode}
Swimsuit Type: {swimsuit_type}
Camera Shot: {shot_type}

Create a unique variation.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_instruction}
        ],
        temperature=1.3,
        top_p=0.95
    )

    return response.choices[0].message.content

# ===============================
# INTERFACE
# ===============================

with gr.Blocks(title="Nano Banana Generator") as app:

    gr.Markdown("# 🧬 Nano Banana Advanced Prompt Generator")

    gender = gr.Radio(["Man", "Woman"], label="Genre")

    random_mode = gr.Checkbox(label="Random Mode")

    top_choice = gr.Dropdown(
        ["Oversized T-shirt", "Hoodie", "Shirt", "Crop Top", "Blouse"],
        label="Top Selection"
    )

    bottom_choice = gr.Dropdown(
        ["Jeans", "Cargo Pants", "Shorts", "Skirt", "Leggings"],
        label="Bottom Selection"
    )

    beach_mode = gr.Checkbox(label="Beach Mode (Only for Women)")

    swimsuit_type = gr.Radio(
        ["One-piece", "Two-piece"],
        label="Swimsuit Type"
    )

    shot_type = gr.Dropdown(
        ["Close-up", "Medium Shot", "Full Body", "Low Angle", "High Angle"],
        label="Camera View"
    )

    generate_btn = gr.Button("🚀 Generate Prompt")

    output = gr.Textbox(label="Generated Prompt", lines=15)

    test_btn = gr.Button("🧪 Test API Connection")
    test_output = gr.Textbox(label="API Status")

    generate_btn.click(
        fn=generate_prompt,
        inputs=[gender, random_mode, top_choice,
                bottom_choice, beach_mode,
                swimsuit_type, shot_type],
        outputs=output
    )

    test_btn.click(
        fn=test_api,
        inputs=[],
        outputs=test_output
    )

# ===============================
# RUN SERVER (RENDER COMPATIBLE)
# ===============================

app.launch(server_name="0.0.0.0", server_port=7860)
