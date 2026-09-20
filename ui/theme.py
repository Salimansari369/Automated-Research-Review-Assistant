import gradio as gr

def get_literature_theme() -> gr.Theme:
    """Returns a customized Gradio theme aligned with the dark cyber-space futuristic design."""
    theme = gr.themes.Soft(
        primary_hue=gr.themes.colors.indigo,
        secondary_hue=gr.themes.colors.purple,
        neutral_hue=gr.themes.colors.slate,
        font=[
            gr.themes.GoogleFont("Plus Jakarta Sans"),
            gr.themes.GoogleFont("Inter")
        ]
    ).set(
        body_background_fill="#060814",
        body_background_fill_dark="#060814",
        block_background_fill="#0d1126",
        block_background_fill_dark="#0d1126",
        block_border_width="1px",
        block_border_color="#1e2548",
        block_shadow="none",
        block_label_background_fill="transparent",
        block_label_border_width="0px",
        block_label_border_color="transparent",
        button_primary_background_fill="linear-gradient(135deg, #6366f1, #8b5cf6)",
        button_primary_background_fill_hover="linear-gradient(135deg, #4f46e5, #7c3aed)",
        button_primary_text_color="#ffffff",
        input_background_fill="#0b0e23",
        input_border_color="#1e2548",
        input_border_color_focus="#818cf8",
        input_shadow="none"
    )
    return theme

