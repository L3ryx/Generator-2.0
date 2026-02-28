import gradio as gr
import os
import random
import requests

# =====================================================
# 🔐 HUGGING FACE CONFIG (NEW API)
# =====================================================

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/hf-inference/models/distilgpt2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# =====================================================
# 📦 LISTES (Augmentées)
# =====================================================

TOP_LIST = [
    "Oversized T-shirt",
    "Hoodie",
    "Shirt",
    "Crop Top",
    "Blouse",
    "Tank Top",
    "Leather Jacket",
    "Sweater",
    "Bomber Jacket",
    "Corset"
]

BOTTOM_LIST = [
    "Jeans",
    "Cargo Pants",
    "Shorts",
    "Skirt",
    "Leggings",
    "Leather Pants",
    "Wide Pants",
    "Mini Skirt",
    "Baggy Jeans"
]

ENV_LIST = [
    "Urban street",
    "Luxury hotel",
    "City rooftop",
    "Modern apartment",
    "Beach sunset",
    "Pool area",
    "Neon city",
    "Abandoned warehouse",
    "Fashion studio",
    "Paris street"
]

COLOR_LIST = [
    "Neutral tones",
    "Pastel colors",
    "Black & White",
    "Earth tones",
    "Vibrant colors",
    "Dark aesthetic"
]

SHOT_LIST = [
    "Centered composition",
    "Full body",
    "Medium shot",
    "Close up",
    "Low angle cinematic",
    "High angle dramatic"
]

# =====================================================
# 🔄 AUTO FUNCTION
# =====================================================

def auto_choice(list_items):
    return random.choice(list_items)

# =====================================================
# 🤖 GENERATOR USING DISTILGPT2 (NEW API)
# =====================================================

def generate_prompt(
    gender,
    beach_mode,
    top,
    bottom,
    env,
    colors,
    shot
):

    if gender == "Man":
        beach_mode = False

    system_prompt = """
You are an advanced fashion prompt engineer.
Generate a high quality image generation prompt.

Rules:
- Always centered
- Cinematic lighting
- DSLR style
- 50mm lens
- Background blur
- Sunglasses from reference image must be highlighted
- Output in English
- No explanations
"""

    user_prompt = f"""
Gender: {gender}
Beach Mode: {beach_mode}
Top: {top}
Bottom: {bottom}
Environment: {env}
Colors: {colors}
Shot: {shot}
"""

    final_prompt = system_prompt + "\n" + user_prompt

    payload = {
        "inputs": final_prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.8,
            "top_p": 0.9,
            "do_sample": True
        }
    }

    if not HF_TOKEN:
        return "❌ HF_TOKEN not set"

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return f"🔥 HF ERROR:\n{response.text}"

        result = response.json()

        if isinstance(result, list):
            return result[0].get("generated_text", "No output")

        return str(result)

    except Exception as e:
        return f"🔥 REQUEST ERROR:\n{str(e)}"


# =====================================================
# 🔎 TEST TOKEN
# =====================================================

def test_token():
    if not HF_TOKEN:
        return "❌ HF_TOKEN NOT FOUND"
    return "✅ TOKEN DETECTED"


# =====================================================
# 🎨 INTERFACE (WITH DROPDOWNS)
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
        border-radius: 12px;
        font-weight: bold;
    }

    textarea, input, select {
        background-color: #0f172a !important;
        color: white !important;
        border: 1px solid #00ffff !important;
    }
    """
) as app:

    gr.Markdown("# 🚀 Nano Banana — DistilGPT2 Version")

    gender = gr.Radio(["Man", "Woman"], label="Gender")
    beach_mode = gr.Checkbox(label="Beach Mode")

    # ✅ DROPDOWNS (IMPORTANT)
    top = gr.Dropdown(TOP_LIST, label="Top")
    bottom = gr.Dropdown(BOTTOM_LIST, label="Bottom")
    env = gr.Dropdown(ENV_LIST, label="Environment")
    colors = gr.Dropdown(COLOR_LIST, label="Colors")
    shot = gr.Dropdown(SHOT_LIST, label="Camera Shot")

    generate_btn = gr.Button("🚀 Generate Prompt")
    output = gr.Textbox(label="Final Prompt", lines=15)

    test_btn = gr.Button("🧪 Test Token")
    test_output = gr.Textbox(label="Status")

    generate_btn.click(
        generate_prompt,
        inputs=[
            gender,
            beach_mode,
            top,
            bottom,
            env,
            colors,
            shot
        ],
        outputs=output
    )

    test_btn.click(test_token, outputs=test_output)


# =====================================================
# 🚀 RUN SERVER
# =====================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 7860))

    app.launch(
        server_name="0.0.0.0",
        server_port=port
    )
