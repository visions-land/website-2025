# Visions — static site

A plain HTML/CSS/JS port of the former Next.js site. No build step, no
dependencies, no server code: open `index.html` or drop the folder on any
static host (GitHub Pages, Netlify, S3, a plain nginx directory).

## Layout

```
index.html              Home — Chapter 1: Foresta di Cristallo
artists.html            The four artists
exhibition.html         Exhibition text, colophon, installation views
contact.html            Contact details
artist/<Id>.html        One page per artist with their works
assets/css/site.css     All styling (hand-written, no framework)
assets/js/site.js       EN/IT switch + mobile menu — the only scripts
assets/fonts/           Host Grotesk, self-hosted (no Google Fonts call)
assets/images/          Photography, artist portraits, sponsor logos
tools/build.py          Regenerates the HTML pages
tools/data/artists.json Artist bios, statements and work descriptions
```

## Editing

Headers, footers and page structure live in `tools/build.py`; artist copy
lives in `tools/data/artists.json`. After changing either, regenerate:

```sh
python3 tools/build.py
```

That rewrites the eight HTML files in place. Editing the generated HTML
directly works too, but the next build overwrites it — prefer the generator for
anything repeated across pages (nav, footer, newsletter block).

CSS, JavaScript, images and fonts are *not* generated; edit them directly.

## Bilingual text

Every translated string ships in the page twice:

```html
<span lang="en">Exhibition</span><span lang="it">Mostra</span>
```

`assets/css/site.css` shows one and hides the other according to
`html[data-lang]`. `site.js` only flips that attribute and remembers the choice
in `localStorage`. With JavaScript off, the site reads correctly in English.

## What changed from the original

- No prices, no ETH/fiat conversion, no purchase modal, no payment icons, no
  "sold"/"coming soon" states — the whole commerce path is gone, along with the
  Stripe/Crossmint API routes.
- "Edition 1" is now "Chapter 1".
- Newsletter sign-up and the contact form are kept for layout but disabled; the
  contact page points at the email address instead.
- Branding reads "Visions"; the footer says "© 2025 Visions".
- Adriano Tenore's seven "Coming Soon" placeholder entries became a gallery of
  further stills under *Bestiario Sintetico* (same images, no empty cards).
- Lorenzo Lunghi had three identical *Vomito* records pointing at one image;
  they are now a single entry, so his count reads 2 works and the site total
  reads 12 pieces.
