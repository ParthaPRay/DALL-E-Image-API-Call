# Partha Pratim Ray
# 6/12/2024
## dall-e-2 call image generation

from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
if load_dotenv():
    print(".env file loaded successfully.")
else:
    print("Failed to load .env file.")

# Retrieve API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
# print(f"API Key Retrieved: {api_key}")  # Debug print

if not api_key:
    raise ValueError("API key not found. Please add it to the .env file.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def generate_and_download_image(prompt, size="1024x1024", n=1, output_folder="generated_content"):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    try:
        print(f"Sending prompt: '{prompt}' to DALL·E model...")  # Debug: Prompt being sent
        print("Processing, please wait...")  # Debug: Indicate processing

        # Generate images
        response = client.images.generate(
            model="dall-e-2",  # Or dall-e-3
            prompt=prompt,
            size=size,
            n=n
        )

        print("Image generated successfully!")  # Debug: Indicate generation success

        # Find the highest current image number in the folder
        existing_files = os.listdir(output_folder)
        image_numbers = [
            int(f.split('_')[1].split('.')[0])
            for f in existing_files if f.startswith('image_') and f.endswith('.png')
        ]
        next_image_number = max(image_numbers, default=0) + 1

        # Save the generated image
        image_url = response.data[0].url  # Get only the first image URL
        image_response = requests.get(image_url)

        if image_response.status_code == 200:
            image_path = os.path.join(output_folder, f"image_{next_image_number}.png")
            with open(image_path, "wb") as file:
                file.write(image_response.content)
            print(f"Image saved: {image_path}")  # Debug: Image saved message
        else:
            print(f"Failed to download image from: {image_url}")

    except Exception as e:
        print(f"An error occurred: {e}")  # Debug: Exception message

# Example usage
generate_and_download_image(prompt="a white Siamese cat", size="1024x1024", n=1)
