import gradio as gr
import os
import random
from openai import OpenAI

# ===============================
# API CONFIG
# ===============================

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

print("API KEY LOADED:", API_KEY is not None)

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

    try:

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

        system_prompt = """You are a professional fashion prompt engineer.
Generate a unique high realism prompt.
Always centered.
Always wearing sunglasses from attached image.
Output in English."""

        user_prompt = f"""Gender: {gender}
Beach: {beach_mode}
Top: {top}
Bottom: {bottom}
Environment: {env}
Colors: {colors}
Shot: {shot}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=1.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"ERROR:\n{str(e)}"

# ===============================
# BACKGROUND CSS GENERATOR
# ===============================

def generate_css(https://ibb.co/vCCW9kMJ):
    if background_url:
        return f"""
        body {{
            background-image: url('{background_url}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        """
    return ""

# ===============================
# INTERFACE
# ===============================

with gr.Blocks(title="Nano Banana") as app:

    gr.Markdown("# Nano Banana Prompt Generator")

    background_url = gr.Textbox(
        label="Background Image URL",
        placeholder="Paste your image link here"
    )

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

    generate_btn = gr.Button("Generate Prompt")
    output = gr.Textbox(label="Final Prompt", lines=15)

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

    # Apply dynamic CSS when background changes
    background_url.change(
        fn=generate_css,
        inputs=background_url,
        outputs=None
    )

# ===============================
# RUN SERVER
# ===============================

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860
    )
