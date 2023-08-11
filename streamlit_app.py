import streamlit as st
import numpy as np
import random
import sys
from main import main
from PIL import Image, ImageColor, ImageFont, ImageDraw
from PIL.Image import Resampling
from rembg import remove
from io import BytesIO

# Page title
pagetitle = '🏞️ Thumbnail Image Generator'
st.set_page_config(pagetitle)
st.title(pagetitle)
st.info('This app allows you to create a thumbnail image for a YouTube video.')

img_path = 'renders'

# Initialize session state
if 'color1' not in st.session_state:
    st.session_state.color1 = '#06D0DE'
if 'color2' not in st.session_state:
    st.session_state.color2 = '#FE31CD'

# Generate a random HEX color
def generate_random_hex_color():
    # Color 1
    hex1 = '%06x' % random.randint(0, 0xFFFFFF)
    hex1 = '#' + hex1
    rgb_color_1 = ImageColor.getcolor(hex1, 'RGB')
    # Complementary of Color 1
    baseline_color = (255, 255, 255)
    tuple_color = tuple(np.subtract(baseline_color, rgb_color_1))
    hex_color = '#' + rgb_to_hex(tuple_color)
    st.session_state.color1 = hex1
    st.session_state.color2 = hex_color

# Convert RGB to HEX color code
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

# Convert the image to BytesIO so we can download it!
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Sidebar input widgets
with st.sidebar:
    st.header('⚙️ Settings')

    # Color selection
    st.subheader('Wallpaper Color Selection')
    with st.expander('Expand', expanded=True):
        color1 = st.color_picker('Choose the first color', st.session_state.color1, key='color1')
        color2 = st.color_picker('Choose the second color', st.session_state.color2, key='color2')
        st.button('Random complementary colors', on_click=generate_random_hex_color)
    
    # Add title text
    st.subheader('Title Text')
    with st.expander('Expand'):
        st.markdown('### Line 1 Text')
        title_text_1 = st.text_input('Enter text', 'GITHUB')
        title_font_1 = st.slider('Font size', 10, 200, 150, step=10)
        bounding_box_1 = st.checkbox('Black bounding box for text', value=True, key='bounding_box_1')
        left_margin_number_1 = st.number_input('Left margin', 0, 800, 50, step=10, key='left_margin_number_1')
        top_margin_number_1 = st.number_input('Top margin', 0, 800, 340, step=10, key='top_margin_number_1')
        box_width_1 = st.number_input('Box width', 0, 800, 750, step=10, key='box_width_1')
        box_height_1 = st.number_input('Box height', 0, 800, 520, step=10, key='box_height_1')

        st.markdown('### Line 2 Text')
        title_text_2 = st.text_input('Enter text', 'SRIKANTH')
        title_font_2 = st.slider('Font size', 10, 200, 120, step=10)
        bounding_box_2 = st.checkbox('Black bounding box for text', value=True, key='bounding_box_2')
        left_margin_number_2 = st.number_input('Left margin', 0, 800, 50, step=10, key='left_margin_number_2')
        top_margin_number_2 = st.number_input('Top margin', 0, 800, 540, step=10, key='top_margin_number_2')
        box_width_2 = st.number_input('Box width', 0, 1200, 1010, step=10, key='box_width_2')
        box_height_2 = st.number_input('Box height', 0, 800, 700, step=10, key='box_height_2')
        
    # Image upload
    st.subheader('Image upload')
    with st.expander('Expand'):
        image_upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        image_vertical_placement = st.slider('Vertical placement', 0, 1000, 0, step=25)
        image_horizontal_placement = st.slider('Horizontal placement', -1000, 1000, 0, step=25)

    # Add Streamlit logo
    st.subheader('Streamlit logo')
    with st.expander('Expand'):
        streamlit_logo = st.checkbox('Add Streamlit logo', value=True, key='streamlit_logo')
        logo_width = st.slider('Image width', 0, 500, 180, step=10)
        logo_vertical_placement = st.slider('Vertical placement', 0, 1000, 900, step=10)
        logo_horizontal_placement = st.slider('Horizontal placement', 0, 1800, 20, step=10)

# Render wallpaper
col1, col2 = st.columns(2)
with col1:
    st.subheader('Rendered Wallpaper')
    # Generate RGB color code from selected colors
    rgb_color1 = ImageColor.getcolor(color1, 'RGB')
    rgb_color2 = ImageColor.getcolor(color2, 'RGB')
    # Generate wallpaper
    main(rgb_color1, rgb_color2)
    with Image.open(f'{img_path}/wallpaper.png') as img:
        st.image(img)

# Add text to wallpaper
with col2:
    st.subheader('Wallpaper with Text')
    with Image.open(f'{img_path}/wallpaper.png') as img:
        title_font_1 = ImageFont.truetype('font/Montserrat-BlackItalic.ttf', title_font_1)
        title_font_2 = ImageFont.truetype('font/Montserrat-BlackItalic.ttf', title_font_2)

        img_edit = ImageDraw.Draw(img)
        if bounding_box_1:
            #img_edit.rectangle(((50, 340), (750, 520)), fill="black")
            img_edit.rectangle(((left_margin_number_1, top_margin_number_1), (box_width_1, box_height_1)), fill="black")
        if bounding_box_2:
            img_edit.rectangle(((left_margin_number_2, top_margin_number_2), (box_width_2, box_height_2)), fill="black")
        img_edit.text((85,340), title_text_1, (255, 255, 255), font=title_font_1)
        img_edit.text((85,550), title_text_2, (255, 255, 255), font=title_font_2)
        
        if streamlit_logo:
            logo_img = Image.open('streamlit-logo.png').convert('RGBA')
            logo_img.thumbnail([sys.maxsize, logo_width], Resampling.LANCZOS)
            img.paste(logo_img, (logo_horizontal_placement, logo_vertical_placement), logo_img)
            
        img.save(f'{img_path}/thumbnail.png')
        st.image(img)

# Remove background from photo
if image_upload:
    st.subheader('Photo overlayed on Wallpaper')
    image = Image.open(image_upload)
    fixed = remove(image)
    fixed.thumbnail([sys.maxsize, 1080], Resampling.LANCZOS)
    fixed.save(f'{img_path}/photo.png')

    # Overlay photo on wallpaper
    base_img = Image.open(f'{img_path}/thumbnail.png').convert('RGBA')
    photo_img = Image.open(f'{img_path}/photo.png').convert('RGBA')

    base_img.paste(photo_img, (image_horizontal_placement, image_vertical_placement), photo_img)
    base_img.save(f'{img_path}/final.png')

    final_img = Image.open(f'{img_path}/final.png')
    st.image(final_img)

    # Download final thumbnail image
    downloadable_image = convert_image(final_img)
    st.download_button("Download thumbnail image", downloadable_image, "thumbnail_image.png", "image/png")
