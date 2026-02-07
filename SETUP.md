# Setup Guide

Detailed instructions for installing and customising the Waboom Landing Page skill.

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- Optional: Python 3.10+ (only needed for image generation)
- Optional: A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey) (free tier available)

## Step 1: Install the Skill

Copy the `skill/` directory to your Claude Code skills folder:

```bash
cp -r skill/ ~/.claude/skills/waboom-landing-page/
```

Verify it's installed:

```bash
ls ~/.claude/skills/waboom-landing-page/
# Should show: SKILL.md, knowledge-base.md, content-templates.md, etc.
```

## Step 2: Run Onboarding

Open Claude Code and say:

```
Waboom setup
```

The skill will ask you 10 questions about your business:

1. **Company name** and tagline
2. **What do you sell?** Products/services with brief descriptions
3. **Key stats** - Customers served, success rates, years in business, any impressive numbers
4. **Target market** - Geography, industries, company size, ideal customer
5. **Brand voice** - Formal, casual, or edgy? Any specific tone you admire?
6. **Brand colour** - Hex code for your primary brand colour (e.g., `#198FFF`)
7. **Competitors** - Who do you compete with? What makes you different?
8. **Testimonial patterns** - Real client quotes or result patterns
9. **Pricing** - If public, include tier names and prices
10. **Website URL** - For internal linking in generated content

After answering, the skill generates your personalised `knowledge-base.md`. Every piece of content will reference your real business data.

## Step 3: Test It

Generate your first landing page:

```
Waboom landing page for [your industry]
```

Claude will:
1. Search Google for industry-specific pain points and statistics
2. Write a complete landing page using your business details
3. Optimise for SEO and AEO with metadata and JSON-LD schema
4. Generate a hero image (if nano-banana-pro is configured)

## Step 4: Image Generation (Optional)

If you want the skill to generate hero images:

### Get a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### Install the MCP Server

```bash
# Install Python dependencies
pip install -r mcp-server/requirements.txt

# Add to Claude Code
claude mcp add nano-banana-pro \
  -e GEMINI_API_KEY=your_key_here \
  -- python3 /absolute/path/to/mcp-server/nano-banana-pro.py
```

Restart Claude Code. The skill will now generate images in Phase 4.

## Customisation

### Changing the Voice

Edit `skill/SKILL.md` — the "VOICE & STYLE GUIDE" section controls tone:

- **Direct** - No corporate fluff
- **Edgy** - Willing to call out BS
- **Value-First** - Lead with insight, not pitch
- **Data-Driven** - Use numbers, always

To make it more formal, soften the "Edgy" and "Slightly Aggressive" guidelines. To make it more casual, lean into the conversational patterns.

### Adding Content Templates

Edit `skill/content-templates.md` to add your own templates:

- Blog post structures
- Social media formats
- Email sequences
- Video script frameworks

### Updating Your Business Data

Edit `skill/knowledge-base.md` directly, or run `Waboom setup` again to regenerate it.

### Customising SEO/AEO

Edit `skill/seo-aeo-checklist.md` to adjust:

- JSON-LD schema templates
- Keyword placement rules
- Meta description patterns

## Tips for Best Results

1. **Be specific with industries** - "Waboom landing page for residential plumbers in Auckland" works better than "Waboom landing page for plumbers"
2. **Let it research** - The skill searches Google for real data. Don't skip this phase.
3. **Review the FAQ** - The researched FAQ section is gold for AEO. AI answer engines love well-structured FAQ content.
4. **Use the headlines command** - "Waboom headlines for [topic]" generates 5-7 variants with different psychological hooks. Pick the best one.
5. **Check generated images** - AI image generation sometimes produces text artefacts. Regenerate if the text on images looks wrong.

## Troubleshooting

**Skill not found?**
Make sure the directory is named exactly `waboom-landing-page` and contains `SKILL.md` (not `skill.md`).

**No web search results?**
The skill needs the `WebSearch` and `WebFetch` tools. These are available in Claude Code by default.

**Image generation failing?**
Check that your `GEMINI_API_KEY` environment variable is set correctly and the MCP server is running. See `mcp-server/README.md` for detailed troubleshooting.

**Content doesn't match my brand?**
Run `Waboom setup` again to update your `knowledge-base.md`. The more detailed your answers, the more personalised the output.
