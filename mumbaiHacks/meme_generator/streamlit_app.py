import streamlit as st
import requests
import os
from PIL import Image, ImageDraw, ImageFont
import random
import matplotlib.pyplot as plt
import urllib.parse
import time

# Predefined meme captions and keywords
meme_captions = [
    "When you realize it's Monday tomorrow!",
    "That feeling when you finish your project.",
    "Trying to adult like...",
    "When your friend says they don't like pizza.",
    "Me trying to be productive...",
    # (more captions)
]

# List of keywords for suggestion
keywords = [
    "dog", "cat", "study", "work", "school", "food", "weekend", "exam", "nap", "movie",
    # (more keywords)
]

# To keep track of how many times each trending topic has been suggested
trending_count = {}

# Function to suggest meme text based on a keyword or randomly
def suggest_meme_text_based_on_keyword(keyword, trending_topics):
    global trending_count
    # (same as your original function)
    return random.choice(meme_captions)

# Meme creation function
def create_meme(image_path, top_text, bottom_text, font_path, font_size, text_color):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    
    top_text_position = (50, 10)
    bottom_text_position = (50, image.height - 100)
    outline_color = "black"

    def draw_text_with_outline(position, text, font, fill, outline):
        x, y = position
        for adj in [-1, 0, 1]:
            draw.text((x + adj, y), text, font=font, fill=outline)
            draw.text((x, y + adj), text, font=font, fill=outline)
        draw.text(position, text, font=font, fill=fill)

    draw_text_with_outline(top_text_position, top_text, font, text_color, outline_color)
    draw_text_with_outline(bottom_text_position, bottom_text, font, text_color, outline_color)

    return image

# (other existing functions unchanged)

# Title for the Streamlit app
st.title("Meme Generator and Trend Helper")

# Fetch trending topics from Django API
try:
    response = requests.get("http://127.0.0.1:8000/trending/")
    if response.status_code == 200:
        trending_topics = response.json().get("trending_topics", [])
        st.write("**Trending Topics:**")
        for topic in trending_topics:
            st.write(f"- {topic}")
            # Initialize the count for each trending topic
            trending_count[topic] = 0
    else:
        st.write("Could not fetch trending topics.")
except requests.exceptions.RequestException as e:
    st.write("Error:", e)
    trending_topics = []

# Create a bar graph for trending topic analysis
if trending_count:
    st.subheader("Trending Topic Analysis")
    
    # Sort the trending topics based on selection counts
    sorted_trends = sorted(trending_count.items(), key=lambda item: item[1], reverse=True)
    topics, counts = zip(*sorted_trends)

    fig, ax = plt.subplots(figsize=(10, 6))  # Increase figure size for better readability
    ax.barh(topics, counts, color='skyblue')  # Horizontal bar graph for better label readability
    ax.set_xlabel("Selection Count", fontsize=12)
    ax.set_ylabel("Trending Topics", fontsize=12)
    ax.set_title("Trending Topics vs. Selection Count", fontsize=14)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    ax.grid(axis='x', linestyle='--', alpha=0.7)  # Add gridlines for better visualization
    st.pyplot(fig)



# Streamlit app layout
meme_template_dir = 'memes/media/memes/'  # Adjust the path accordingly
meme_templates = os.listdir(meme_template_dir)

selected_template = st.selectbox("Select a Meme Template", meme_templates)
top_text = st.text_input("Top Text")
bottom_text = st.text_input("Bottom Text")

# New customization options
font_choices = ["arial.ttf", "cour.ttf", "times.ttf"]  # Add paths to available fonts
selected_font = st.selectbox("Select Font", font_choices)
font_size = st.slider("Select Font Size", min_value=10, max_value=150, value=100)
text_color = st.color_picker("Pick a Text Color", "#FFFFFF")  # Default white color

if st.button("Create Meme"):
    if selected_template:
        meme_path = os.path.join(meme_template_dir, selected_template)
        meme_image = create_meme(meme_path, top_text, bottom_text, selected_font, font_size, text_color)
        output_path = "memes/media/memes/created_meme.png"
        meme_image.save(output_path)
        st.image(meme_image, caption="Your Meme", use_column_width=True)

        # Download button for the created meme
        with open(output_path, "rb") as f:
            st.download_button("Download Meme", f, "created_meme.png")
        
        # Social media share buttons
        # (same code for sharing as before)

# Image upload and text suggestion
uploaded_image = st.file_uploader("Upload an image for text suggestion", type=["jpg", "png"])
if uploaded_image:
    img_path = f"uploaded_{uploaded_image.name}"
    with open(img_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
    st.image(img_path, caption="Uploaded Image", use_column_width=True)

    # Ask user for a keyword
    keyword = st.text_input("Enter a keyword for meme suggestion")

    if st.button("Suggest Meme Text"):
        suggested_text = suggest_meme_text_based_on_keyword(keyword, trending_topics)
        st.write("Suggested Meme Text:", suggested_text)

        # Create a meme with the suggested text
        with st.spinner("Generating suggested meme..."):
            time.sleep(1)  # Simulate time taken for processing
            meme_image = create_meme(img_path, suggested_text, "", selected_font, font_size, text_color)
            output_path = "memes/media/memes/suggested_meme.png"
            meme_image.save(output_path)
            st.image(meme_image, caption="Meme with Suggested Text", use_column_width=True)

            # Download button for the suggested meme
            with open(output_path, "rb") as f:
                st.download_button("Download Suggested Meme", f, "suggested_meme.png")
