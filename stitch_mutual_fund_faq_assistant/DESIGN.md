---
name: Kinetic Ledger
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#444651'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#757682'
  outline-variant: '#c5c5d3'
  surface-tint: '#4059aa'
  primary: '#00236f'
  on-primary: '#ffffff'
  primary-container: '#1e3a8a'
  on-primary-container: '#90a8ff'
  inverse-primary: '#b6c4ff'
  secondary: '#006c49'
  on-secondary: '#ffffff'
  secondary-container: '#6cf8bb'
  on-secondary-container: '#00714d'
  tertiary: '#4b1c00'
  on-tertiary: '#ffffff'
  tertiary-container: '#6e2c00'
  on-tertiary-container: '#f39461'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dce1ff'
  primary-fixed-dim: '#b6c4ff'
  on-primary-fixed: '#00164e'
  on-primary-fixed-variant: '#264191'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffdbcb'
  tertiary-fixed-dim: '#ffb691'
  on-tertiary-fixed: '#341100'
  on-tertiary-fixed-variant: '#773205'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 24px
  margin: 32px
---

## Brand & Style

The brand personality is rooted in stability, precision, and forward-thinking financial stewardship. It targets users who value security over spectacle, requiring a user interface that feels both institutional and accessible.

The design style is **Corporate Modern with a Minimalist focus**. It leverages heavy whitespace and a restricted color palette to reduce cognitive load during complex financial tasks. The emotional response should be one of "calm confidence"—achieved through high-contrast typography, systematic alignment, and subtle tactile cues that signify reliability.

## Colors

The palette is anchored by **Deep Trust Blue**, used for primary actions, navigation headers, and brand-critical elements. **Emerald Green** serves as the secondary color, reserved strictly for positive financial growth, success states, and "Confirm" actions to reinforce a sense of prosperity and accuracy.

The background uses a subtle **Off-white** to reduce screen glare and distinguish the UI from standard white browser chrome. Grays are tiered carefully: darker grays for body text to ensure WCAG AAA compliance, and lighter grays for structural dividers.

## Typography

The design system utilizes **Inter** for all roles to maintain a cohesive, systematic appearance. Inter’s tall x-height and neutral character provide the necessary clarity for numerical data and fine-print financial disclosures.

Headlines use a tighter letter-spacing and heavier weights to create a sense of authority. Labels and captions use medium to semi-bold weights to ensure they remain legible at small scales, particularly in data-heavy tables or dashboard widgets.

## Layout & Spacing

This design system employs a **12-column fluid grid** for desktop and a **4-column grid** for mobile. The spacing rhythm is based on a **4px baseline**, ensuring all components align to a predictable mathematical scale.

- **Desktop (1280px+):** 32px outer margins, 24px gutters.
- **Tablet (768px - 1279px):** 24px outer margins, 16px gutters.
- **Mobile (Up to 767px):** 16px outer margins, 12px gutters.

Large cards and containers should utilize `lg` (24px) padding to maintain an airy, premium feel, while smaller interactive elements like input fields should use `md` (16px) horizontal padding.

## Elevation & Depth

Hierarchy is established through **Ambient Shadows** and **Tonal Layering**. Surfaces do not use "pure black" shadows; instead, they use a highly diffused Deep Trust Blue tint (`rgba(30, 58, 138, 0.08)`) to maintain color harmony.

- **Level 0 (Background):** #F9FAFB.
- **Level 1 (Cards/Containers):** White (#FFFFFF) with a 1px border (#E5E7EB).
- **Level 2 (Hover/Active):** White (#FFFFFF) with a soft 8px blur shadow.
- **Level 3 (Modals/Popovers):** White (#FFFFFF) with a 16px blur shadow and a 1px border.

Avoid using shadows on buttons; use solid color fills to denote primary actions and subtle grey borders for secondary actions.

## Shapes

The design system uses a **Rounded** language (Scale 2). This provides a friendly, modern touch without appearing overly "bubbly" or juvenile, maintaining a professional fintech aesthetic.

- **Small Components (Checkboxes, Tags):** 4px (Soft)
- **Medium Components (Buttons, Inputs, Chat Bubbles):** 8px (Rounded)
- **Large Components (Cards, Modals):** 16px (Rounded-LG)
- **Specialty Components (Pills):** Full height radius (9999px)

## Components

### Chat Bubbles
- **User:** Primary color background, white text. Aligned right. 8px rounded corners, with the bottom-right corner sharp (0px).
- **Support/System:** White background, 1px border (#E5E7EB), text-main color. Aligned left. 8px rounded corners, with the bottom-left corner sharp (0px).

### Pill Buttons
- **Style:** High-contrast, fully rounded ends.
- **Primary:** Deep Trust Blue fill, white text. No shadow.
- **Secondary:** Transparent fill, Deep Trust Blue 1px border and text.

### Input Fields
- **Default:** White background, 1px border (#E5E7EB), 8px rounded corners.
- **Focus:** 1px border (Deep Trust Blue) with a 2px outer "glow" using 10% opacity of the primary color.
- **Label:** `label-md` placed above the field with 4px spacing.

### Citation Cards
- **Style:** Level 1 elevation (White background, 1px border).
- **Content:** Uses a 4px left-accent border in Secondary color (Emerald Green) to indicate verified data or high-confidence citations.
- **Typography:** Uses `body-md` for description and `label-sm` for the source metadata.

### Checkboxes & Radio Buttons
- 4px corner radius for checkboxes; 100% for radios.
- **Checked state:** Deep Trust Blue fill with a white checkmark/dot.