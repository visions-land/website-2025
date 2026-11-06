#!/usr/bin/env python3
"""Generate the static Visions site.

Run from the project root:  python3 tools/build.py

Writes index.html, artists.html, exhibition.html, contact.html and
artist/<Id>.html. Everything else (CSS, JS, images, fonts) is hand-kept
under assets/. Artist copy lives in tools/data/artists.json.

Every translated string is emitted as two spans, <span lang="en"> and
<span lang="it">; assets/css/site.css shows one and hides the other based on
html[data-lang], so the site reads in English with JavaScript turned off.
"""

import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTISTS = json.loads((ROOT / "tools/data/artists.json").read_text("utf-8"))

EMAIL = "visions@napuleth.org"
TELEGRAM = "https://t.me/+yAnPodng62NhMGNk"
INSTAGRAM = "https://www.instagram.com/napuleth.visions/#"
HANDLE = "napulethvisions"


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def t(en, it=None):
    """A translated run of text: English visible by default, Italian hidden."""
    en_txt = html.escape(en)
    if it is None:
        return en_txt
    return f'<span lang="en">{en_txt}</span><span lang="it">{html.escape(it)}</span>'


def tt(pair, key="en"):
    """Translated text from a {"en":…, "it":…} dict in the data file."""
    if not pair:
        return ""
    return t(pair["en"], pair.get("it"))


ICONS = {
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-left": '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
    "calendar": '<path d="M8 2v4"/><path d="M16 2v4"/>'
    '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/>'
    '<path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "instagram": '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/>'
    '<path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/>'
    '<line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>',
    "map-pin": '<path d="M20 10c0 4.4-5.6 9.6-7.3 11.1a1 1 0 0 1-1.4 0C9.6 19.6 4 14.4 4 10a8 8 0 0 1 16 0"/>'
    '<circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "menu": '<line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/>'
    '<line x1="4" x2="20" y1="18" y2="18"/>',
}

TELEGRAM_SVG = (
    '<svg class="{cls}" viewBox="0 0 448 512" fill="currentColor" aria-hidden="true">'
    '<path d="M446.7 98.6l-67.6 318.8c-5.1 22.5-18.4 28.1-37.3 17.5l-103-75.9-49.7 47.8'
    "c-5.5 5.5-10.1 10.1-20.7 10.1l7.4-104.9 190.9-172.5c8.3-7.4-1.8-11.5-12.8-4.1"
    "L117.8 284 16.2 252.2c-22.1-6.9-22.5-22.1 4.6-32.7L418.2 66.4c18.4-6.9 34.5 4.1 28.5 32.2z"
    '"/></svg>'
)


def icon(name, cls="icon", extra=""):
    if name == "telegram":
        return TELEGRAM_SVG.format(cls=cls)
    return (
        f'<svg class="{cls}{(" " + extra) if extra else ""}" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
    )


NAV = [
    ("home", "index.html", "Home", "Home"),
    ("artists", "artists.html", "Artists", "Artisti"),
    ("exhibition", "exhibition.html", "Exhibition", "Mostra"),
    ("contact", "contact.html", "Contact", "Contatti"),
]


def header(active, prefix):
    nav = "\n".join(
        f'            <a href="{prefix}{href}"'
        f'{" aria-current=\"page\"" if key == active else ""}>{t(en, it)}</a>'
        for key, href, en, it in NAV
    )
    return f"""      <header class="site-header">
        <div class="container site-header__inner">
          <a class="site-header__logo" href="{prefix}index.html">
            <img src="{prefix}assets/images/logo.webp" alt="Visions" width="120" height="100">
          </a>
          <div class="site-header__right">
            <nav class="site-nav">
{nav}
            </nav>
            <p class="nav-sep" aria-hidden="true">|</p>
            <div class="lang-switch">
              <label class="sr-only" for="lang-select">{t("Language", "Lingua")}</label>
              <select id="lang-select">
                <option value="en">English</option>
                <option value="it">Italiano</option>
              </select>
            </div>
            <button class="menu-btn" type="button" aria-label="Menu" aria-controls="mobile-menu">
              {icon("menu")}
            </button>
          </div>
        </div>
      </header>"""


