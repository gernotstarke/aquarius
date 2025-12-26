# Icons Directory

Add icon images here to enhance the homepage feature boxes.

## Suggested Icons

```
icons/
├── requirements.png  # For Requirements section (e.g., checklist icon)
├── architecture.png  # For Architecture section (e.g., blueprint icon)
└── application.png   # For Application section (e.g., rocket icon)
```

## Size Recommendations

- **Format**: PNG or SVG
- **Size**: 128x128px to 256x256px
- **Style**: Simple, flat design matching arc42.org aesthetic
- **Color**: Blue tones (#2c5aa0) or monochrome

## Usage in index.md

Once icons are added, update the `aquarius_sections` in `index.md`:

```yaml
aquarius_sections:
  - title: "Requirements"
    excerpt: "![Requirements](/assets/images/icons/requirements.png)<br>
    User stories, use cases..."
```

## Free Icon Sources

- [Font Awesome](https://fontawesome.com) - Icon fonts
- [Heroicons](https://heroicons.com) - MIT licensed SVG icons
- [Lucide](https://lucide.dev) - Beautiful open source icons
- [Iconoir](https://iconoir.com) - Free SVG icons

For now, the feature row works without images and displays clean text boxes.
