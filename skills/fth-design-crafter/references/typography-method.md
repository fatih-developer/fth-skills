# Typography Method (FOUNDATIONS)

Pick type that says something about this product. The default families most interfaces share (Inter, Roboto, Open Sans, Poppins, Montserrat, Lato) and the families AI tools reach for (Space Grotesk, Fraunces, Instrument Serif, Geist, Plus Jakarta Sans, Manrope, Outfit, DM Sans, Satoshi, General Sans) are excluded by default. They are allowed only when the brand already uses them or the rationale explains why they are the best fit.

## 1. Describe the project in type terms

Translate the product into 3-4 typographic traits before looking at any font list.

| Product character | Traits to look for |
|---|---|
| Logistics, industry, infrastructure | Condensed or compact grotesque, slab serif, stencil-like weight, tabular figures |
| Finance, legal, insurance | Transitional or modern text serif, or a humanist sans with tabular figures; restrained weights |
| Health, public services, accessibility-first | High-legibility humanist sans, distinct I/l/1 and 0/O, generous x-height |
| Editorial, publishing, culture | Text serif with optical sizes, expressive display serif for headlines |
| Developer tools, data products | Neo-grotesque or grotesque with a good monospace companion |
| Food, craft, hospitality | Warm serif or humanist sans, soft terminals, lively italics |
| Children, education | Rounded or open humanist forms, large x-height, not a novelty face |
| Luxury, fashion | High-contrast serif, wide spacing, light weights used large |

Traits vocabulary: construction (geometric, grotesque, neo-grotesque, humanist, slab, transitional, old-style, didone, rounded, monospace, stencil), width (condensed, normal, extended), contrast (low, medium, high), terminals (flat, angled, rounded, ball), aperture (open, closed), x-height (small, large), and details such as single- or double-story `a`/`g`.

## 2. Read the logo

- **SVG with live text:** read `font-family` from the file; that family (if licensed) is the strongest candidate for headings.
- **Outlined SVG or raster logo:** describe its letterforms with the traits vocabulary (for example "geometric construction, flat terminals, single-story a, low contrast, slightly condensed"). Mark the description as inferred.
- **Match, do not clone:** choose a heading face that shares 2-3 of the logo's traits so the wordmark and headings feel related; keep the logo itself unique. Choose the body face for reading, with a complementary construction (a geometric logo often pairs better with a humanist text face than with another geometric one).
- **No logo:** start from the product-character table.

## 3. Find candidates

```bash
python <skill-dir>/scripts/find_fonts.py search --category sans-serif --axes wdth --limit 15   # compact grotesques with width axis
python <skill-dir>/scripts/find_fonts.py search --category serif --variable --axes opsz          # text serifs with optical sizes
python <skill-dir>/scripts/find_fonts.py search --category display --query slab
python <skill-dir>/scripts/find_fonts.py check "Family One" "Family Two"
```

The search skips the Google Fonts top 60, the overused and AI-favorite lists, vendor brand families, and families without Turkish support. Look beyond Google Fonts too (see `references/font-sources.md`), but check license, hosting, and glyph coverage yourself for anything off Google Fonts.

For each direction pick:

- **Heading:** carries personality; 2 weights at most.
- **Body:** optimized for reading at 14-18px; 2 weights (regular, semibold/bold); italics only if content needs them.
- **Mono (optional):** only for codes, IDs, tracking numbers, or data tables.
- One family for both slots is fine when it has enough range (widths or optical sizes).

## 4. Verify

- **Turkish:** `latin-ext` must be present (`find_fonts.py check` shows `TR yes`). In the specimen, test `ğ ş ı İ Ğ Ş`, uppercase headings (`İSTANBUL`, `IĞDIR`), and the Turkish lira sign `₺`.
- **Weights:** every weight you specify must exist (the specimen check fails otherwise).
- **License:** OFL or equivalent for Google Fonts; record the license for anything else.
- **Performance:** at most 2 families and 4 font files on first load; prefer variable fonts; use `display=swap` and system fallbacks with similar metrics.
- **Distinctness:** directions must not share the heading family.

## 5. Scale and rhythm

- Choose a modular ratio by density: 1.125-1.2 for dense apps, 1.25 for general product UI, 1.333 or more for editorial and marketing pages.
- Body 16px (15px acceptable for dense apps), line-height 1.45-1.65 for body and 1.05-1.2 for headings.
- Line length 45-75 characters; serif body text gets slightly more line-height.
- Use tabular figures for prices, quantities, and tables where the font supports them.
- Avoid ALL CAPS body labels and single-word color or italic accents in headlines.