def mobile_menu(active, prefix):
    items = []
    for key, href, en, it in NAV:
        current = ' aria-current="page"' if key == active else ""
        dot = '<span class="menu-panel__dot"></span>' if key == active else ""
        items.append(
            f"            <li{current}><a href=\"{prefix}{href}\" data-menu-close>"
            f"{t(en, it)}</a>{dot}</li>"
        )
    lis = "\n".join(items)
    return f"""    <div class="menu-scrim"></div>
    <nav class="menu-panel" id="mobile-menu" aria-hidden="true">
      <div class="menu-panel__head">
        <img src="{prefix}assets/images/logo.webp" alt="Visions" width="80" height="80">
        <button class="menu-panel__close" type="button" aria-label="Close menu" data-menu-close>&times;</button>
      </div>
      <ul>
{lis}
      </ul>
    </nav>"""


def back_link(prefix, label=None):
    label = label or t("Back to Exhibition", "Torna alla Mostra")
    return f"""      <div class="container back-nav">
        <a href="{prefix}index.html">{icon("arrow-left")}{label}</a>
      </div>"""


def newsletter():
    """Kept for layout fidelity, but switched off: the static site has no
    mailing-list backend, so input and button are disabled."""
    return f"""      <section class="newsletter-section">
        <div class="container">
          <div class="newsletter">
            <h2>{t("Stay Connected with Visions", "Rimani Connesso con Visions")}</h2>
            <form class="newsletter__form" onsubmit="return false;">
              <div>
                <label class="sr-only" for="newsletter-email">{t("Email address", "Indirizzo email")}</label>
                <input class="input" id="newsletter-email" type="email" disabled
                       placeholder="Enter your email address"
                       data-ph-it="Inserisci il tuo indirizzo email">
              </div>
              <button class="btn btn--disabled" type="button" disabled aria-disabled="true">
                {t("Subscribe", "Iscriviti")}
              </button>
            </form>
            <p class="newsletter__note">{t(
                "Newsletter sign-up is currently closed.",
                "Le iscrizioni alla newsletter sono attualmente chiuse.")}</p>
          </div>
        </div>
      </section>"""


def footer():
    return f"""      <footer class="site-footer">
        <div class="container">
          <div class="site-footer__cols">
            <div>
              <h4>{t("Contact", "Contatti")}</h4>
              <div class="footer-links">
                <a href="mailto:{EMAIL}">{icon("mail")}<span>{EMAIL}</span></a>
                <a href="{TELEGRAM}" target="_blank" rel="noopener noreferrer">{icon("telegram", "icon")}<span>{HANDLE}</span></a>
                <a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">{icon("instagram")}<span>{HANDLE}</span></a>
              </div>
            </div>
          </div>
          <div class="site-footer__bottom">
            <p>{t("© 2025 Visions. All rights reserved.", "© 2025 Visions. Tutti i diritti riservati.")}</p>
          </div>
        </div>
      </footer>"""


def document(title_en, title_it, description, body, prefix, active):
    return f"""<!doctype html>
<html lang="en" data-lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title data-it="{html.escape(title_it, quote=True)}">{html.escape(title_en)}</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <link rel="icon" href="{prefix}assets/images/logo.webp">
  <link rel="preload" href="{prefix}assets/fonts/host-grotesk-latin-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{prefix}assets/css/site.css">
</head>
<body>
  <div class="page">
{body}
  </div>
{mobile_menu(active, prefix)}
  <script src="{prefix}assets/js/site.js"></script>
</body>
</html>
"""


# --------------------------------------------------------------------------
# copy
# --------------------------------------------------------------------------
INTRO = {
    "en": "Visions is a cultural project and exhibition format born within Napuleth Open "
    "Village, promoting dialogue and exchange between the world of Web3 and contemporary "
    "art. Conceived by a group of young creatives with transversal skills in art and "
    "technology, Visions aims to become a recurring event, exploring the intersections "
    "between the digital economy, innovation, and artistic practices. The initiative aims "
    "not only as an exhibition event, but as a stable and growing platform, with the goal "
    "of developing tailored technological solutions to redefine artistic production and "
    "enjoyment in the information and digital age.",
    "it": "Visions è un progetto culturale e format espositivo nato all’interno di Napuleth "
    "Open Village, che promuove il dialogo e lo scambio tra il mondo del Web3 e l’arte "
    "contemporanea. Ideato da un gruppo di giovani creativi con competenze trasversali in "
    "arte e tecnologia, Visions vuole diventare un appuntamento ricorrente, esplorando le "
    "intersezioni tra economia digitale, innovazione e pratiche artistiche. L’iniziativa si "
    "propone non solo come evento espositivo, ma come piattaforma stabile e in crescita, con "
    "l’obiettivo di sviluppare soluzioni tecnologiche su misura per ridefinire la produzione "
    "e la fruizione artistica nell’era dell'informazione e della digitalizzazione.",
}

