# SEO/AEO Optimisation Checklist

Apply this checklist after writing any landing page or content piece.

---

## SEO Checklist

- [ ] **Page title**: [Industry] + [Service] + [Brand] (under 60 characters)
- [ ] **Meta description**: Benefit-focused, includes primary keyword (under 160 characters)
- [ ] **H1** contains primary keyword
- [ ] **H2s** contain secondary keywords
- [ ] **Primary keyword** appears in first 100 words
- [ ] **Internal links** to 2-3 related pages on the site
- [ ] **Canonical URL** set correctly
- [ ] **OG image** created (1200x630px) with title text
- [ ] **Alt text** on all images (descriptive, keyword-rich)
- [ ] **URL slug** is short, keyword-rich, lowercase with hyphens

---

## AEO Checklist (Answer Engine Optimisation)

AEO optimises content for AI answer engines (ChatGPT, Perplexity, Google AI Overviews) that pull direct answers from web pages.

- [ ] **FAQ section** with 5-8 questions using FAQPage schema
- [ ] **Direct answer paragraphs** (2-3 sentences that directly answer common queries)
- [ ] **JSON-LD schema**: Service + FAQPage + LocalBusiness (all three)
- [ ] **"People also ask" style subheadings** (question-format H2s/H3s)
- [ ] **Statistics with sources** (AI engines prefer cited, specific data)
- [ ] **Clear entity definitions** ("What is [service]?" answered in first section)
- [ ] **Structured data** matches page content exactly (no schema stuffing)

---

## JSON-LD Schema Templates

### Service Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "[Service Name] for [Industry]",
  "description": "[One-sentence description of the service]",
  "provider": {
    "@type": "Organization",
    "name": "[Company Name]",
    "url": "[Website URL]"
  },
  "areaServed": {
    "@type": "Country",
    "name": "[Country]"
  },
  "serviceType": "[Type of service]",
  "offers": {
    "@type": "Offer",
    "price": "[Starting price]",
    "priceCurrency": "[Currency code]"
  }
}
```

### FAQPage Schema
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question from FAQ section]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Direct answer, 2-3 sentences]"
      }
    }
  ]
}
```

### LocalBusiness Schema
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[Company Name]",
  "url": "[Website URL]",
  "telephone": "[Phone number]",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "[City]",
    "addressCountry": "[Country code]"
  },
  "priceRange": "[Price range, e.g. $$]",
  "openingHours": "Mo-Fr 09:00-17:00"
}
```

---

## Quick Reference: Keyword Placement

| Location | Priority | Example |
|----------|----------|---------|
| Page title | Critical | "AI Voice Agents for Plumbers | 24/7 Booking | [Brand]" |
| H1 | Critical | "AI Voice Agents for Plumbers" |
| First paragraph | High | "Plumbing businesses lose $X per year from missed calls..." |
| H2 subheadings | Medium | "Why Plumbers Need AI Call Answering" |
| Meta description | High | "AI voice agents for plumbing businesses. Answer every call..." |
| Image alt text | Medium | "AI voice agent dashboard for plumbing dispatch" |
| URL slug | Medium | /ai-voice-agents/plumbers |
