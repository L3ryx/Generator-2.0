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
# LISTES
# ===============================

TOP_LIST = ["Oversized T-shirt", "Hoodie", "Shirt", "Crop Top", "Blouse"]
BOTTOM_LIST = ["Jeans", "Cargo Pants", "Shorts", "Skirt", "Leggings"]
ENV_LIST = ["Urban Lifestyle", "Luxury Hotel", "City Street", "Modern Apartment"]
COLOR_LIST = ["Neutral Colors", "Pastel Colors", "Black & White", "Earth Tone"]
SHOT_LIST = ["Close-up", "Medium Shot", "Full Body", "Low Angle", "High Angle"]

# ===============================
# AUTO FUNCTIONS
# ===============================

def auto_top(): return random.choice(TOP_LIST)
def auto_bottom(): return random.choice(BOTTOM_LIST)
def auto_env(beach_mode):
    if beach_mode:
        return random.choice(["Beach", "Pool Area"])
    return random.choice(ENV_LIST)
def auto_colors(): return random.choice(COLOR_LIST)

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

    if gender == "Man":
        beach_mode = False

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
Always centered.
Always wearing sunglasses from attached image.
Output in English.
"""

    user_prompt = f"""
Gender: {gender}
Beach: {beach_mode}
Top: {top}
Bottom: {bottom}
Environment: {env}
Colors: {colors}
Shot: {shot}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=1.4
    )

    return response.choices[0].message.content


# ===============================
# TEST API
# ===============================

def test_api():
    try:
        client.models.list()
        return "✅ API Connected"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ===============================
# INTERFACE (CHANGE ONLY IMAGE LINK BELOW)
# ===============================

with gr.Blocks(
    title="Nano Banana",
    css="""
    /* 🔥 CHANGE ONLY THIS IMAGE LINK */
    body {
        background: url('https://drive.google.com/file/d/1HD4qAQRb_Lzp0Ilg8vU7U1qMH0sRv_zK/view?usp=drivesdk');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
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

    .block {
        background-color: rgba(15, 23, 42, 0.85) !important;
        border-radius: 20px !important;
        padding: 25px;
        box-shadow: 0 0 25px #00ffff;
    }

    textarea, input, select {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #00ffff !important;
        box-shadow: 0 0 10px #00ffff;
    }
    """
) as app:

    gr.Markdown("# 🚀 Nano Banana Prompt Optimizer")

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

    test_btn = gr.Button("🧪 Test API")
    test_output = gr.Textbox(label="API Status")

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

    test_btn.click(test_api, inputs=[], outputs=test_output)

# ===============================
# RUN
# ===============================

app.launch(server_name="0.0.0.0", server_port=7860)