CHAPTER_BLURB = {
    "en": "Curated by Alessio Esposito, Foresta di Cristallo, the inaugural exhibition of "
    "Visions, comes to life in the spaces of Villa Doria D’Angri in Naples. The exhibition "
    "brings together the works of Clarissa Falco, Lorenzo Lunghi, Adriano Tenore, and "
    "Emilio Vavarella.",
    "it": "A cura di Alessio Esposito. Negli spazi di Villa Doria D’Angri a Napoli prende "
    "vita Foresta di Cristallo, la mostra inaugurale di Visions. L’esposizione riunisce le "
    "opere di Clarissa Falco, Lorenzo Lunghi, Adriano Tenore ed Emilio Vavarella.",
}

DATE = ("17–19 July 2025", "17–19 Luglio 2025")

OVERVIEW = [
    (
        "On the occasion of Napuleth Open Village 2025, Visions is pleased to present "
        "Foresta di Cristallo, curated by Alessio Esposito. The exhibition inaugurates a "
        "format conceived as a platform for dialogue between the Web3 landscape and "
        "contemporary art. Set in the evocative spaces of Villa Doria d'Angri and open to "
        "the public from July 17 to 19, 2025, Foresta di Cristallo brings together works by "
        "Clarissa Falco, Lorenzo Lunghi, Adriano Tenore, and Emilio Vavarella.",
        "In occasione di Napuleth Open Village 2025, Visions è lieta di presentare Foresta di "
        "Cristallo, a cura di Alessio Esposito. L’esposizione inaugura il format concepito "
        "come una piattaforma di dialogo tra il panorama del Web3 e quello dell’arte "
        "contemporanea. Allestita nei suggestivi spazi di Villa Doria d’Angri e visitabile "
        "dal 17 al 19 luglio 2025, Foresta di Cristallo riunisce le opere di Clarissa Falco, "
        "Lorenzo Lunghi, Adriano Tenore ed Emilio Vavarella.",
    ),
    (
        "The title harks back to J.G. Ballard's novel of the same name (The Crystal World, "
        "1966), which describes a world in which nature undergoes a radical transformation: "
        "living beings and objects crystallize, merging in an irreversible process that "
        "strips them of their original identities. This phenomenon becomes a metaphor for a "
        "reality in which the distinction between humans, nature, and objects dissolves, "
        "creating a constantly fluid hybrid.",
        "Il titolo riprende l’omonimo romanzo di J.G. Ballard (The Crystal World, 1966), che "
        "descrive un mondo in cui la natura subisce una trasformazione radicale: esseri "
        "viventi e oggetti si cristallizzano, mescolandosi in un processo irreversibile che "
        "li priva delle loro identità originarie. Questo fenomeno diventa metafora di una "
        "realtà in cui la distinzione tra esseri umani, natura e oggetti si dissolve, "
        "creando un ibrido in costante fluidità.",
    ),
    (
        "These aspects are well-matched with Bruno Latour's thinking: for the French "
        "sociologist, reality is not composed of fixed matter or immutable essences, but "
        "rather of a web of forces that dissolves the traditional distinction between "
        "'being' and 'object.' This perspective undermines traditional dichotomies—physical "
        "and digital, art and market, subject and object—opening up reflections on how "
        "meaning itself is constructed in relational terms, both aesthetically (in meaning) "
        "and economically (in value).",
        "Tali aspetti sono ben assimilabili al pensiero di Bruno Latour: per il sociologo "
        "francese, infatti, la realtà non sarebbe composta da una materia fissa o da essenze "
        "immutabili ma da un intreccio di forze che dissolve la tradizionale distinzione tra "
        "“essere” e “oggetto”. Questa prospettiva scardina le tradizionali dicotomie – fisico "
        "e digitale, arte e mercato, soggetto e oggetto – aprendo a riflessioni su come il "
        "senso stesso si costruisca in termini relazionali, sia in ambito estetico (nel "
        "significato) che economico (nel valore).",
    ),
    (
        "In the latter, the discourse finds immediate parallels in the phenomenon of "
        "cryptocurrencies. These not only exemplify the overcoming of the centrality of one "
        "authority, but also embody the very idea of dematerialization of value: its "
        "attribution is thus entrusted to systems based on multi-party consensus and "
        "algorithms, rather than physical media.",
        "In quest’ultimo, il discorso trova corrispondenza immediata nel fenomeno delle "
        "criptovalute. Queste, non solo esemplificano il superamento della centralità di "
        "un’autorità, ma incarnano l’idea stessa di dematerializzazione del valore: la sua "
        "attribuzione viene così affidata a sistemi basati sul consenso di più parti e su "
        "algoritmi, piuttosto che a supporti fisici.",
    ),
    (
        "In this sense, Vavarella's work can be reinterpreted as staging an act of radical "
        "decentralization of the subject through the adoption of an animal point of view: "
        "thus, the aesthetic experience is simultaneously configured as a relationship and "
        "an act of liberation from anthropocentrism, displacing the centrality of the human "
        "in favor of another perspective. This dynamic manifests itself in Falco's "
        "sculptures through the hybridization of heterogeneous elements: these are "
        "concrescences, monstrosities in the Harawayan sense, which evoke forms of "
        "coexistence between the organic, the artificial, and the symbolic.",
        "In questa direzione, il lavoro di Vavarella può essere riletto come la messa in "
        "scena di un atto di radicale decentralizzazione del soggetto attraverso l’assunzione "
        "del punto di vista animale: così, l’esperienza estetica si configura al contempo "
        "come relazione e atto di liberazione dall’antropocentrismo, dislocando la centralità "
        "dell’umano a favore di una prospettiva altra. Questa dinamica si manifesta nelle "
        "sculture di Falco attraverso l’ibridazione di elementi eterogenei: si tratta di "
        "concrescenze, di mostruosità in senso harawayano, che evocano forme di coesistenza "
        "tra organico, artificiale e simbolico.",
    ),
    (
        "Tenore, on the other hand, interprets the hybrid in a postmedia perspective: his "
        "creatures do not belong to any existing species—rather, they constitute a bestiary "
        "generated by data processing. Lunghi's sculptures reinterpret this dynamic according "
        "to a parasitic logic: entities that discreetly yet persistently insert themselves "
        "and take root in their environments, activating dynamics of cohabitation and latent "
        "symbiosis.",
        "Tenore declina invece l’ibrido in una chiave postmediale: le sue creature non "
        "appartengono a nessuna specie esistente – costituiscono, piuttosto, un bestiario "
        "generato dall’elaborazione di dati. Le sculture di Lunghi reinterpretano questa "
        "dinamica secondo una logica parassitaria: entità che si inseriscono e si radicano "
        "negli ambienti in modo discreto ma persistente, attivando dinamiche di coabitazione "
        "e simbiosi latente.",
    ),
    (
        "The exhibition explores the process of dematerialization of value – characteristic "
        "of post-digital economies – reflected in the production of meaning in art, "
        "suggesting how the aesthetic and economic dimensions are constantly being "
        "redefined, shaped by a network of interconnected actors and relationships.",
        "La mostra esplora come il processo di dematerializzazione del valore – "
        "caratteristico delle economie post-digitali – si rifletta nella produzione del "
        "significato nell’arte, suggerendo come le dimensioni estetica ed economica siano in "
        "costante ridefinizione, modellate da una rete di attori e relazioni interconnesse.",
    ),
    (
        "In this scenario, the interference between heterogeneous languages and "
        "temporalities—activated by the dialogue between the works, the architecture, and "
        "the decorations of Villa Doria d'Angri—helps strengthen the exhibition's hybrid "
        "horizon: between digital organisms and posthuman monstrosities, Foresta di Cristallo "
        "grafts itself onto the space, multiplying its levels of interpretation, bringing to "
        "light contradictions, frictions, and unexpected areas of intersection.",
        "In questo scenario, l'interferenza tra linguaggi e temporalità eterogenee – attivata "
        "dal dialogo tra le opere, l’architettura e le decorazioni di Villa Doria d’Angri – "
        "contribuisce a rafforzare l’orizzonte ibrido della mostra: tra organismi digitali e "
        "mostruosità postumane, Foresta di Cristallo si innesta nello spazio moltiplicandone "
        "i livelli di lettura, facendo emergere contraddizioni, attriti e zone di "
        "intersezione inattese.",
    ),
]

