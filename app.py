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

        system_prompt = "You generate high realism fashion prompts in English."

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

    except Exception as e:
        return f"🔥 ERROR OCCURRED:\n{str(e)}"
