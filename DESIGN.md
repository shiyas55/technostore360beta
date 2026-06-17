# TechnoStore360 Design System Documentation

This document provides a detailed, technical breakdown of the TechnoStore360 website design system. It details the brand styles, colors, layouts, typography, breakpoints, animations, components, and page-by-page design structure **exactly as implemented** in the project's source code (HTML, CSS, and JS).

---

## 1. Color System

### Brand Colors
The brand colors are configured as CSS variables in the `:root` scope of [styles.css](file:///Users/shiyasahmad/.gemini/antigravity/scratch/technostore360/css/styles.css):

| Token Name | HEX Value | Description / Usage |
| :--- | :--- | :--- |
| `--accent` | `#e21b5a` | Primary Pink brand theme color; used for primary buttons, highlights, badges, and key accents. |
| `--accent-dark` | `#b80d40` | Dark pink; used for hover states on primary buttons and links. |
| `--navy` | `#25344b` | Deep navy; used for primary layout headers, background shape styling, and text. |
| `--cyan` | `#2db8db` | Cyan accent; used for illustration graphics and floating iconography. |
| `--mint` | `#60c392` | Mint green; used for brand-specific gradients and indicators. |
| `--blue-soft` | `#fde8ef` | Soft pinkish tint; used for light accent backdrops. |
| `--primary-blue` | `#e21b5a` | Re-mapped to pink theme color (`--accent`) for B2B dashboard tokens. |
| `--primary-blue-hover` | `#b80d40` | Re-mapped to dark pink (`--accent-dark`) for B2B hover actions. |
| `--primary-green` | `#10b981` | Standard emerald green; used for verified badges and success pills/nodes. |
| `--white` | `#ffffff` | Pure white. |

### Slate Grayscale Tones
The design uses a defined spectrum of slate colors for typography hierarchy, dividers, and background planes:

*   `--slate-900`: `#25344b` (Mapped to deep navy)
*   `--slate-800`: `#24324b` (Deep text color / ink)
*   `--slate-700`: `#3a4b66` (Sub-headings and label texts)
*   `--slate-600`: `#4a5c77` (Muted interface details / borders)
*   `--slate-500`: `#6b7a99` (Secondary labels and placeholder colors)
*   `--slate-400`: `#8a94b0` (Disabled states / divider strokes)
*   `--slate-200`: `#e6e9f2` (Light grey borders)
*   `--slate-100`: `#f4f6fb` (Soft backgrounds / tab backdrops)
*   `--slate-50`: **Undefined in :root**, but used in styles.css as a background fallback. It applies to elements like table headers, stepper containers, table label columns, referral input boxes, and active suggestion dropdown options.

### Contextual Colors
*   `--bg`: `#ffffff` (Base body and application background)
*   `--bg-soft`: `#fcfcff` (Secondary body backgrounds)
*   `--bg-dashboard`: `#ffffff` (Dashboard background canvas)
*   `--paper`: `#ffffff` (Standard card and modal faces)
*   `--paper-strong`: `#fbfbff` (Strong card backdrops)
*   `--ink`: `#24324b` (Body text default)
*   `--ink-strong`: `#18263d` (Strong headings color)
*   `--muted`: `#78829b` (Muted paragraph details)
*   `--line`: `#e6e9f2` (Standard 1px layout boundaries)
*   `--line-strong`: `#d7dceb` (Stronger button/input borders)
*   `--shadow-sm` backdrop alpha: `rgba(0, 0, 0, 0.05)`
*   `--shadow-md` backdrop alpha: `rgba(32, 46, 77, 0.08)`
*   `--shadow-lg` backdrop alpha: `rgba(32, 46, 77, 0.1)`

### Gradients
The system features several linear and radial gradients utilized for visual panels:

1.  **Primary Brand Gradient (`--primary-gradient`)**: `linear-gradient(135deg, #25344b 0%, #2ba1fb 100%)`. Runs from deep navy (`#25344b`) to cyan-blue (`#2ba1fb`).
2.  **Hero Heading Highlight**: `linear-gradient(120deg, #e21b5a 0%, #ff6b8b 100%)`. Runs from primary pink (`#e21b5a`) to soft pink (`#ff6b8b`).
3.  **Video Banner Overlay**: `linear-gradient(135deg, rgba(30, 27, 75, 0.55) 0%, rgba(236, 72, 153, 0.55) 100%)`.
4.  **Reseller Banner Background**: `linear-gradient(180deg, #f0effa, #e6e6f3)`.
5.  **Reseller Card Floating Shape**: `linear-gradient(135deg, var(--accent), #6fc0fc)`.
6.  **Hero Section Background**: `linear-gradient(135deg, #ffffff 0%, #edf3fe 50%, #fdf0f4 100%)`.
7.  **Custom Solutions Banner**: `linear-gradient(135deg, #25344b 0%, #152030 100%)`.
8.  **Brand chip hover underline**: `linear-gradient(90deg, var(--accent), #6fc0fc)`.
9.  **Product Card Radial Brand Glows** (Glow maps located at the top center of card elements):
    *   **Zoho**: `radial-gradient(circle at top, rgba(96, 195, 146, 0.1) 0%, rgba(255, 255, 255, 0.9) 70%)` (Mint glow)
    *   **Microsoft**: `radial-gradient(circle at top, rgba(43, 161, 251, 0.06) 0%, rgba(255, 255, 255, 0.9) 70%)` (Blue glow)
    *   **Google**: `radial-gradient(circle at top, rgba(45, 184, 219, 0.08) 0%, rgba(255, 255, 255, 0.9) 70%)` (Cyan glow)
    *   **Intuit**: `radial-gradient(circle at top, rgba(16, 185, 129, 0.08) 0%, rgba(255, 255, 255, 0.9) 70%)` (Green glow)
    *   **Cisco & AWS**: `radial-gradient(circle at top, rgba(0, 82, 255, 0.06) 0%, rgba(255, 255, 255, 0.9) 70%)` (Deep blue glow)
    *   **OpenAI**: `radial-gradient(circle at top, rgba(16, 185, 129, 0.08) 0%, rgba(255, 255, 255, 0.9) 70%)` (Green glow)
    *   **Sophos**: `radial-gradient(circle at top, rgba(239, 68, 68, 0.05) 0%, rgba(255, 255, 255, 0.9) 70%)` (Red glow)

---

## 2. Typography

The design imports fonts dynamically from Google Fonts. Font stacks are configured as follows:

*   **Heading Font Family (`--font-heading`)**: `'Outfit', sans-serif`
*   **Body Font Family (`--font-body`)**: `'Inter', sans-serif`

### Font Scale & Weights
Hierarchy rules are established globally in [styles.css](file:///Users/shiyasahmad/.gemini/antigravity/scratch/technostore360/css/styles.css):

| Element / Class | Font Family | Size | Weight | Line Height / Letter Spacing |
| :--- | :--- | :--- | :--- | :--- |
| `body` | `Inter` | `1rem` (Inherited) | `400` | `1.5` |
| `h1, h2, h3, h4, h5, h6` | `Outfit` | Variable | `700` / `800` | Colors map to `var(--ink-strong)` |
| `.hero-title` | `Outfit` | `clamp(2.25rem, 4.2vw, 3.25rem)` | `800` | `1.15` / `-0.025em` |
| `.hero-desc` | `Inter` | `1rem` | `400` | `1.6` |
| `.section-kicker` | `Outfit` | `0.72rem` | `800` | `1.5` / `0.18em` (letter-spacing) |
| `.storemark__title` | `Outfit` | `1.5rem` | `800` | `0.95` |
| `.storemark__tag` | `Inter` | `0.65rem` | `500` | Default |
| `.masthead__nav-link` | `Inter` | `0.88rem` | `600` | Default |
| `.product-card-t360__title` | `Outfit` | `1.05rem` | `700` | `1.3` |
| `.product-card-t360__vendor` | `Inter` | `0.75rem` | `500` | Default |
| `.product-card-t360__price-value`| `Inter` | `0.95rem` | `800` | Default |
| `.product-card-t360__price-label`| `Inter` | `0.68rem` | `600` | Default |
| `.btn` | `Inter` | `0.875rem` | `600` | Default |
| `.btn-sm` | `Inter` | `0.75rem` | `600` | Default |
| `.form-label` | `Inter` | `0.8rem` | `600` | Default |
| `.form-input` / `.form-select` | `Inter` | `0.85rem` | `400` | Default |
| `.reseller-band__metric` | `Outfit` | `clamp(3.5rem, 5.5vw, 4.75rem)` | `800` | `1` / `-0.04em` (letter-spacing) |
| `.office-card__index` | `Outfit` | `1.25rem` | `800` | Default |
| `.office-card h5` | `Outfit` | `0.95rem` | `700` | Default |
| `.office-card p` | `Inter` | `0.8rem` | `400` | `1.5` |
| `.status-pill` / `.badge` | `Inter` | `0.7rem` | `600` | Default |

---

## 3. Layout & Structure

### Container Widths
The site implements a centered grid envelope using the `width` rules below:
```css
.utility-bar__inner, 
.masthead__inner, 
.category-bar__inner, 
.site-main, 
.techno-footer__inner {
  width: min(1320px, calc(100% - 40px));
  margin: 0 auto;
}
```
*   **Maximum Width**: `1320px`
*   **Padding Gutter**: `20px` on both left and right edges when viewport is narrower than 1360px (`calc(100% - 40px)`).

### Grid Layouts
*   **Homepage Category Grid (`.category-grid`)**: `display: grid`, `grid-template-columns: repeat(4, 1fr)`, `gap: 1.25rem`.
*   **Homepage Product Grid (`.product-grid`)**: `display: grid`, `grid-template-columns: repeat(4, 1fr)`, `gap: 1.25rem`.
*   **Listing Page Split Layout (`.listing-layout`)**: `display: grid`, `grid-template-columns: 260px 1fr`, `gap: 2rem`, `align-items: start`.
*   **Product Detail Split Layout (`.detail-layout`)**: `display: grid`, `grid-template-columns: 1fr 320px`, `gap: 2rem`, `align-items: start`.
*   **Authentication Split Container (`.auth-container`)**: `display: grid`, `grid-template-columns: 1fr 1fr`, `min-height: 480px`.
*   **Hero Grid (`.hero-section`)**: `display: grid`, `grid-template-columns: 52% 48%`, `gap: 2.5rem`.
*   **Footer Top Structure (`.techno-footer__top`)**: `display: grid`, `grid-template-columns: 1.3fr 1fr 1fr 1fr`, `gap: 2.5rem`.
*   **Footer Offices Grid (`.techno-footer__inner--offices`)**: `display: grid`, `grid-template-columns: repeat(3, minmax(0, 1fr))`, `gap: 2rem`.
*   **Double Column Form Grid (`.form-grid-2`)**: `display: grid`, `grid-template-columns: 1fr 1fr`, `gap: 1rem`.
*   **Step Selector Chip Grid (`.chip-grid`)**: `display: grid`, `grid-template-columns: repeat(3, 1fr)`, `gap: 0.75rem`.

---

## 4. Spacing & Gutters

Spacing relies on a rem-based utility system to ensure proportional margins and paddings:

### Standard Paddings
*   **Site Main Content Wrapper (`.site-main`)**: `3rem` top, `5rem` bottom.
*   **Hero Section (`.hero-section`)**: `70px` top and bottom, `80px` left and right.
*   **B2B Reseller Band (`.reseller-band`)**: `3.5rem` on all sides.
*   **Video Banner Box (`.video-banner-card`)**: `3rem` on all sides.
*   **B2B Standard Cards (`.product-card-t360`)**: `1.25rem` top and horizontal edges, `1.1rem` bottom.
*   **BuyMore Card (`.product-card-buymore`)**: `1.25rem` on all sides.
*   **Filter Sidebar (`.filter-sidebar`)**: `1.25rem` on all sides.
*   **Admin Dashboard Tables wrapper**: `0.85rem` vertical, `1.15rem` horizontal cell padding.
*   **Comparison Matrix Cell**: `1.25rem` padding on all sides.
*   **Stepper Frame Box (`.stepper-container`)**: `2rem` padding.
*   **Split Auth Form side**: `3rem` top/bottom, `2rem` left/right.
*   **Split Auth Banner side**: `2.5rem` padding on all sides (with `1rem` card margin spacing).
*   **Footer Top column block**: `3.5rem` top/bottom.
*   **Footer Offices row**: `2.5rem` top/bottom.
*   **Footer base copyright block**: `2rem` top, `3.5rem` bottom.
*   **Header Masthead padding**: `.9rem` top/bottom. Scrolled state transitions to `.55rem` top/bottom.

### Standard Margins
*   **Form groups spacing**: `margin-bottom: 1.25rem`.
*   **Product detail tabs margin**: `margin-bottom: 1.5rem`.
*   **Trust indicators margin**: `margin-bottom: 2rem`.
*   **Hero title layout spacing**: `margin-bottom: 0.5rem` (for kicker/desc).
*   **Product list divider line margin**: `margin-bottom: 0.5rem`.

---

## 5. Borders, Radius & Shadows

### Border Radius System
The system maps border-radius curves through variables and custom declarations:

```css
--radius-sm: 0.5rem;   /* 8px */
--radius-md: 0.85rem;  /* 13.6px */
--radius-lg: 1.5rem;   /* 24px */
--radius-full: 9999px; /* Pill / Circular */
```

*   **`--radius-sm` (8px)**: Used for `.form-input`, `.form-select`, `.form-textarea`, `.compare-selection-chip`.
*   **`--radius-md` (13.6px)**: Used for `.product-image-container`, `.pills-tabs`, `.chip-option`, `.search-suggestions-dropdown`.
*   **`--radius-lg` (24px)**: Used for `.card`, `.product-card-buymore`, `.video-banner-card`, `.filter-sidebar`, `.comparison-table-wrapper`, `.sticky-cta-card`, `.stepper-container`, `.dash-table-wrapper`, `.product-card-t360`, `.ai-banner-section`, `.case-study-card`, `.plan-selector-card`, `.auth-container`.
*   **`--radius-full` (9999px)**: Used for `.price-circle-badge`, `.round-action`, `.hamburger-button`, `.status-pill`, `.badge`, `#sidebar-toggle-btn`, `#back-to-top-btn`.
*   **Custom Radii**:
    *   **Hero Outer wrapper**: `border-radius: 32px`.
    *   **Reseller Outer banner**: `border-radius: 30px`.
    *   **Brand chip panel**: `border-radius: 16px`.
    *   **Product Card logo frame**: `border-radius: 16px`.
    *   **Search shell borders**: `border-radius: 14px`.
    *   **Trust highlights badges**: `border-radius: 10px`.
    *   **Product card buy button**: `border-radius: 10px`.
    *   **Thumb carousel frames**: `border-radius: 8px`.

### Borders System
*   **Standard Layout Border (`var(--line)`)**: `1px solid #e6e9f2`. Applied to masthead bottoms, category-bars, card divisions, specifications tables, AI banners, and case study borders.
*   **Strong Accent Border (`var(--line-strong)`)**: `1px solid #d7dceb`. Used on active outlines, utility pills, action buttons, search bar borders, and back-to-top buttons.
*   **Dashboard / Form Inputs Border**: `1px solid var(--slate-200)` (`#e6e9f2`). Used on textareas, selection fields, stepper components, table wrappers, comparison cells, quantity controls, and check chips.
*   **Active Brand Chip Underline Border**: `1.5px solid var(--line)`. Activates an active pink gradient line on hover/active states.

### Shadows System
```css
--shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.05);
--shadow-md: 0 14px 35px rgba(32, 46, 77, 0.08);
--shadow-lg: 0 24px 60px rgba(32, 46, 77, 0.1);
```

*   **`--shadow-sm`**: Used on normal product cards, search shells, brand panels, detail tab selectors, and check indicators.
*   **`--shadow-md`**: Used on sticky cards, comparison selectors, reseller bands, back-to-top controls, and card hover states.
*   **`--shadow-lg`**: Used on card hover focus states, dropdowns, and toast messages.
*   **Custom Shadows**:
    *   **Hero container shadow**: `0 20px 50px rgba(37, 52, 75, 0.04)`.
    *   **Trusted strip shadow**: `0 15px 45px rgba(37, 52, 75, 0.03)`.
    *   **Floating badges shadow**: `0 8px 25px rgba(37, 52, 75, 0.06)`.

---

## 6. Global Header & Navigation Menu

The header consists of two main sections: a utility bar (which is hidden in CSS) and a sticky masthead.

### 1. Utility Bar
*   **HTML Structure**: Top utility bar containing language picker, currency selectors, "Become a Partner" and "Workspace Portal" links.
*   **Implementation Status**: Hidden globally via CSS:
    ```css
    .utility-bar {
      display: none !important;
    }
    ```

### 2. Sticky Masthead (`.masthead`)
*   **Background**: Initially `#fffffff2` with a `1px solid var(--line)` border.
*   **Sticky Position**: Affixed at `top: 0` with a `z-index: 100`.
*   **State Shift (`.scrolled`)**: Triggered via scroll event listener. Adds backdrop blur, reduces padding, and updates the background color:
    ```css
    .masthead.scrolled {
      background: rgba(255, 255, 255, 0.85) !important;
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      box-shadow: 0 4px 20px rgba(37, 52, 75, 0.04);
      border-bottom-color: rgba(230, 233, 242, 0.5);
    }
    .masthead.scrolled .masthead__inner {
      padding: 0.55rem 0 !important;
    }
    ```
*   **Inner Layout Grid**: `.masthead__inner` uses grid layouts with columns: `auto 1fr auto` (Branding, Navigation, Actions).

### 3. Logo Branding (`.storemark`)
*   **Title**: `TECHNOSTORE360` stacked vertically in Outfit font (`#1d2a5e`). The "360" portion is colored with `--accent` (`#e21b5a`).
*   **Sub-tag**: "Empowering Diversity in Tech" in Inter font (`#78829b`) at `0.65rem`.

### 4. Navigation Menu
*   **Desktop Navigation**: Hidden on viewports below `991px` (`.desktop-only`).
*   **Navigation Links**: Configured with a relative positioning structure that activates a sliding underline animation on hover:
    ```css
    .masthead__nav-link::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 2px;
      background-color: var(--accent);
      transform: scaleX(0);
      transform-origin: right;
      transition: transform 0.25s cubic-bezier(0.25, 1, 0.5, 1);
    }
    .masthead__nav-link:hover::after {
      transform: scaleX(1);
      transform-origin: left;
    }
    ```

### 5. Header Actions
*   **Search Trigger**: Button containing a search icon, routing directly to the `#listing` page.
*   **Country Selector Button**: Contains a globe icon, label ("India"), and a chevron down icon.
*   **Sign-in Button**: Styled as a pill button with a user icon, linking to `#login`.
*   **Demo Request CTA**: A solid pink button (`.header-demo-btn`) linking to `#demo`.
*   **Mobile Hamburger Toggler**: Activates below `991px`. Made of 3 lines that animate into an 'X' using CSS transitions when clicked.
*   **Mobile Navigation Drawer (`.mobile-nav`)**: Displays vertical link lists with a slide-down animation controlled via `max-height` transitions:
    ```css
    .mobile-nav {
      display: block !important;
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.35s cubic-bezier(0.25, 1, 0.5, 1);
    }
    .mobile-nav.active {
      max-height: 85vh !important;
      overflow-y: auto;
    }
    ```

---

## 7. Hero Section Structure

The hero section features a dual-column layout containing a text copy block on the left and a visual graphics container on the right.

### 1. Left Copy Area
*   **Kicker Badge (`.hero-kicker-badge`)**: Pill badge containing check icon and text "Find, Compare & Choose". Styled with light pink background (`rgba(226, 27, 90, 0.07)`), pink text (`#e21b5a`), and 1px border.
*   **Heading Title (`.hero-title`)**: outfit font (`#18263d`) with a nested span (`.highlight-pink`) displaying the pink text gradient.
*   **Description Paragraph (`.hero-desc`)**: Inter font (`#78829b`) at `1rem` with `1.6` line-height.
*   **Pill Search Bar (`.hero-search-shell`)**: Includes a category dropdown picker, vertical spacer divider, text input box, and a circular pink action submit button.
*   **Benefits Strip (`.hero-benefits-strip`)**: Features 3 benefit nodes divided by 1px vertical borders:
    *   *Node 1 (Trusted Brands)*: Features a pink background circle (`rgba(226, 27, 90, 0.08)`) with a pink icon.
    *   *Node 2 (Secure Procurement)*: Features a blue background circle (`rgba(43, 161, 251, 0.08)`) with a blue icon.
    *   *Node 3 (Expert Guidance)*: Features a pink background circle with a pink icon.

### 2. Right Visual Graphics Area
*   **Shapes Layer**:
    *   *Pink Glow Circle*: Located top right with a slow pulse animation.
    *   *Blue Glow Circle*: Located bottom left with a slow pulse animation.
    *   *Navy Base Circle*: Deep navy (`#1a222e`) backdrop shape.
    *   *Pink Wire Circle*: A thin pink accent ring overlay.
    *   *Dotted Grid Pattern*: Dotted grid pattern backdrop.
*   **Main Visual Screen Stack (`.hero-illustration-stack`)**: Displays dynamic B2B website screenshots, overlaid with floating badges containing cloud, AI, and secure lock icons that float dynamically.

---

## 8. Interactive Buttons & Controls

Buttons are defined with a unified transition system.

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  cursor: pointer;
  transition: transform 0.2s cubic-bezier(0.25, 1, 0.5, 1), 
              background-color 0.2s ease, 
              box-shadow 0.2s ease, 
              border-color 0.2s ease;
  position: relative;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
```

### Button States & Variations

#### Primary Button (`.btn-primary`)
*   **Default State**: Background is `--primary-blue` (`#e21b5a`), text color is white.
*   **Hover State**: Background changes to `--primary-blue-hover` (`#b80d40`), shifts upward (`translateY(-2px)`), and displays `--shadow-sm`.
*   **Active State**: Resets translate position and scales down to `0.97` to simulate a click.

#### Secondary Button (`.btn-secondary`)
*   **Default State**: Background is `--slate-100` (`#f4f6fb`), text color is slate-700 (`#3a4b66`).
*   **Hover State**: Background changes to `--slate-200` (`#e6e9f2`), translates upward (`translateY(-2px)`), and displays `--shadow-sm`.

#### Outline Button (`.btn-outline`)
*   **Default State**: Background is transparent, border is `1px solid var(--slate-200)`, text color is slate-600 (`#4a5c77`).
*   **Hover State**: Border color and text change to `--primary-blue` (`#e21b5a`).

#### Card Buy Button (`.product-card-t360__btn`)
*   **Default State**: Background is `--accent` (`#e21b5a`), width `2.75rem`, height `2rem`, border-radius 10px. Contains a white SVG icon.
*   **Hover State**: Background turns to `--accent-dark` (`#b80d40`) and scales up by `1.05`.

#### Back to Top Control (`#back-to-top-btn`)
*   **Default State**: Positioned fixed at `bottom: 2rem`, `right: 2rem`, width/height `44px` circular, border-radius 50%, white background, 1px border. Hidden by default (`opacity: 0`, pointer-events disabled, `translateY(20px)`).
*   **Scrolled State (`.visible`)**: Becomes visible (`opacity: 1`, pointer-events enabled, `translateY(0)`).
*   **Hover State**: Background changes to `--accent` (`#e21b5a`), text icon changes to white, translates upward (`translateY(-3px)`), and rotates `-8deg`.

#### Left/Right Sliding Indicators
*   Buttons with arrow icons shift the arrow to the right on hover:
    ```css
    .btn:hover i[data-lucide="arrow-right"] {
      transform: translateX(4px);
    }
    ```

---

## 9. Card Components

Cards represent the core containers for data on both the homepage and listing pages:

### 1. Basic Card (`.card`)
*   **Layout**: `background-color: var(--white)`, `border-radius: var(--radius-lg)` (24px), `border: 1px solid var(--slate-200)`, `box-shadow: var(--shadow-sm)`.
*   **Hover Effect (`.card-hover:hover`)**:
    ```css
    .card-hover:hover {
      transform: translateY(-5px) !important;
      box-shadow: var(--shadow-lg) !important;
      border-color: rgba(236, 72, 153, 0.2);
    }
    ```

### 2. Homepage Category Card
*   Contains a top icon container with a background shape, a heading title, and a subtext description. On card hover, the icon container scales up and rotates slightly:
    ```css
    .card-hover:hover div i {
      transform: scale(1.1) rotate(4deg);
      color: var(--accent);
    }
    ```

### 3. TechnoStore B2B Product Card (`.product-card-t360`)
*   **Size**: Min-height `310px`, card layout structured with flex column alignment.
*   **Glow Backdrops**: Includes vendor-specific radial glows (as documented in the Colors section).
*   **Logo Wrapper**: `.product-card-t360__logo-container` features a white background, 1px border, and 16px radius. Contains a centered logo using `object-fit: contain`. The logo scales up on hover:
    ```css
    .product-card-t360:hover .product-card-t360__logo-container img {
      transform: scale(1.05);
    }
    ```
*   **Card Details**: Shows card title, category/vendor text in slate-500, a dividing rule (`.product-card-t360__divider`), and a footer containing pricing and the checkout action button.

### 4. BuyMore Product Card (`.product-card-buymore`)
*   **Size**: Min-height `440px`. Features a large image container (260px height) at the top, a circular price badge at the bottom right, color variant circles, and a compare button positioned top-right.

---

## 10. Forms & Input Fields

Forms feature floating transitions and validation layouts:

### Input Elements (`.form-input`, `.form-select`, `.form-textarea`)
*   **Styles**: Width `100%`, padding `0.65rem 0.85rem`, border `1px solid var(--slate-200)`, border-radius `--radius-sm` (8px), white background.
*   **Focus State**: Focus adds a pink border, outlines the element, and lifts the label:
    ```css
    .form-input:focus, .form-select:focus, .form-textarea:focus {
      border-color: var(--accent) !important;
      box-shadow: 0 0 0 3px rgba(226, 27, 90, 0.12) !important;
    }
    .form-group:focus-within .form-label {
      color: var(--accent) !important;
      transform: translateY(-1px);
    }
    ```

### Form Validation
*   **Invalid State (`.form-input.invalid`)**: Changes the input borders to pink and triggers a keyframe shake animation:
    ```css
    .form-input.invalid {
      border-color: var(--accent) !important;
      animation: invalidShakeAnim 0.4s ease;
    }
    @keyframes invalidShakeAnim {
      0%, 100% { transform: translateX(0); }
      20%, 60% { transform: translateX(-4px); }
      40%, 80% { transform: translateX(4px); }
    }
    ```

### Checkboxes & Radios
*   **Color**: Accent color set to `--accent` (`#e21b5a`).
*   **Interaction**: Scales down on press and pops outward when checked:
    ```css
    input[type="checkbox"]:active, input[type="radio"]:active {
      transform: scale(0.8);
    }
    input[type="checkbox"]:checked, input[type="radio"]:checked {
      transform: scale(1.1);
      animation: checkPop 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.5) forwards;
    }
    @keyframes checkPop {
      50% { transform: scale(1.2); }
    }
    ```

---

## 11. Footer Structure

The global footer is located in the `.techno-footer` block and features three main layout layers:

```
+-----------------------------------------------------------+
|                  techno-footer__top                       |
|  [Brand Info]    [Categories]    [Business]    [About]    |
+-----------------------------------------------------------+
|                techno-footer__offices                     |
|  [1. India Office]   [2. UAE Office]   [3. Oman Office]   |
+-----------------------------------------------------------+
|                  techno-footer__base                      |
|       [Accreditation Badges]    [Copyright Text]          |
+-----------------------------------------------------------+
```

### 1. Top Column Block (`.techno-footer__top`)
*   **Background**: Deep black (`#050505`).
*   **Columns**: Layout structured with 4 columns (`1.3fr 1fr 1fr 1fr`):
    *   *Column 1 (Brand Column)*: Contains the footer Storemark logo, primary support email, office street address, and social links in muted grey font.
    *   *Columns 2-4 (Category, Business, About Links)*: Structured with `1px solid rgba(255, 255, 255, 0.16)` left borders. Contains vertically stacked anchor menus. Links display with a slate-grey color overlay (`rgba(255, 255, 255, 0.7)`).

### 2. Offices Block (`.techno-footer__offices`)
*   **Background**: Darker black tone (`#0b0b0b`).
*   **Divider**: Divided from the top columns by a `1px solid rgba(255, 255, 255, 0.12)` border.
*   **Inner Layout**: Contains a 3-column grid mapping the global branches (India, UAE, Oman).
*   **Office Card**: Styled using a grid column template (`52px minmax(0, 1fr)`). Shows a large pink number index (`.office-card__index`) next to contact details.

### 3. Copyright Base Block (`.techno-footer__base`)
*   **Divider**: Divided from the office block by a `1px solid rgba(255, 255, 255, 0.12)` border.
*   **Accreditation Badges**: Features a row of trust badges (BBB Accredited, Norton Secured, Verified Business, Trusted Commerce) styled with a semi-transparent white background (`rgba(255, 255, 255, 0.08)`).
*   **Copyright Text**: Small grey font (`rgba(255, 255, 255, 0.45)`) positioned below the badges.

---

## 12. Media Queries & Responsive Breakpoints

The responsive system is managed using 6 media queries:

### 1. Screen Width: 1280px (`max-width: 1280px`)
*   **Listing Grid**: Drops from 4 columns to 3 columns.
    ```css
    @media (max-width: 1280px) {
      .product-grid {
        grid-template-columns: repeat(3, 1fr);
      }
    }
    ```

### 2. Screen Width: 1024px (`max-width: 1024px`)
*   **Sidebar Filter Panel**: Left sidebar is hidden off-screen (`transform: translateX(-100%)`) and transitions in when toggled.
*   **Sidebar Toggle Trigger**: Displays a circular floating action button (`#sidebar-toggle-btn`).
*   **Category Grid**: Drops from 4 columns to 3 columns.
*   **Listing Page Split**: Collapses from a 2-column split to a single stacked layout.

### 3. Screen Width: 991px (`max-width: 991px`)
*   **Header Navigation Menu**: Desktop-only nav items are hidden (`display: none !important`).
*   **Mobile Hamburger Toggler**: Displays the mobile hamburger menu icon.
*   **Hero Grid**: Collapses to a single column. The visual graphics layer stacks below the copy.

### 4. Screen Width: 768px / 769px (`max-width: 768px`)
*   **Product & Category Grids**: Drops to 2 columns.
*   **Double Column Form Grid**: Collapses to single-column input layout.
*   **Authentication Split**: Collapses to single-column auth form; marketing side hides.
*   **Video Banner**: Padding is reduced and the heading font size scales down to `1.5rem`.

### 5. Screen Width: 576px (`max-width: 576px`)
*   **Hero Benefits Strip**: Collapses from a horizontal layout to a stacked vertical alignment.
*   **Benefits Divider Line**: Hidden.

### 6. Screen Width: 480px (`max-width: 480px`)
*   **Product & Category Grids**: Collapses to a single column.
*   **Hero Search Bar**: Dropdown selector and vertical divider are hidden to fit mobile screens.

---

## 13. Hover Effects, Transitions & Animations

The system utilizes transition variables and keyframe animations:

### Transitions
*   **Standard Transition (`--transition-all`)**: `all 0.2s ease-in-out`. Applied to buttons, category highlights, cards, text overlays, and chevrons.
*   **Mobile Nav Drawer Transition**: `max-height 0.35s cubic-bezier(0.25, 1, 0.5, 1)`.

### Animations

#### 1. Page Entrance Transition
Transitions the container on hash route changes:
```css
#app-container {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.35s cubic-bezier(0.25, 1, 0.5, 1), 
              transform 0.35s cubic-bezier(0.25, 1, 0.5, 1);
}
#app-container.page-entering {
  opacity: 0;
  transform: translateY(12px);
  transition: none !important;
}
```

#### 2. Scroll Reveal Animations
Reveals elements sequentially on scroll using JS scroll detectors:
```css
.reveal-on-scroll {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.6s cubic-bezier(0.25, 1, 0.5, 1), 
              transform 0.6s cubic-bezier(0.25, 1, 0.5, 1);
}
.reveal-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}
```

#### 3. Floating Micro-animations
Three speed settings used on background shapes and floating cards in the hero section:
*   **`animate-float-slow`**: 6s duration, rotates 1deg.
*   **`animate-float-medium`**: 5s duration, rotates -1deg.
*   **`animate-float-fast`**: 4s duration, translates upward.

#### 4. Hero Pulse Glows
*   **Pink Pulse**: Translates `15px` right, `-10px` top, and scales up `1.1`.
*   **Blue Pulse**: Translates `-15px` left, `15px` bottom, and scales up `1.05`.

#### 5. Shimmer Loaders
Runs a continuous horizontal color sweep over skeleton layout blocks:
```css
@keyframes shimmerAnim {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

#### 6. Toast Alerts
*   **Success Alerts**: Slides up from bottom right and triggers checkmark rotation.
*   **Warning Alerts**: Triggers a pulse animation.
*   **Error Alerts**: Triggers a horizontal shake animation.

---

## 14. Page-by-Page Design Structure

The application functions as a Single Page Application (SPA) with routing managed by hash state transitions `#home`, `#listing`, `#detail`, `#compare`, `#packages`, `#demo`, `#reseller`, `#admin`, `#login`.

```
                  +-----------------------------------+
                  |            index.html             |
                  |  [Utility Bar]                    |
                  |  [Masthead]                       |
                  |      |                            |
                  |      v (Routes Hash)              |
                  |  [#app-container]                 |
                  |      |                            |
                  |      +---> #home                  |
                  |      +---> #listing               |
                  |      +---> #detail                |
                  |      +---> #compare               |
                  |      +---> #packages              |
                  |      +---> #demo                  |
                  |      +---> #reseller              |
                  |      +---> #admin                 |
                  |      +---> #login                 |
                  |      v                            |
                  |  [Global Footer]                  |
                  +-----------------------------------+
```

### 1. Homepage (`#home`)
*   **Grid layout**: Displays the hero banner card at the top, a horizontal marquee of trusted B2B logos, a 4-column category card grid, a horizontal brand filter strip, and a 4-column product grid.
*   **Highlight Elements**: Includes the AI Recommendations box and success story cards displaying B2B stats.

### 2. Product Catalog Listing (`#listing`)
*   **Grid Layout**: Split layout. Shows the sticky category sidebar on the left and catalog cards on the right.
*   **Interactive Details**: Displays active filter chips that can be clicked to clear filters, listing count indicators, and skeleton card loaders.

### 3. Product Details Page (`#detail`)
*   **Grid Layout**: Split layout. Shows the main product specifications and documentation on the left and a sticky buy panel on the right.
*   **Purchase Control Components**: Contains standard, professional, and enterprise tabs, a monthly/annual billing toggle, a user quantity adjuster, custom specs, and an accordion-style FAQ.
*   **Showcase Media Component**: Displays product screenshots with zoom-on-hover effects, an overlay play button for videos, a 360-rotation badge, and a thumbnail navigation carousel.

### 4. Product Comparison Screen (`#compare`)
*   **Layout**: Displays comparison cards at the top, a search selection list, and a detailed specifications matrix table.

### 5. Consolidated Solutions (`#packages`)
*   **Grid Layout**: Multi-column grid showcasing solution packages.
*   **Card Anatomy**: Displayed with a pink package header, sub-badge details, list of included services, pricing details, and an onboarding action button.

### 6. Booking / Quote Form (`#demo`)
*   **Layout**: Split layout. Shows the booking form on the left and B2B security/support benefits on the right.
*   **Success Indicator**: Submitting the form hides the inputs and fades in a centered checkmark overlay.

### 7. Reseller Portal (`#reseller`)
*   **Grid Layout**: Split layouts displaying referral margins, commission analytics cards, copy-to-clipboard referral links, payout method pickers, referral lead ledgers, and marketing download boxes.

### 8. Admin Dashboard (`#admin`)
*   **Layout**: Vertical tabbed navigation on the left, dashboard statistics cards on the top right, and data tables on the bottom right.
*   **Status Indicators**: Shows transaction ledger tables and status badges (Paid, Pending, Refunded).

### 9. Sign In Portal (`#login`)
*   **Layout**: Balanced double-column split container.
*   **Login Flow**: Displays role tabs (Buyer, Partner, Admin), credentials inputs, and a B2B SSO option on the left. The right column displays a pink-navy-blue gradient panel showcasing B2B portal security details.