COLOPHON = [
    (t("Colophon Impressum Visions", "Colophon Impressum Visions"),),
    (t("Works by", "Opere di") + ": Clarissa Falco, Lorenzo Lunghi, Adriano Tenore, Emilio Vavarella",),
    (t("Curated by", "A cura di") + ": Alessio Esposito",),
    ("Project Manager: Fabiola Cangiano",),
    (t("Texts", "Testi") + ": Francesca Blandino, Alessio Esposito, Franco Speroni, Stefano Taccone",),
    (t("Translations", "Traduzioni") + ": Giuseppe Giuliano",),
    (t("Thanks to", "Si ringrazia") + ": Francesca Blandino, Alessandra Troncone",),
    (t("Photo credits", "Crediti foto") + ": Danilo Donzelli",),
]

SPONSORS = [
    ("https://www.teatrodisancarlo.it/", "assets/images/sponsors/SanCarlo.png", "Teatro di San Carlo", "sponsor--h32"),
    ("https://www.associazionecivita.it/", "assets/images/sponsors/civita.png", "Associazione Civita", "sponsor--h32"),
    ("https://www.comunenapoli.it/", "assets/images/sponsors/commune.webp", "Comune di Napoli", "sponsor--h32"),
    ("https://www.fmgreco.it/", "assets/images/sponsors/FMG_Logo.webp", "Fondazione Morra Greco", "sponsor--h24"),
    ("https://www.familiae.it/", "assets/images/sponsors/FAMILIAE.webp", "Familiae", "sponsor--h52"),
    ("", "assets/images/sponsors/FRG.webp", "FRG", "sponsor--h64"),
]


