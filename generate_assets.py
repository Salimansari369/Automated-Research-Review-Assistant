import base64
import os

def to_b64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

assets = {
    "HERO_ANIME_IMG": to_b64("static/images/hero_anime_space.png"),
    "SIDEBAR_ASTRONAUT_IMG": to_b64("static/images/sidebar_astronaut.png"),
    "CHIBI_READING_IMG": to_b64("static/images/chibi_reading.png"),
    "CHIBI_COOL_IMG": to_b64("static/images/chibi_cool.png"),
    "CHIBI_GAPS_IMG": to_b64("static/images/chibi_gaps.png"),
    "CHIBI_REVIEW_IMG": to_b64("static/images/chibi_review.png"),
    "GAP_BOY_IMG": to_b64("static/images/gap_anime_boy.png"),
    "INSIGHT_GIRL_IMG": to_b64("static/images/insight_anime_girl.png"),
    "USER_AVATAR_IMG": to_b64("static/images/user_avatar.png"),
}

with open("ui/assets.py", "w", encoding="utf-8") as f:
    f.write('"""Exact original reference anime assets stored as high-fidelity data-URIs."""\n\n')
    for k, v in assets.items():
        f.write(f'{k} = "{v}"\n\n')

    sparkline_func = '''def generate_sparkline_svg(color="#6366f1", points="5,20 25,18 45,22 65,12 85,15 105,8 125,10"):
    return f"""
    <svg viewBox="0 0 130 30" width="100%" height="24" xmlns="http://www.w3.org/2000/svg">
      <polyline fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" points="{points}" />
    </svg>
    """
'''
    f.write(sparkline_func)

print("ui/assets.py generated with exact reference character assets successfully!")
