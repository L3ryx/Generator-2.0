import gradio as gr
import os
import random
import requests
import re

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
    "Urban lifestyle street",
    "Luxury hotel interior",
    "City street golden hour",
    "Modern apartment aesthetic",
    "Beach sunset",
    "Pool area luxury"
]

COLOR_LIST = [
    "Neutral tones",
    "Pastel colors",
    "Black and white style",
    "Earth tone palette"
]

SHOT_LIST = [
    "Centered composition",
    "Medium shot",
    "Full body portrait",
    "Close-up portrait",
    "Low angle cinematic"
]

# =====================================================
# UTILITIES
# =====================================================

def auto_choice(list_items):
    return random.choice(list_items)

# =====================================================
# GENERATION VIA HUGGINGFACE
# =====================================================

def generate_with_hf(prompt):

    if not HF_TOKEN:
        return "❌ HF_TOKEN NOT CONFIGURED"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 450,
            "temperature": 0.8,
            "top_p": 0.9,
            "do_sample": True
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    result = response.json()

    if isinstance(result, list):
        return result[0].get("generated_text", "")

    return str(result)

# =====================================================
# 🔥 POST PROCESSING ENGINE (PRO FEATURE)
# =====================================================

def clean_and_optimize(text):

    # Supprime répétitions inutiles
    text = re.sub(r"\n+", "\n", text)

    # Supprime phrases inutiles souvent générées par distilgpt2
    remove_phrases = [
        "You are",
        "As an AI",
        "I cannot",
        "Sure,",
        "Here is"
    ]

    for phrase in remove_phrases:
        text = text.replace(phrase, "")

    # Force format image prompt clair
    text += "\n\n-- Optimized for Image Generation --"

    return text.strip()

# =====================================================
# MAIN GENERATOR (PRO LEVEL)
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

    # 🔥 Logique intelligente
    if gender == "Man":
        beach_mode = False

    if auto_top_toggle:
        top = auto_choice(TOP_LIST)

    if auto_bottom_toggle:
        bottom = auto_choice(BOTTOM_LIST)

    if auto_env_toggle:
        env = auto_choice(ENV_LIST)

    if auto_color_toggle:
        colors = auto_choice(COLOR_LIST)

    # ===============================
    # SYSTEM RULES STRICT FOR MODEL
    # ===============================

    system_prompt = """
Generate a professional image generation prompt.

Rules:
- Always centered
- High realism
- Cinematic lighting
- 800x1000px
- DSLR camera
- 50mm lens
- Shallow depth of field
- Background blur
- Model wearing sunglasses from attached image
- Sunglasses must be main visual focus
- Sunglasses must NOT be described as outfit
- Output in clean structured format
- English only
"""

    user_prompt = f"""
Create optimized prompt.

Gender: {gender}
Beach: {beach_mode}
Top: {top}
Bottom: {bottom}
Environment: {env}
Colors: {colors}
Shot: {shot}

Apply professional optimization.
"""

    final_prompt = system_prompt + "\n" + user_prompt

    # 🔥 Génération brute
    raw_output = generate_with_hf(final_prompt)

    # 🔥 Post Processing Intelligent
    optimized_output = clean_and_optimize(raw_output)

    return optimized_output


# =====================================================
# TEST TOKEN
# =====================================================

def test_hf():
    if not HF_TOKEN:
        return "❌ HF TOKEN NOT FOUND"
    return "✅ HF TOKEN OK"


# =====================================================
# INTERFACE UI
# =====================================================

with gr.Blocks(
    title="Nano Banana AI",
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
    }

    textarea, input, select {
        background-color: #0f172a !important;
        color: white !important;
        border: 1px solid #00ffff !important;
    }
    """
) as app:

    gr.Markdown("# 🚀 Nano Banana — AI Pro Prompt Engine")

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

    generate_btn = gr.Button("🚀 Generate Ultra Optimized Prompt")
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
# RUN
# =====================================================

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860
    )