def sponsors_block():
    def group():
        out = []
        for href, src, alt, cls in SPONSORS:
            tag = (
                f'<a class="{cls}" href="{href}" target="_blank" rel="noopener noreferrer">'
                if href
                else f'<span class="{cls}">'
            )
            close = "</a>" if href else "</span>"
            out.append(f'            {tag}<img src="{src}" alt="{alt}">{close}')
        return "\n".join(out)

    # the track is duplicated so the -50% translation loops seamlessly
    return f"""      <section class="container sponsors-section">
        <div class="sponsors">
          <div class="sponsors__fade sponsors__fade--left"></div>
          <h2>{t("With The Patronage Of", "Con il Patrocinio di")}</h2>
          <div class="marquee">
            <div class="marquee__track">
              <div class="marquee__group">
{group()}
              </div>
              <div class="marquee__group" aria-hidden="true">
{group()}
              </div>
            </div>
          </div>
          <div class="sponsors__fade sponsors__fade--right"></div>
        </div>
      </section>"""


# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------
def works_count(n, capitalized=False):
    """'1 work' / '2 works' — the original template always said 'works'."""
    en = f"{n} work" if n == 1 else f"{n} works"
    it = f"{n} opera" if n == 1 else f"{n} opere"
    if capitalized:
        en, it = en.replace("work", "Work"), it.replace("oper", "Oper")
    return t(en, it)


def sorted_artists():
    return sorted(ARTISTS, key=lambda a: a["name"].split(" ")[1])


def total_pieces():
    return sum(a["works"] for a in ARTISTS)


