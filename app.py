import gradio as gr
import os
import random
import requests
import json

# =====================================================
# 🔐 HUGGING FACE CONFIG
# =====================================================

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/distilgpt2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
} if HF_TOKEN else {}

# =====================================================
# 📦 LISTES
# =====================================================

TOP_LIST = [
    "Oversized T-shirt",
    "Basic Fitted T-shirt",
    "Graphic Street Tee",
    "Vintage Band Tee",
    "Premium Cotton T-shirt",
    "Heavyweight Oversized Hoodie",
    "Zip Hoodie",
    "Minimalist Hoodie",
    "Luxury Embroidered Sweatshirt",
    "Crewneck Sweatshirt",
    "Tank Top",
    "Athletic Tank",
    "Silk Blouse",
    "Satin Blouse",
    "Oversized Shirt",
    "Slim Fit Shirt",
    "Denim Jacket",
    "Leather Jacket",
    "Bomber Jacket",
    "Blazer Jacket",
    "Cardigan",
    "Long Sleeve Shirt",
    "Short Sleeve Shirt",
    "Mesh Fashion Top",
    "Streetwear Pullover",
    "Designer Statement Top"
]
BOTTOM_LIST = [
    "Skinny Jeans",
    "Slim Fit Jeans",
    "Wide Leg Jeans",
    "Baggy Jeans",
    "Cargo Pants",
    "Oversized Cargo Pants",
    "Tailored Pants",
    "Suit Pants",
    "Joggers",
    "Techwear Pants",
    "Track Pants",
    "Shorts",
    "Denim Shorts",
    "Bermuda Shorts",
    "Mini Skirt",
    "Midi Skirt",
    "Maxi Skirt",
    "Leather Pants",
    "High Waist Pants",
    "Straight Leg Pants",
    "Streetwear Cargo Pants",
    "Pleated Trousers",
    "Luxury Fabric Pants"
]

ENV_LIST = [
    "Urban street at golden hour",
    "Luxury hotel lobby",
    "Modern luxury apartment",
    "City rooftop sunset",
    "Beach sunset aesthetic",
    "Private pool villa",
    "Minimalist studio background",
    "Graffiti wall urban setting",
    "Fashion district street",
    "Glass architecture building",
    "Professional fashion studio",
    "Cafe aesthetic interior",
    "Neon city night scene",
    "Private yacht deck",
    "Tropical paradise beach",
    "Luxury shopping mall",
    "Industrial warehouse fashion shoot",
    "Modern office interior",
    "Luxury penthouse terrace",
    "Underground parking cinematic"
]

COLOR_LIST = [
    "Neutral tones",
    "Pastel colors",
    "Black and white style",
    "Earth tone palette"
]

SHOT_LIST = [
    "Centered cinematic composition",
    "Professional fashion full body shot",
    "Medium portrait shot",
    "Close-up portrait",
    "Ultra close-up focusing on sunglasses",
    "Low angle dramatic shot",
    "High angle aesthetic shot",
    "Wide angle fashion shot",
    "Telephoto lens compression effect",
    "Editorial magazine style framing",
    "Luxury brand campaign style shot",
    "Instagram aesthetic composition",
    "Film photography style shot",
    "Studio light professional shot",
    "High fashion runway perspective"
]

# =====================================================
# 🔄 AUTO FUNCTION
# =====================================================

def auto_choice(items):
    return random.choice(items)

# =====================================================
# 🤖 HUGGINGFACE GENERATION
# =====================================================

def generate_with_hf(prompt):

    if not HF_TOKEN:
        return "❌ HF_TOKEN NOT FOUND IN ENV VARIABLES"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.8,
            "top_p": 0.9,
            "do_sample": True
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            return f"🔥 HF API ERROR:\n{response.text}"

        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

        return json.dumps(result, indent=2)

    except Exception as e:
        return f"🔥 REQUEST ERROR:\n{str(e)}"


# =====================================================
# 🚀 MAIN GENERATOR
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

    # 🔥 Rule
    if gender == "Man":
        beach_mode = False

    # Auto logic
    if auto_top_toggle:
        top = auto_choice(TOP_LIST)

    if auto_bottom_toggle:
        bottom = auto_choice(BOTTOM_LIST)

    if auto_env_toggle:
        env = auto_choice(ENV_LIST)

    if auto_color_toggle:
        colors = auto_choice(COLOR_LIST)

    # =====================================================
    # 🧠 SYSTEM PROMPT
    # =====================================================

    system_prompt = """
You are an advanced fashion prompt engine.

Generate ONLY optimized image generation prompts.

Rules:
- Always centered composition
- High realism
- Cinematic lighting
- DSLR camera
- 50mm lens
- Shallow depth of field
- Background blur
- Model wearing sunglasses from attached image
- Sunglasses must be the main visual focus
- Sunglasses must NOT be described as outfit accessory
- 800x1000px
- Output in English
- No explanation
"""

    user_prompt = f"""
Generate professional image prompt.

Gender: {gender}
Beach Mode: {beach_mode}
Top: {top}
Bottom: {bottom}
Environment: {env}
Colors: {colors}
Camera Shot: {shot}

Apply all rules.
Optimize for image generation.
"""

    final_prompt = system_prompt + "\n" + user_prompt

    return generate_with_hf(final_prompt)


# =====================================================
# 🔎 TEST TOKEN
# =====================================================

def test_hf():
    if not HF_TOKEN:
        return "❌ HF TOKEN NOT FOUND"
    return "✅ HF TOKEN DETECTED"


# =====================================================
# 🎨 INTERFACE
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

    gr.Markdown("# 🚀 Nano Banana — Production Version")

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

    generate_btn = gr.Button("🚀 Generate Optimized Prompt")
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
# 🚀 RUN
# =====================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 7860))

    app.launch(
        server_name="0.0.0.0",
        server_port=port
    )
