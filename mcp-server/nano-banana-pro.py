#!/usr/bin/env python3
"""
Nano Banana Pro MCP Server
--------------------------
An MCP server for generating images using Google's Nano Banana Pro (Gemini 3 Pro Image).

Usage in Claude Code:
  Add to your .claude.json mcpServers or run: /mcp add nano-banana-pro

Environment Variable Required:
  GEMINI_API_KEY - Your Google AI Studio API key from https://aistudio.google.com/apikey

Features:
  - Automatic WebP optimization (typically 90%+ smaller than PNG)
  - Configurable quality settings
  - Support for both generation and editing
"""

import os
import sys
import json
import base64
import asyncio
import io
from pathlib import Path
from datetime import datetime

# Check for required packages
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Installing google-genai package...", file=sys.stderr)
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai", "-q"])
    from google import genai
    from google.genai import types

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow package...", file=sys.stderr)
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
    from PIL import Image

# MCP Protocol imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent, ImageContent
except ImportError:
    print("Installing mcp package...", file=sys.stderr)
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mcp", "-q"])
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent, ImageContent


# Initialize MCP Server
server = Server("nano-banana-pro")

# Default output directory
OUTPUT_DIR = Path.home() / "Pictures" / "nano-banana"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def optimize_to_webp(pil_image, quality: int = 80) -> tuple[bytes, int]:
    """Convert PIL Image to optimized WebP bytes.

    Returns tuple of (webp_bytes, size_in_bytes).
    """
    buffer = io.BytesIO()
    pil_image.save(buffer, format='WEBP', quality=quality, method=6)
    webp_bytes = buffer.getvalue()
    return webp_bytes, len(webp_bytes)


def save_image(pil_image, filepath: Path, img_format: str = "webp", quality: int = 80) -> tuple[Path, int, int]:
    """Save image in specified format with optimization.

    Returns tuple of (final_path, original_size_estimate, final_size).
    """
    # Ensure we have a proper PIL Image (convert if needed)
    if not isinstance(pil_image, Image.Image):
        # If it's bytes or has a read method, open it
        if hasattr(pil_image, 'read'):
            pil_image = Image.open(pil_image)
        elif isinstance(pil_image, bytes):
            pil_image = Image.open(io.BytesIO(pil_image))

    # Convert to RGB if necessary (for WEBP compatibility)
    if pil_image.mode in ('RGBA', 'P'):
        pil_image = pil_image.convert('RGB')

    # Estimate original PNG size
    png_buffer = io.BytesIO()
    pil_image.save(png_buffer, 'PNG')
    original_size = len(png_buffer.getvalue())

    if img_format.lower() == "webp":
        filepath = filepath.with_suffix('.webp')
        webp_buffer = io.BytesIO()
        pil_image.save(webp_buffer, 'WEBP', quality=quality, method=6)
        webp_bytes = webp_buffer.getvalue()
        final_size = len(webp_bytes)
        with open(filepath, 'wb') as f:
            f.write(webp_bytes)
    else:
        filepath = filepath.with_suffix('.png')
        pil_image.save(str(filepath), 'PNG')
        final_size = filepath.stat().st_size

    return filepath, original_size, final_size


def format_size(size_bytes: int) -> str:
    """Format bytes to human readable string."""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f}MB"


def get_client():
    """Get authenticated Gemini client."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable not set. "
            "Get your key from https://aistudio.google.com/apikey"
        )
    return genai.Client(api_key=api_key)


@server.list_tools()
async def list_tools():
    """List available tools."""
    return [
        Tool(
            name="generate_image",
            description="""Generate an image using Nano Banana Pro (Gemini 3 Pro Image).

Best practices for prompts:
- Be specific and detailed about what you want
- Describe style, lighting, mood, composition
- Mention specific art styles if desired (e.g., "photorealistic", "watercolor", "3D render")
- For text in images, put the exact text in quotes
- Nano Banana Pro excels at: text rendering, photorealism, creative compositions