def page_home():
    tiles = "\n".join(
        f"""            <a class="artist-tile" href="artist/{a["id"]}.html">
              <div class="artist-tile__media">
                <img src="{a["image"]}" alt="{html.escape(a["name"])}" loading="lazy">
              </div>
              <div class="artist-tile__body">
                <h3>{html.escape(a["name"])}</h3>
                <div class="artist-tile__foot">
                  <span>{works_count(a['works'])}</span>
                  {icon("arrow-right")}
                </div>
              </div>
            </a>"""
        for a in sorted_artists()
    )

    rows = [
        (t("Dates", "Date"), t(*DATE)),
        (t("Venue", "Luogo"), "Villa Doria D'Angri"),
        (t("Location", "Località"), t("Naples, Italy", "Napoli, Italia")),
        (t("Artists", "Artisti"), str(len(ARTISTS))),
        (t("Artworks", "Opere"), works_count(total_pieces()).replace("works", "pieces")),
    ]
    rows_html = "\n".join(
        f'                <div class="details__row"><dt>{k}</dt><dd>{v}</dd></div>'
        for k, v in rows
    )

    body = f"""{header("home", "")}

      <section class="hero">
        <div class="container hero__grid">
          <div class="hero__copy">
            <div class="hero__intro">
              <p>{tt(INTRO)}</p>
              <div class="hero__chapter">
                <h2>{t("Chapter", "Capitolo")} 1: Foresta di Cristallo</h2>
                <p>{tt(CHAPTER_BLURB)}</p>
              </div>
              <div class="hero__meta">
                <span class="badge shiny-badge">{icon("calendar")}<span>{t(*DATE)}</span></span>
              </div>
            </div>
            <div class="hero__actions">
              <a href="artists.html">
                <button class="btn btn--primary btn--block shiny-button" type="button">
                  {t("View Artists", "Vedi Artisti")}{icon("arrow-right", "icon", "icon--nudge")}
                </button>
              </a>
              <a href="exhibition.html">
                <button class="btn btn--outline btn--block" type="button">{t("Exhibition", "Mostra")}</button>
              </a>
            </div>
          </div>
          <div class="hero__media">
            <div class="card card--shadow">
              <img src="assets/images/4.webp" alt="Villa Doria D'Angri">
            </div>
          </div>
        </div>
      </section>

      <section class="artists-strip">
        <div class="container">
          <div class="section-heading">
            <h2>{t("Artists", "Artisti")}</h2>
          </div>
          <div class="artist-grid">
{tiles}
          </div>
          <div class="artists-strip__cta">
            <a href="artists.html">
              <button class="btn btn--outline on-gray" type="button">{t("Artists Information", "Informazioni Artisti")}</button>
            </a>
          </div>
        </div>
      </section>

      <section class="details">
        <div class="container details__grid">
          <div class="details__media">
            <h2>{t("About the Exhibition", "A Proposito Della Mostra")}</h2>
            <div class="details__media-frame">
              <img src="assets/images/windows.webp" alt="Foresta di Cristallo, Villa Doria D'Angri" loading="lazy">
            </div>
          </div>
          <div class="details__list">
            <h3>{t("Exhibition Details", "Dettagli Mostra")}</h3>
            <dl class="details__rows">
{rows_html}
            </dl>
          </div>
        </div>
      </section>

{sponsors_block()}

{newsletter()}

{footer()}"""

    return document(
        "Visions — Digital Art Exhibition",
        "Visions — Mostra di Arte Digitale",
        "Visions is a cultural project and exhibition format exploring the intersections "
        "between contemporary art, innovation and digital culture. Chapter 1: Foresta di "
        "Cristallo, Villa Doria D'Angri, Naples.",
        body,
        "",
        "home",
    )


def page_artists():
    rows = []
    for i, a in enumerate(sorted_artists()):
        flip = " artist-row--flip" if i % 2 else ""
        rows.append(
            f"""          <div class="artist-row{flip}">
            <div class="artist-row__media">
              <div class="card card--shadow">
                <img src="{a["image"]}" alt="{html.escape(a["name"])}" loading="lazy">
              </div>
            </div>
            <div class="artist-row__copy">
              <div>
                <h2>{html.escape(a["name"])}</h2>
                <h5>{tt(a["short"])}</h5>
                <div class="artist-row__count">{works_count(a['works'], True)}</div>
              </div>
              <a href="artist/{a["id"]}.html">
                <button class="btn btn--primary shiny-button" type="button">
                  {t("View Artworks", "Vedi Opere")}{icon("arrow-right", "icon", "icon--nudge")}
                </button>
              </a>
            </div>
          </div>"""
        )

    body = f"""{header("artists", "")}

{back_link("")}

      <section class="container page-head">
        <div class="page-head__inner">
          <h1>{t("Artists", "Artisti")}</h1>
        </div>
      </section>

      <section class="container artist-rows">
{chr(10).join(rows)}
      </section>

{newsletter()}

{footer()}"""

    return document(
        "Artists — Visions",
        "Artisti — Visions",
        "The four artists of Foresta di Cristallo: Clarissa Falco, Lorenzo Lunghi, "
        "Adriano Tenore and Emilio Vavarella.",
        body,
        "",
        "artists",
    )


