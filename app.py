import gradio as gr
import os
import random
import requests

# =====================================================
# HUGGING FACE CONFIG
# =====================================================

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/distilgpt2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# =====================================================
# LISTES
# =====================================================

TOP_LIST = ["Oversized T-shirt", "Hoodie", "Shirt", "Crop Top", "Blouse"]
BOTTOM_LIST = ["Jeans", "Cargo Pants", "Shorts", "Skirt", "Leggings"]
ENV_LIST = [
    "Urban Lifestyle",
    "Luxury Hotel",
    "City Street",
    "Modern Apartment"
]
COLOR_LIST = [
    "Neutral Colors",
    "Pastel Colors",
    "Black & White",
    "Earth Tone"
]
SHOT_LIST = [
    "Close-up",
    "Medium Shot",
    "Full Body",
    "Low Angle",
    "High Angle"
]

# =====================================================
# AUTO FUNCTIONS
# =====================================================

def auto_top():
    return random.choice(TOP_LIST)

def auto_bottom():
    return random.choice(BOTTOM_LIST)

def auto_env(beach_mode):
    if beach_mode:
        return random.choice(["Beach", "Pool Area"])
    return random.choice(ENV_LIST)

def auto_colors():
    return random.choice(COLOR_LIST)

# =====================================================
# HUGGING FACE GENERATION (distilgpt2)
# =====================================================

def generate_with_hf(prompt):

    if not HF_TOKEN:
        return "❌ HF_TOKEN not configured"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 500,
            "temperature": 0.9,
            "top_p": 0.95,
            "do_sample": True
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    result = response.json()

    if isinstance(result, list):
        return result[0].get("generated_text", "No text generated")

    return str(result)

# =====================================================
# 🔥 PROMPT GENERATOR (TOUTES TES INSTRUCTIONS MAINTENUES)
# =====================================================

def generate_prompt(
    gender,
    beach_mode,
    auto_top_toggle,
    auto_bottom_toggle,
    auto_env_toggle,
    auto_color_toggle,
    top,
    bottom,
    env,
    colors,
    shot
):

    # ---- Désactivation intelligente ----
    if gender == "Man":
        beach_mode = False

    # ---- Auto system ----
    if auto_top_toggle:
        top = auto_top()

    if auto_bottom_toggle:
        bottom = auto_bottom()

    if auto_env_toggle:
        env = auto_env(beach_mode)

    if auto_color_toggle:
        colors = auto_colors()

    # =====================================================
    # 🚀 TES RÈGLES INTELLIGENTES DE PROMPT
    # =====================================================

    system_rules = """
You are a professional fashion prompt engineer.

Rules:
- Always centered
- High realism
- Always wearing sunglasses from attached image
- Sunglasses must be main focal point
- The sunglasses must never be described as part of outfit
- Cinematic lighting
- Professional photography look
- 800x1000px
- DSLR camera
- 50mm lens
- Shallow depth of field
- Background slightly blurred
- Output in English
"""

    user_prompt = f"""
Generate a unique fashion image prompt.

Gender: {gender}
Beach Mode: {beach_mode}
Top: {top}
Bottom: {bottom}
Environment: {env}
Colors: {colors}
Camera Shot: {shot}

Apply all professional rules.
Follow system instructions.
"""

    final_prompt = system_rules + "\n" + user_prompt

    # Send to distilgpt2
    result = generate_with_hf(final_prompt)

    return result


# =====================================================
# TEST TOKEN
# =====================================================

def test_hf():
    if not HF_TOKEN:
        return "❌ HF_TOKEN NOT FOUND"
    return "✅ HF_TOKEN LOADED"


# =====================================================
# INTERFACE (TON DESIGN + BACKGROUND IMAGE)
# =====================================================

with gr.Blocks(
    title="Nano Banana",
    css="""
    body {
        background-image: url('https://i.postimg.cc/FHC5G1FX/nano-banana-logo.png');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }

    .gr-button {
        background-color: red !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold;
        box-shadow: 0 0 15px red;
    }

    .gr-button:hover {
        box-shadow: 0 0 30px red;
        transform: scale(1.05);
    }

    textarea, input, select {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #00ffff !important;
    }
    """
) as app:

    gr.Markdown("# 🚀 Nano Banana Prompt Generator - distilgpt2")

    gender = gr.Radio(["Man", "Woman"], label="Gender")
    beach_mode = gr.Checkbox(label="Beach Mode")

    auto_top_toggle = gr.Checkbox(label="Auto Top")
    auto_bottom_toggle = gr.Checkbox(label="Auto Bottom")
    auto_env_toggle = gr.Checkbox(label="Auto Environment")
    auto_color_toggle = gr.Checkbox(label="Auto Colors")

    top = gr.Textbox(label="Top")
    bottom = gr.Textbox(label="Bottom")
    env = gr.Textbox(label="Environment")
    colors = gr.Textbox(label="Colors")

    shot = gr.Dropdown(SHOT_LIST, label="Camera Shot")

    generate_btn = gr.Button("🚀 Generate Prompt")
    output = gr.Textbox(label="Final Prompt", lines=15)

    test_btn = gr.Button("🧪 Test HF Token")
    test_output = gr.Textbox(label="Status")

    generate_btn.click(
        generate_prompt,
        inputs=[
            gender,
            beach_mode,
            auto_top_toggle,
            auto_bottom_toggle,
            auto_env_toggle,
            auto_color_toggle,
            top,
            bottom,
            env,
            colors,
            shot
        ],
        outputs=output
    )

    test_btn.click(test_hf, outputs=test_output)


# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860
    )
