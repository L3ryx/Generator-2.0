import gradio as gr
import os
import random
from huggingface_hub import InferenceClient

# =====================================================
# 🔐 HUGGING FACE CONFIG (NEW ROUTER API)
# =====================================================

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    model="distilgpt2",
    token=HF_TOKEN
)

# =====================================================
# 📦 LISTES (PLUS COMPLETES)
# =====================================================

TOP_LIST = [
    "Oversized T-shirt",
    "Hoodie",
    "Graphic Tee",
    "Tank Top",
    "Leather Jacket",
    "Crop Top",
    "Sweatshirt",
    "Denim Jacket",
    "Blazer",
    "Corset"
]

BOTTOM_LIST = [
    "Jeans",
    "Cargo Pants",
    "Shorts",
    "Mini Skirt",
    "Long Skirt",
    "Leggings",
    "Wide Pants",
    "Leather Pants",
    "Joggers",
    "Tailored Pants"
]

ENV_LIST = [
    "Urban Street",
    "Luxury Hotel",
    "Beach Sunset",
    "Private Pool",
    "Modern Apartment",
    "City Rooftop",
    "Fashion Studio",
    "Neon City",
    "Car Parking Scene",
    "Tropical Paradise"
]

COLOR_LIST = [
    "Neutral Tone",
    "Black & White",
    "Pastel Colors",
    "Earth Tone",
    "Neon Style",
    "Dark Elegant",
    "Luxury Gold",
    "Minimal Clean"
]

SHOT_LIST = [
    "Centered Composition",
    "Full Body Shot",
    "Medium Shot",
    "Close Up",
    "Low Angle",
    "High Angle",
    "Portrait Style",
    "Wide Angle Cinematic"
]

# =====================================================
# 🤖 PROMPT GENERATOR (USING HUGGINGFACE ROUTER)
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

    if not HF_TOKEN:
        return "❌ HF_TOKEN NOT CONFIGURED"

    if gender == "Man":
        beach_mode = False

    system_prompt = """
You are an advanced fashion AI prompt engine.

Generate ONLY optimized image generation prompts.

Rules:
- Cinematic lighting
- DSLR camera
- 50mm lens
- Centered
- Background blur
- Sunglasses must be highlighted
- 800x1000 resolution
- Output in English
- No explanation
"""

    user_prompt = f"""
Gender: {gender}
Beach Mode: {beach_mode}
Top: {top}
Bottom: {bottom}
Environment: {env}
Colors: {colors}
Camera Shot: {shot}
"""

    final_prompt = system_prompt + "\n" + user_prompt

    try:
        response = client.text_generation(
            final_prompt,
            max_new_tokens=300,
            temperature=0.9,
            top_p=0.95
        )

        return response

    except Exception as e:
        return f"🔥 HF API ERROR:\n{str(e)}"


# =====================================================
# 🔎 TOKEN TEST
# =====================================================

def test_token():
    if HF_TOKEN:
        return "✅ HF TOKEN DETECTED"
    return "❌ HF TOKEN NOT FOUND"


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

    gr.Markdown("# 🚀 Nano Banana — Prompt Generator")

    gender = gr.Radio(["Man", "Woman"], label="Gender")
    beach_mode = gr.Checkbox(label="Beach Mode")

    # ✅ DROPDOWNS POUR TOUS LES PARAMÈTRES
    top = gr.Dropdown(TOP_LIST, label="Top Selection")
    bottom = gr.Dropdown(BOTTOM_LIST, label="Bottom Selection")
    env = gr.Dropdown(ENV_LIST, label="Environment")
    colors = gr.Dropdown(COLOR_LIST, label="Colors")
    shot = gr.Dropdown(SHOT_LIST, label="Camera Shot")

    generate_btn = gr.Button("🚀 Generate Optimized Prompt")
    output = gr.Textbox(label="Final Prompt", lines=15)

    test_btn = gr.Button("🧪 Test HF Token")
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
# 🚀 RUN (RENDER COMPATIBLE)
# =====================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 7860))

    app.launch(
        server_name="0.0.0.0",
        server_port=port
    )
