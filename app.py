import json
import os
import random
import re
import tempfile

import streamlit as st
from google import genai
from google.genai import types
from PIL import Image, ImageColor, ImageDraw, ImageFont


def call_llm(img: Image, prompt: str) -> str:
    system_prompt = """
    Return bounding boxes as a JSON array with labels. Never return masks or code fencing. Limit to 25 objects.
    If an object is present multiple times, name them according to their unique characteristic (colors, size, position, unique characteristics, etc..).
    Output a json list where each entry contains the 2D bounding box in "box_2d" and a text label in "label".
    """

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[prompt, img],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.5,
            safety_settings=[  # https://ai.google.dev/api/generate-content#v1beta.HarmCategory
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_ONLY_HIGH",
                ),
            ],
        ),
    )
    print("Response from LLM", response)
    return response.text


def parse_json(json_input: str) -> str:
    match = re.search(r"```json\n(.*?)```", json_input, re.DOTALL)
    json_input = match.group(1) if match else ""
    return json_input


def get_default_font():
    try:
        # Try to use Arial if available
        return ImageFont.truetype("arial.ttf", size=14)
    except OSError:
        try:
            # Try to use TrueType font on Windows
            return ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", size=14)
        except OSError:
            # Fallback to default bitmap font
            return ImageFont.load_default()


def plot_bounding_boxes(img: Image, bounding_boxes: str) -> Image:
    width, height = img.size
    colors = [colorname for colorname in ImageColor.colormap.keys()]
    draw = ImageDraw.Draw(img)

    bounding_boxes = parse_json(bounding_boxes)

    for bounding_box in json.loads(bounding_boxes):
        color = random.choice(colors)

        # Convert normalized coordinates to absolute coordinates
        abs_y1 = int(bounding_box["box_2d"][0] / 1000 * height)
        abs_x1 = int(bounding_box["box_2d"][1] / 1000 * width)
        abs_y2 = int(bounding_box["box_2d"][2] / 1000 * height)
        abs_x2 = int(bounding_box["box_2d"][3] / 1000 * width)

        if abs_x1 > abs_x2:
            abs_x1, abs_x2 = abs_x2, abs_x1

        if abs_y1 > abs_y2:
            abs_y1, abs_y2 = abs_y2, abs_y1

        print(
            f"Absolute Co-ordinates: {bounding_box['label']}, {abs_y1}, {abs_x1},{abs_y2}, {abs_x2}",
        )

        draw.rectangle(((abs_x1, abs_y1), (abs_x2, abs_y2)), outline=color, width=4)

        # Draw label
        draw.text(
            (abs_x1 + 8, abs_y1 + 6),
            bounding_box["label"],
            fill=color,
            font=get_default_font(),
        )

    return img


if __name__ == "__main__":
    st.set_page_config(page_title="Gemini 2.0 Spatial Demo")
    st.header("⚡️ Gemini 2.0 Spatial Demo")
    
    api_key = st.text_input("Enter your Google API Key (get it from https://aistudio.google.com/app/apikey)", type="password")
    if not api_key:
        st.warning("Please enter your Google API Key to continue")
        st.stop()
    
    os.environ["GOOGLE_API_KEY"] = api_key
    prompt = st.text_input("Enter your prompt")
    run = st.button("Run!")

    with st.sidebar:
        uploaded_image = st.file_uploader(
            accept_multiple_files=False,
            label="Upload your photo here:",
            type=["jpg", "jpeg", "png"],
        )

        if uploaded_image:
            with st.expander("View the image"):
                st.image(uploaded_image)

    if uploaded_image and run and prompt:
        # Process the image directly from the uploaded file
        img = Image.open(uploaded_image)
        width, height = img.size
        resized_image = img.resize(
            (1024, int(1024 * height / width)), Image.Resampling.LANCZOS
        )
        img.close()
        print(
            f"Image Original Size: {img.size} | Resized Image size: {resized_image.size}"
        )

        with st.spinner("Running..."):
            response = call_llm(resized_image, prompt)
            plotted_image = plot_bounding_boxes(resized_image, response)
        st.image(plotted_image)
