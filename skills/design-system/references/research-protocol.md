# Research Protocol (FOUNDATIONS)

Every palette and type choice must trace back to evidence: the project's own assets, the competitive landscape, real-world typography, or the domain's physical materials. "It looks modern" is not evidence.

## When to scan

- **No established brand:** scan by default. Tell the user first, in one line, which kinds of sites you will read (read-only, public pages only).
- **Established brand:** scan only to position the brand (where it sits against competitors); do not replace the brand.
- **User says no, or no network/browsing tool:** skip the scan, say so in `design-research.md`, and work from project context. Never claim a scan you did not run.

## Steps

1. **Project evidence.** Collect what already exists: logo (SVG or image), brand colors, current CSS/tokens (`scan_site.py` on the project's own site), screenshots, audience, market, and product domain. Existing brand assets outrank every other source.
2. **Competitors and category (3-5 sites).** Ask the user for competitors, or search for the category in the target market. Run:

   ```bash
   python <skill-dir>/scripts/scan_site.py https://competitor-a.com https://competitor-b.com https://competitor-c.com --json > design/landscape.json
   ```

   Record per site: theme, background/text, top accents, fonts, and gradient count. Record the landscape: occupied accent hues, free accent hues, and fonts shared by several competitors.
3. **Typography in use (2-3 references).** Look for how comparable products, publications, or signage in the domain use type (Fonts In Use, Typewolf, the domain's printed materials). Note the traits that recur (condensed grotesques on freight documents, transitional serifs in finance reports) rather than copying a specific site.
4. **Domain materials.** Name 3-5 physical or cultural materials of the domain (kraft paper, container steel, hospital signage, harbor rope, ledger paper) and sample hue/lightness ideas from them. These give palettes that belong to the product instead of to a generator.
5. **Candidate fonts.** Use `find_fonts.py search` with the traits you need; it excludes the most popular families and AI-favorite picks by default and requires Turkish (latin-ext) support. Check any font found elsewhere with `find_fonts.py check`.
6. **Write `design/design-research.md`** from `templates/design-research.template.md` before proposing directions.

## Using competitor data

- Competitor palettes are **input for positioning**, not something to reuse. Never copy a competitor's primary color or font pairing.
- Decide explicitly: **differentiate** (take a free hue, a different neutral temperature, or a different type construction) or **follow a category convention** when trust depends on it (for example, restrained blues in healthcare). If you follow a convention, differentiate through neutrals, chroma, typography, and shape instead.
- If most competitors use gradients, glow, or the same framework defaults, that is a signal to go flat and specific, not a trend to follow.

## Ethics and limits

- Read public pages only; one request per page or stylesheet; no logins, no crawling beyond the pages named.
- Fonts or assets you see on another site are not licensed to you. Verify licenses for everything you propose.
- Separate **observed** facts (measured values, URLs) from **inferred** judgments in the research note.
