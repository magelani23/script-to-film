import os
import json
from typing import List
from google import genai
from google.genai import types
from schemas import SceneCreate

SYSTEM_PROMPT = """
You are an expert film director and AI storyboard artist. 
Your task is to take a raw movie script (which can be in Georgian or any language) and convert it into a structured shot-by-shot visual breakdown for AI video generation.

For each scene:
1. Identify location, time of day, and characters.
2. Break the scene down into sequential camera shots (Shots).
3. Generate highly detailed English image_prompt and video_prompt for each shot to ensure high cinematic visual quality.
4. Output strict JSON matching the schema provided.
"""

def process_script_with_ai(script_text: str) -> List[SceneCreate]:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Analyze and break down the following movie script into structured visual scenes and shots:
    
    SCRIPT:
    {script_text}
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=List[SceneCreate]
        )
    )

    data = json.loads(response.text)
    return [SceneCreate(**scene) for scene in data]