def page_artist(a):
    works = []
    for w in a["detailedWorks"]:
        parts = [f"              <h3>{html.escape(w['title'])}</h3>"]
        if w["description"]:
            parts.append(f"              <p>{tt(w['description'])}</p>")
        if w["technique"]:
            parts.append(f"              <p>{tt(w['technique'])}</p>")
        gallery = ""
        if w["gallery"]:
            imgs = "\n".join(
                f'                <img src="../{src}" alt="{html.escape(w["title"])}" loading="lazy">'
                for src in w["gallery"]
            )
            gallery = f"""
            <div class="work__gallery">
{imgs}
            </div>"""
        works.append(
            f"""          <article class="work">
            <div class="work__media">
              <div class="card card--shadow">
                <img src="../{w["image"]}" alt="{html.escape(w["title"])}" loading="lazy">
              </div>{gallery}
            </div>
            <div class="work__copy">
{chr(10).join(parts)}
            </div>
          </article>"""
        )

    body = f"""{header("artists", "../")}

{back_link("../", t("Back to Artists", "Torna agli Artisti")).replace('href="../index.html"', 'href="../artists.html"')}

      <section class="artist-intro">
        <div class="container artist-intro__inner">
          <h1>{html.escape(a["name"])}</h1>
          <div class="artist-intro__cols">
            <div>
              <h3>{t("Biography", "Biografia")}</h3>
              <p>{tt(a["bio"])}</p>
            </div>
            <div>
              <h3>{t("Artist Statement", "Artist Statement")}</h3>
              <p>{tt(a["statement"])}</p>
            </div>
          </div>
        </div>
      </section>

      <section class="container works">
{chr(10).join(works)}
      </section>

{newsletter()}

{footer()}"""

    return document(
        f"{a['name']} — Visions",
        f"{a['name']} — Visions",
        f"{a['name']} in Foresta di Cristallo, Chapter 1 of Visions, Villa Doria D'Angri, Naples.",
        body,
        "../",
        "artists",
    )


def page_exhibition():
    paras = "\n".join(f"              <p>{t(en, it)}</p>" for en, it in OVERVIEW)
    colophon = "\n".join(f"              <p>{line[0]}</p>" for line in COLOPHON)
    shots = "\n".join(
        f"""            <div class="card card--shadow">
              <img src="assets/images/installation/{n}.webp" alt="Foresta di Cristallo, installation view" loading="lazy">
            </div>"""
        for n in range(1, 20)
    )

    body = f"""{header("exhibition", "")}

{back_link("")}

      <section class="container page-head" style="padding-top:4rem">
        <div class="page-head__inner">
          <h1>Foresta di Cristallo</h1>
        </div>
      </section>

      <section class="container exhibition-body">
        <div class="exhibition-body__grid">
          <div class="exhibition-main">
            <div class="exhibition-text">
{paras}
{colophon}
            </div>

            <div class="installation">
              <h2>{t("Installation View", "Installation View")}</h2>
              <div class="installation__grid">
{shots}
              </div>
            </div>
          </div>

          <aside class="exhibition-aside">
            <div class="card card--bordered">
              <h3>{t("Show Info", "Informazioni sulla mostra")}</h3>
              <div class="fact-list">
                <div class="fact">
                  {icon("calendar", "icon-lg")}
                  <div>
                    <p class="fact__label">{t("Duration", "Durata")}</p>
                    <p class="fact__value">{t(*DATE)}</p>
                  </div>
                </div>
                <div class="fact">
                  {icon("map-pin", "icon-lg")}
                  <div>
                    <p class="fact__label">{t("Location", "Località")}</p>
                    <p class="fact__value">Villa Doria D'Angri, {t("Naples", "Napoli")}</p>
                  </div>
                </div>
                <div class="aside-block">
                  <p class="aside-block__label">{t("Opening Hours", "Orari")}</p>
                  <p>{t("17 July 2025: 6 PM – 10 PM", "17 Luglio 2025: 18:00 – 22:00")}</p>
                  <p>{t("18 – 19 July 2025: 9 AM – 6 PM", "18 – 19 Luglio 2025: 9:00 – 18:00")}</p>
                </div>
                <div class="aside-block">
                  <p class="aside-block__label">{t("Admission", "Ingresso")}</p>
                  <p>{t("Free admission", "Ingresso gratuito")}</p>
                  <p>{t("Registration recommended", "Registrazione raccomandata")}</p>
                </div>
                <div class="aside-block">
                  <p class="aside-block__label">{t("Accessibility", "Accessibilità")}</p>
                  <p>{t("Wheelchair accessible", "Accessibile ai disabili")}</p>
                  <p>{t("Audio guides available", "Audioguide disponibili")}</p>
                </div>
              </div>
            </div>

            <div class="card card--bordered">
              <h3>{t("Contact", "Contatti")}</h3>
              <div class="aside-contact">
                <div>
                  <p>{t("Email", "Email")}</p>
                  <a href="mailto:{EMAIL}"><p>{EMAIL}</p></a>
                </div>
                <div>
                  <p>Telegram</p>
                  <a href="{TELEGRAM}" target="_blank" rel="noopener noreferrer"><p>{HANDLE}</p></a>
                </div>
                <div>
                  <p>Instagram</p>
                  <a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer"><p>{HANDLE}</p></a>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </section>

{newsletter()}

{footer()}"""

    return document(
        "Foresta di Cristallo — Visions",
        "Foresta di Cristallo — Visions",
        "Foresta di Cristallo, curated by Alessio Esposito: Chapter 1 of Visions at Villa "
        "Doria D'Angri, Naples, 17–19 July 2025.",
        body,
        "",
        "exhibition",
    )


