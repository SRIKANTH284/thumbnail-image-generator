# 🏞️ Thumbnail Image Generator

This app allows you to create thumbnail images for YouTube videos.

## App screenshot



## How the app works?

**Input:**
- User selects 2 colors they like (or randomly select complementary colors, blue + orange, green + red)
- Enter title text to display on thumbnail image
- Option to add logo
- Upload photo
  
**App:**
- Generates a wallpaper based on user-selected colors
- Add text + bounding box to thumbnail image
- If user upload their photo, overlays the photo on top of the wallpaper

**Output:**
- Finally, the generated thumbnail image can be downloaded

## Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://srikanththumbnailimage.streamlit.app/)

## Resources and Libraries used
- Wallpaper generation was performed using the 
- Python libraries used: `PIL`, `subprocess`, `math`, `os`, `random`, `rembg`, `sys` and `streamlit`.
