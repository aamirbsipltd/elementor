# CIWA Elementor

Standalone Elementor-based WordPress theme for Canadian Immigrant Women's Association — a parallel build to the Gutenberg `ciwa-final` theme.

## What this is

A minimal WordPress theme that hands rendering entirely over to Elementor. Every page seeded by this theme is set to Elementor Canvas template — meaning Elementor renders the full page (no theme header/footer interference).

## What's included

- **Minimal theme files** (`index.php`, `header.php`, `footer.php`, `page.php`, `single.php`) — used only for archive/search/404 fallbacks
- **41 brand image assets** in `assets/img/` (icons, photos, logos)
- **Self-hosted brand fonts** in `assets/fonts/` (Cormorant Garamond, Inter)
- **`inc/seed-pages.php`** — on theme activation, auto-creates 20 blank Pages (Home + 19 inner) with Elementor Canvas template assigned and Elementor edit-mode flagged
- **`inc/elementor-presets.php`** — on first Elementor boot, seeds the active "kit" with 11 Global Colors and 4 Global Fonts from CIWA brand tokens, so every widget pulls from brand variables

## Deployment workflow (Bitnami WP on Railway)

### Step 1 — push this repo to GitHub

```bash
cd C:\Users\aamir\ciwa-elementor
git init -b main
git add -A
git commit -m "Initial: CIWA Elementor theme scaffold"
gh repo create ciwa-elementor --public --source=. --remote=origin --push
```

### Step 2 — create the Railway service

1. Go to [railway.app](https://railway.app), create a new project named `ciwa-elementor`
2. Add a service → **Deploy from GitHub repo** → pick `ciwa-elementor`
3. Add a **Bitnami WordPress** template service alongside it (separate service in the same project)
4. The Bitnami WP container will spin up at a `*.up.railway.app` URL — note that URL

### Step 3 — point Bitnami at this theme

Set the following env vars on the Bitnami WordPress service:

```
WORDPRESS_THEME_REPO=https://github.com/<your-user>/ciwa-elementor.git
WORDPRESS_THEME_SLUG=ciwa-elementor
WORDPRESS_DATA_TO_PERSIST=/bitnami/wordpress/wp-content/uploads /bitnami/wordpress/wp-content/plugins
```

(The third line excludes `themes/` from the persistent volume, so git pushes to this repo are picked up on each container restart.)

### Step 4 — install Elementor plugins

After the WP container is up:

1. Open `https://<your-railway-domain>/wp-admin/`
2. Log in with the Bitnami auto-generated credentials (Railway logs show them on first boot)
3. **Plugins → Add New → search "Elementor"** → Install + Activate (the free plugin)
4. **Plugins → Add New → Upload Plugin** → upload the `elementor-pro-4.0.2.zip` from your Downloads folder → Activate
5. Enter your Elementor Pro license key (Elementor → License)

### Step 5 — activate the CIWA Elementor theme

1. **Appearance → Themes** → activate **CIWA Elementor**
2. On activation, the seeder runs once and creates 20 blank pages
3. The Elementor preset hook runs on next page load and seeds the kit with brand colors + fonts

### Step 6 — start building pages

1. **Pages → Home → Edit with Elementor** → build the homepage
2. Each widget that exposes a Color picker can pick from **Global Colors** → CIWA Primary / Pink / Orange / etc.
3. Each text widget can pick from **Global Fonts** → CIWA Display / Body

## Brand tokens reference

Global Colors registered on activation:

| Token slug | Hex | Use |
|---|---|---|
| `primary` | `#6a1753` | Primary purple — headings, buttons |
| `secondary` | `#e22371` | Pink accent |
| `text` | `#1a1a1a` | Body text |
| `accent` | `#f68b3c` | Orange CTA |
| `ciwa-coral` | `#ff6e6e` | Coral accent |
| `ciwa-teal` | `#5bbdad` | Teal accent |
| `ciwa-olive` | `#aaa835` | Olive accent |
| `ciwa-cream` | `#fdf6ef` | Cream surface |
| `ciwa-pink-bg` | `#fce7f0` | Pink surface (hero bg) |
| `ciwa-muted` | `#4a4a4a` | Body text muted |
| `ciwa-border` | `#e6dce4` | Card/divider border |

Global Fonts:

| Token slug | Family | Weight |
|---|---|---|
| `primary` | Cormorant Garamond | 400 |
| `secondary` | Cormorant Garamond | 700 |
| `text` | Inter | 400 |
| `accent` | Inter | 600 |

## Reference site

The Gutenberg-built version of this site lives at:

- Repo: https://github.com/aamirbsipltd/ciwa-final
- Live: https://ciwa-final-production.up.railway.app/

All 20 pages from the Figma source have been built there in Gutenberg patterns — useful as a visual reference for what each Elementor page should look like.

## License

GPL-2.0-or-later.