def page_contact():
    body = f"""{header("contact", "")}

{back_link("")}

      <section class="container page-head">
        <div class="page-head__inner">
          <h1>{t("Contact Us", "Contattaci")}</h1>
          <p>{t(
            "Get in touch with our team for inquiries about the exhibition, press "
            "opportunities, or general information.",
            "Contattaci per informazioni sulla mostra, opportunità di stampa o informazioni "
            "generali.")}</p>
        </div>
      </section>

      <section class="container contact-body">
        <div class="contact-body__grid">
          <div>
            <div class="contact-card">
              <div class="contact-card__head">
                <h2>{t("Send us a message", "Invia un messaggio")}</h2>
              </div>
              <div class="contact-card__body">
                <form class="form" onsubmit="return false;">
                  <div class="form__row">
                    <div>
                      <label for="name">{t("Name", "Nome")} <span class="req">*</span></label>
                      <input class="input" id="name" name="name" disabled>
                    </div>
                    <div>
                      <label for="email">{t("Email", "Email")} <span class="req">*</span></label>
                      <input class="input" id="email" name="email" type="email" disabled>
                    </div>
                  </div>
                  <div>
                    <label for="subject">{t("Subject", "Oggetto")} <span class="req">*</span></label>
                    <input class="input" id="subject" name="subject" disabled>
                  </div>
                  <div>
                    <label for="message">{t("Message", "Messaggio")} <span class="req">*</span></label>
                    <textarea class="input" id="message" name="message" rows="6" disabled></textarea>
                  </div>
                  <button class="btn btn--disabled btn--block" type="button" disabled aria-disabled="true">
                    {t("Send Message", "Invia")}
                  </button>
                  <p class="form__note">{t(
                    "This form is not active. Please write to", "Questo modulo non è attivo. Scrivici a")}
                    <a href="mailto:{EMAIL}"><strong>{EMAIL}</strong></a>.</p>
                </form>
              </div>
            </div>
          </div>

          <div class="contact-info">
            <div>
              <h2>{t("Get in Touch", "Contattaci")}</h2>
            </div>
            <div class="contact-info__list">
              <div class="contact-info__item">
                {icon("mail", "icon-lg")}
                <div>
                  <h3>{t("Email", "Email")}</h3>
                  <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
                </div>
              </div>
              <div class="contact-info__item">
                {icon("clock", "icon-lg")}
                <div>
                  <h3>{t("Exhibition Hours", "Orari Mostra")}</h3>
                  <div>
                    <p>{t("17 July 2025: 6 PM – 10 PM", "17 Luglio 2025: 18:00 – 22:00")}</p>
                    <p>{t("18 – 19 July 2025: 9 AM – 6 PM", "18 – 19 Luglio 2025: 9:00 – 18:00")}</p>
                    <p>{t("Free admission", "Ingresso gratuito")}</p>
                  </div>
                </div>
              </div>
              <div class="contact-info__item">
                {icon("instagram", "icon-lg")}
                <div>
                  <h3>Instagram</h3>
                  <div><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">{HANDLE}</a></div>
                </div>
              </div>
              <div class="contact-info__item">
                {icon("telegram", "icon-lg")}
                <div>
                  <h3>Telegram</h3>
                  <div><a href="{TELEGRAM}" target="_blank" rel="noopener noreferrer">{HANDLE}</a></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

{footer()}"""

    return document(
        "Contact — Visions",
        "Contatti — Visions",
        "Contact Visions about the exhibition, press or general information.",
        body,
        "",
        "contact",
    )


def main():
    written = []

    def write(path, text):
        p = ROOT / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        written.append((path, len(text)))

    write("index.html", page_home())
    write("artists.html", page_artists())
    write("exhibition.html", page_exhibition())
    write("contact.html", page_contact())
    for a in ARTISTS:
        write(f"artist/{a['id']}.html", page_artist(a))

    for path, size in written:
        print(f"{path:34} {size / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
