# Image Generation Guide

## nano-banana-pro Settings

When generating images, use `mcp__nano-banana-pro__generate_image` with these settings:

**ALWAYS specify these parameters:**
- `quality: 95` (prevents pixelation)
- `size: "2K"` for hero images, `"1K"` for thumbnails
- `aspect_ratio: "16:9"` for blog headers, `"1:1"` for social, `"9:16"` for stories

**Note:** If your website uses `unoptimized` on Image components, webp files are served as-is without re-compression.

---

## Text on Images

nano-banana-pro handles text well:
- Include exact text in quotes: `with text "HOT LEAD" on screen`
- Be specific about placement: "on the monitor", "on a sign", "on the shirt"
- After generating, CHECK for strange symbols or garbled text
- If text looks wrong, REGENERATE
- Keep text short (1-3 words works best)

---

## Style Guidelines

- Professional, editorial style
- Dark backgrounds with brand colour accents
- Business/tech aesthetic
- No cheesy stock photo vibes
- Cinematic lighting

---

## Prompts by Content Type

### Blog Headers (16:9)
- Dark backgrounds, moody lighting
- Brand colour accents
- Tech/business aesthetic
- One clear focal point

### Social Posts (1:1 or 4:5)
- Bold, attention-grabbing
- Text overlay friendly (leave space)
- Brand colour highlights

### Ad Creatives
- Problem visualisation OR outcome visualisation
- Clean, not cluttered
- Human element when possible

---

## Example Prompts

**Service Business**: "Futuristic office with holographic AI interfaces, professional setting, one glowing blue AI avatar assisting, dark moody atmosphere, editorial photography"

**Training/Education**: "Modern workshop space with professionals looking at screens showing AI interfaces, collaborative energy, blue accent lighting, corporate photography style"

**Automation**: "Digital transformation visualisation, manual paperwork dissolving into clean digital streams, blue data particles, dark background, cinematic"

**General**: "A modern office transformed with AI. Half the routine tasks automated, holographic dashboards floating above workstations, dramatic blue lighting accents, editorial magazine photography style, cinematic composition, dark moody atmosphere"

---

## VEO 3.1 / Kling Video Prompts

**Required Elements:**
1. **Subject Action** - What the subject physically does (specific, visual)
2. **Camera Movement** - How camera moves through scene
3. **Emotion/Mood/Tone** - How viewer should feel

**Output Format:** One cohesive paragraph merging all three elements. No scene changes, no cuts.

**Example - Service Ad:**
"A business owner sits at a modern desk, overwhelmed with ringing phones. They take a breath, smile, and lean back as holographic AI avatars appear and begin answering the calls. Slow push-in on their relieved expression. Camera subtly rises to reveal multiple AI interfaces handling conversations. Mood: transformation from chaos to calm control. Blue accent lighting, cinematic depth of field, editorial photography style."

**Example - Training Workshop:**
"A diverse group of professionals lean forward engaged around a conference table, laptop screens glowing with AI interfaces. The camera slowly orbits the table, capturing expressions of discovery and understanding. Natural morning light mixed with blue screen glow. Mood: collaborative energy, breakthrough moment, professional excitement."