Example prompts:
- "A photorealistic image of a CEO standing at a crossroads, one path labeled 'Innovation' bathed in light, the other labeled 'Status Quo' dark and overgrown. Dramatic lighting, editorial magazine style."
- "Corporate boardroom with a glowing AI hologram in the center, executives looking amazed, cinematic lighting, 16:9"
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Detailed description of the image to generate"
                    },
                    "model": {
                        "type": "string",
                        "enum": ["nano-banana-pro", "nano-banana"],
                        "default": "nano-banana-pro",
                        "description": "Model to use. 'nano-banana-pro' (Gemini 3 Pro) for best quality, 'nano-banana' (Gemini 2.5 Flash) for faster generation"
                    },
                    "aspect_ratio": {
                        "type": "string",
                        "enum": ["1:1", "16:9", "9:16", "4:3", "3:4", "21:9"],
                        "default": "16:9",
                        "description": "Aspect ratio of the generated image"
                    },
                    "size": {
                        "type": "string",
                        "enum": ["1K", "2K", "4K"],
                        "default": "2K",
                        "description": "Image resolution (only for nano-banana-pro)"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Optional filename (without extension). Defaults to timestamp."
                    },
                    "output_dir": {
                        "type": "string",
                        "description": f"Optional output directory. Defaults to {OUTPUT_DIR}"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["webp", "png"],
                        "default": "webp",
                        "description": "Output format. WebP is ~90% smaller than PNG (recommended for web)."
                    },
                    "quality": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100,
                        "default": 80,
                        "description": "WebP quality (1-100). 80 is good balance of quality/size. Only applies to WebP."
                    },
                    "alt_text": {
                        "type": "string",
                        "description": "SEO alt text for the image. If not provided, one will be auto-generated from the prompt."
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="edit_image",
            description="""Edit an existing image using Nano Banana Pro.

Provide a path to an existing image and describe the edits you want to make.

Example edits:
- "Remove the background and replace with a gradient"
- "Add dramatic lighting from the left side"
- "Make it look like a vintage photograph"
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the image to edit"
                    },
                    "edit_prompt": {
                        "type": "string",
                        "description": "Description of the edits to make"
                    },
                    "model": {
                        "type": "string",
                        "enum": ["nano-banana-pro", "nano-banana"],
                        "default": "nano-banana-pro"
                    },
                    "output_dir": {
                        "type": "string",
                        "description": f"Optional output directory. Defaults to {OUTPUT_DIR}"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["webp", "png"],
                        "default": "webp",
                        "description": "Output format. WebP is ~90% smaller than PNG."
                    },
                    "quality": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100,
                        "default": 80,
                        "description": "WebP quality (1-100). Only applies to WebP."
                    },
                    "alt_text": {
                        "type": "string",
                        "description": "SEO alt text for the edited image."
                    }
                },
                "required": ["image_path", "edit_prompt"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls."""

    if name == "generate_image":
        return await generate_image(arguments)
    elif name == "edit_image":
        return await edit_image(arguments)
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


def generate_alt_text(prompt: str) -> str:
    """Generate SEO-friendly alt text from the prompt.

    Strips style/technical instructions and keeps descriptive content.
    """
    # Remove common style instructions
    skip_phrases = [
        "photorealistic", "cinematic lighting", "dramatic lighting",
        "editorial", "magazine style", "16:9", "9:16", "4:3", "1:1",
        "high quality", "detailed", "professional", "4K", "2K", "1K"
    ]
    alt = prompt
    for phrase in skip_phrases:
        alt = alt.replace(phrase, "").replace(phrase.lower(), "")

    # Clean up and truncate
    alt = " ".join(alt.split())  # Normalize whitespace
    alt = alt.strip(" .,;:-")

    # Truncate to ~125 chars for SEO best practice
    if len(alt) > 125:
        alt = alt[:122].rsplit(" ", 1)[0] + "..."

    return alt


async def generate_image(args: dict):
    """Generate an image from a text prompt with WebP optimization."""
    try:
        client = get_client()

        prompt = args["prompt"]
        model_choice = args.get("model", "nano-banana-pro")
        aspect_ratio = args.get("aspect_ratio", "16:9")
        size = args.get("size", "2K")
        filename = args.get("filename", datetime.now().strftime("%Y%m%d_%H%M%S"))
        output_dir = Path(args.get("output_dir", OUTPUT_DIR))
        output_format = args.get("format", "webp")
        quality = args.get("quality", 80)
        alt_text = args.get("alt_text") or generate_alt_text(prompt)

        # Map model names - using current Gemini image generation models
        model_map = {
            "nano-banana-pro": "gemini-3-pro-image-preview",
            "nano-banana": "gemini-2.5-flash-image"
        }
        model = model_map.get(model_choice, "gemini-3-pro-image-preview")

        # Build config - note: aspect_ratio not supported on gemini-2.0-flash-exp
        # Include aspect ratio in prompt instead
        aspect_prompt = f" The image should be in {aspect_ratio} aspect ratio format."
        full_prompt = prompt + aspect_prompt

        config = types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )

        # Generate
        response = client.models.generate_content(
            model=model,
            contents=full_prompt,
            config=config
        )

        # Process response
        output_dir.mkdir(parents=True, exist_ok=True)
        saved_files = []
        size_info = []
        text_response = ""

        for part in response.parts:
            if hasattr(part, 'text') and part.text:
                text_response += part.text + "\n"
            elif hasattr(part, 'inline_data') and part.inline_data:
                # Get image data and convert to PIL Image
                image_data = part.inline_data.data
                pil_image = Image.open(io.BytesIO(image_data))

                # Build filepath (without extension - save_image will add it)
                base_filepath = output_dir / filename
                # Handle duplicate names
                counter = 1
                test_path = base_filepath.with_suffix(f'.{output_format}')
                while test_path.exists():
                    base_filepath = output_dir / f"{filename}_{counter}"
                    test_path = base_filepath.with_suffix(f'.{output_format}')
                    counter += 1

                # Save with optimization
                final_path, orig_size, final_size = save_image(
                    pil_image, base_filepath, output_format, quality
                )
                saved_files.append(str(final_path))

                # Calculate savings
                if output_format == "webp":
                    savings_pct = ((orig_size - final_size) / orig_size) * 100
                    size_info.append(f"{format_size(orig_size)} -> {format_size(final_size)} ({savings_pct:.0f}% smaller)")

        # Build result message
        result = f"Generated image saved to: {', '.join(saved_files)}\n"
        if size_info:
            result += f"Size optimization: {', '.join(size_info)}\n"
        result += f"Alt text (SEO): \"{alt_text}\"\n"
        if text_response:
            result += f"\nModel notes: {text_response}"

        return [TextContent(type="text", text=result)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error generating image: {str(e)}")]


async def edit_image(args: dict):
    """Edit an existing image with WebP optimization."""
    try:
        client = get_client()

        image_path = args["image_path"]
        edit_prompt = args["edit_prompt"]
        model_choice = args.get("model", "nano-banana-pro")
        output_dir = Path(args.get("output_dir", OUTPUT_DIR))
        output_format = args.get("format", "webp")
        quality = args.get("quality", 80)
        alt_text = args.get("alt_text") or generate_alt_text(edit_prompt)

        # Load image
        if not Path(image_path).exists():
            return [TextContent(type="text", text=f"Image not found: {image_path}")]

        image = Image.open(image_path)

        # Map model names
        model_map = {
            "nano-banana-pro": "gemini-3-pro-image-preview",
            "nano-banana": "gemini-2.5-flash-image"
        }
        model = model_map.get(model_choice, "gemini-3-pro-image-preview")

        config = types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )

        # Generate edit
        response = client.models.generate_content(
            model=model,
            contents=[edit_prompt, image],
            config=config
        )

        # Process response
        output_dir.mkdir(parents=True, exist_ok=True)
        saved_files = []
        size_info = []
        text_response = ""
        filename = f"edited_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        for part in response.parts:
            if hasattr(part, 'text') and part.text:
                text_response += part.text + "\n"
            elif hasattr(part, 'inline_data') and part.inline_data:
                # Get image data and convert to PIL Image
                image_data = part.inline_data.data
                pil_image = Image.open(io.BytesIO(image_data))
                base_filepath = output_dir / filename

                # Save with optimization
                final_path, orig_size, final_size = save_image(
                    pil_image, base_filepath, output_format, quality
                )
                saved_files.append(str(final_path))

                # Calculate savings
                if output_format == "webp":
                    savings_pct = ((orig_size - final_size) / orig_size) * 100
                    size_info.append(f"{format_size(orig_size)} -> {format_size(final_size)} ({savings_pct:.0f}% smaller)")

        # Build result message
        result = f"Edited image saved to: {', '.join(saved_files)}\n"
        if size_info:
            result += f"Size optimization: {', '.join(size_info)}\n"
        result += f"Alt text (SEO): \"{alt_text}\"\n"
        if text_response:
            result += f"\nModel notes: {text_response}"

        return [TextContent(type="text", text=result)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error editing image: {str(e)}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
