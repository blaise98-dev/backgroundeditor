import streamlit as st
from rembg import remove
from PIL import Image
import io
import base64
import zipfile
def remove_background(input_image):
    try:
        # Remove background
        output_image = remove(input_image)
        return output_image
    except Exception as e:
        st.error(f"Error occurred while processing image: {e}")
        return None

def apply_background(image, background_option, background_image=None, background_color=None):
    if background_option == "custom_background":
        if background_image is not None:
            background = Image.open(background_image)
        else:
            st.error("Please upload a background image")
            return None
    elif background_option == "background_color_editor":
        # Apply selected background color
        background = Image.new("RGB", image.size, background_color)
        pass
    else:
        st.error("Invalid background option")
        return None
    
    # Resize background image to match the size of the input image
    background = background.resize(image.size)
    
    # Composite the input image with the selected background
    composite_image = Image.alpha_composite(background.convert("RGBA"), image.convert("RGBA"))
    return composite_image

st.title('Background Editor App')

# Upload multiple images
uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

background_options = ["custom_background", "background_color_editor"]
selected_background = st.selectbox("Select background option", background_options)

background_image = None
background_color = None

if selected_background == "custom_background":
    background_image = st.file_uploader("Upload a background image", type=["jpg", "jpeg", "png"])
elif selected_background == "background_color_editor":
    background_color = st.color_picker("Choose background color", "#FFFFFF")  # Default color is white

processed_images = []

if uploaded_files:
    for idx, uploaded_file in enumerate(uploaded_files):
        try:
            # Display uploaded image
            input_image = Image.open(uploaded_file)
            st.image(input_image, caption=f'Uploaded Image {idx+1}', use_column_width=True)

            # Perform background removal
            output_image = remove_background(input_image)

            if output_image:
                # # Display image without background
                # st.image(output_image, caption='Image with Removed Background', use_column_width=True)
                
                # Apply selected background
                background_applied_image = apply_background(output_image, selected_background, background_image, background_color)
                
                if background_applied_image:
                    # Display image with selected background
                    st.image(background_applied_image, use_column_width=True)
                    
                    # With caption
                    #  st.image(background_applied_image, caption=f'Image with {selected_background} Background', use_column_width=True)
                    
                    # Append processed image to the list
                    processed_images.append(background_applied_image)

        except Exception as e:
            st.error(f"Error occurred while processing image {idx+1}: {e}")

# Generate download link(s) for processed images
if processed_images:
    for i, image in enumerate(processed_images):
        image_name = f"processed_image_{i+1}.png"
        output_buffer = io.BytesIO()
        # Save processed image with a default quality value
        image.save(output_buffer, format='PNG', quality=95)
        b64_image = base64.b64encode(output_buffer.getvalue()).decode()
        download_link = f'<a href="data:application/octet-stream;base64,{b64_image}" download="{image_name}">Download {image_name}</a>'
        st.markdown(download_link, unsafe_allow_html=True)
else:
    st.warning("No images processed.")