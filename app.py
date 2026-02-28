import gradio as gr
import os
import random
from openai import OpenAI

# ===============================
# API CONFIG
# ===============================

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# ===============================
# LISTES INTELLIGENTES
# ===============================

TOP_LIST = [
    "Oversized T-shirt",
    "Hoodie",
    "Shirt",
    "Crop Top",
    "Blouse",
    "Corset",
    "Sweater",
    "Tank Top"
]

BOTTOM_LIST = [
    "Jeans",
    "Cargo Pants",
    "Shorts",
    "Skirt",
    "Leggings",
    "Flare Pants"
]

ENV_LIST = [
    "Urban Lifestyle",
    "Luxury Hotel",
    "City Street",
    "Modern Apartment",
    "Graffiti Wall"
]

COLOR_LIST = [
    "Neutral Colors",
    "Pastel Colors",
    "Black & White",
    "Earth Tone",
    "Bold Colors",
    "Luxury Gold Style"
]

SHOT_LIST = [
    "Close-up",
    "Medium Shot",
    "Full Body",
    "Low Angle",
    "High Angle"
]

# ===============================
# AUTO FUNCTIONS
# ===============================

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

# ===============================
# PROMPT GENERATOR
# ===============================

def generate_prompt(gender,
                    beach_mode,
                    auto_top_toggle,
                    auto_bottom_toggle,
                    auto_env_toggle,
                    auto_color_toggle,
                    top,
                    bottom,
                    env,
                    colors,
                    shot):

    # 🔴 Auto disable beach if man
    if gender == "Man":
        beach_mode = False

    # 🔥 AUTO SYSTEM PER PARAMETER
    if auto_top_toggle:
        top = auto_top()

    if auto_bottom_toggle:
        bottom = auto_bottom()

    if auto_env_toggle:
        env = auto_env(beach_mode)

    if auto_color_toggle:
        colors = auto_colors()

    system_prompt = """
You are a professional fashion prompt engineer.

Generate a unique high realism prompt.

Rules:
- 800x1000px
- DSLR camera
- 50mm lens
- Cinematic lighting
- Always perfectly centered
- Always wearing sunglasses from attached image
- Sunglasses must be main focal point
- Environment must match lifestyle
- Output in English only
"""

    user_prompt = f"""
Gender: {gender}
Beach Mode: {beach_mode}

Top: {top}
Bottom: {bottom}
Environment: {env}
Colors: {colors}
Camera Shot: {shot}

Create a unique optimized variation for Nano Banana.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=1.4,
        top_p=0.95
    )

    return response.choices[0].message.content


# ===============================
# TEST API
# ===============================

def test_api():
    try:
        client.models.list()
        return "✅ API Connected Successfully"
    except Exception as e:
        return f"❌ API Error: {str(e)}"


# ===============================
# INTERFACE
# ===============================

with gr.Blocks(title="Nano Banana Advanced") as app:

    gr.Markdown("# 🚀 Nano Banana Prompt Optimizer")

    gender = gr.Radio(["Man", "Woman"], label="Gender")

    beach_mode = gr.Checkbox(label="Beach Mode")

    # Auto toggles
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

    test_btn = gr.Button("🧪 Test API Connection")
    test_output = gr.Textbox(label="API Status")

    # ===============================
    # BUTTON LOGIC
    # ===============================

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

    test_btn.click(
        test_api,
        inputs=[],
        outputs=test_output
    )

# ===============================
# RUN SERVER
# ===============================

app.launch(server_name="0.0.0.0", server_port=7860)
