# Nano Banana Pro MCP Server

An MCP (Model Context Protocol) server that gives Claude Code the ability to generate and edit images using Google's Gemini image models.

## Setup

### 1. Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API Key"
3. Copy the key

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add to Claude Code

**Option A: Using the CLI**

```bash
claude mcp add nano-banana-pro \
  -e GEMINI_API_KEY=your_api_key_here \
  -- python3 /path/to/nano-banana-pro.py
```

**Option B: Manual configuration**

Add to your `~/.claude.json` (or project `.claude.json`):

```json
{
  "mcpServers": {
    "nano-banana-pro": {
      "command": "python3",
      "args": ["/path/to/nano-banana-pro.py"],
      "env": {
        "GEMINI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 4. Verify

Restart Claude Code and check that `nano-banana-pro` appears in your MCP tools. You can test with:

```
Generate an image of a sunset over mountains, photorealistic style
```

## Features

- **generate_image** - Create images from text prompts
- **edit_image** - Edit existing images with text instructions
- **WebP optimization** - Automatic compression (typically 90%+ smaller than PNG)
- **Multiple aspect ratios** - 1:1, 16:9, 9:16, 4:3, 3:4, 21:9
- **Resolution control** - 1K, 2K, or 4K output
- **SEO alt text** - Auto-generates alt text from prompts

## Models

| Name | Model | Best For |
|------|-------|----------|
| `nano-banana-pro` | Gemini 3 Pro Image | Best quality, text in images |
| `nano-banana` | Gemini 2.5 Flash Image | Faster generation |

## Image output

Images are saved to `~/Pictures/nano-banana/` by default. You can override this with the `output_dir` parameter.

## Without this MCP server

The Waboom Landing Page skill works without image generation. It will skip Phase 4 (hero image) if nano-banana-pro is not configured. All text content, research, and SEO/AEO features work independently.
