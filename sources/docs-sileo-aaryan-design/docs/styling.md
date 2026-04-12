---
title: "Sileo"
source: "https://sileo.aaryan.design/docs/styling"
---

[Sileo](/)

[GitHub](https://github.com/hiaaryan/sileo)[Docs](https://sileo.aaryan.design/docs/styling/docs)[Playground](https://sileo.aaryan.design/docs/styling/play)

[Kickstart](https://sileo.aaryan.design/docs/styling/docs)[sileo](https://sileo.aaryan.design/docs/styling/docs/api)[Toaster](https://sileo.aaryan.design/docs/styling/docs/api/toaster)[Styling](https://sileo.aaryan.design/docs/styling/docs/styling)

Basics[Kickstart](https://sileo.aaryan.design/docs/styling/docs)

API[sileo](https://sileo.aaryan.design/docs/styling/docs/api)[Toaster](https://sileo.aaryan.design/docs/styling/docs/api/toaster)

Guides[Styling](https://sileo.aaryan.design/docs/styling/docs/styling)

# Styling

Sileo is designed to look great out of the box. When you need to customize, there are a few escape hatches.

## Fill Color

The `fill` prop sets the SVG background color of the toast. The default is `"#FFFFFF"`. Set it to a dark color like `"#171717"` or `"black"` to create a dark toast — just make sure to pair it with light text via `styles`.

PreviewCode

Dark accentFull dark

## Style Overrides

The `styles` prop lets you override classes on individual sub-elements. Use Tailwind's `!` modifier to ensure specificity.

PreviewCode

Try it

### Available Keys

| Key         | Element                   | Selector                   |
| ----------- | ------------------------- | -------------------------- |
| title       | The heading text          | \[data-sileo-title\]       |
| description | The body/description area | \[data-sileo-description\] |
| badge       | The icon badge circle     | \[data-sileo-badge\]       |
| button      | The action button         | \[data-sileo-button\]      |

## Custom Icons

Pass any React node as the `icon` prop to replace the default state icon.

PreviewCode

Try it

## Custom Description

The `description` prop accepts JSX, so you can build rich toast content.

PreviewCode

Try it

You can use any layout — stack multiple elements, add icons, or use your own components.

PreviewCode

Rich content

## Roundness

Control the border radius with the `roundness` prop (default `16`). Set it lower for sharper corners or higher for a rounder pill shape.

PreviewCode

Sharp (12)Round (16)

> **Performance note:** Higher `roundness` values increase the SVG blur radius used for the gooey morph effect, which is more expensive to render. The recommended value is `16` for a good balance between aesthetics and performance.

## Autopilot

By default, toasts auto-expand after a short delay and collapse before dismissing. Control this with the `autopilot` prop.

* `autopilot: false` — disables auto expand/collapse entirely (hover to expand)
* `autopilot: { expand: ms, collapse: ms }` — custom timing for each phase

PreviewCode

DisabledCustom timing

## Dismissing Toasts

Use `sileo.dismiss(id)` to remove a specific toast, or `sileo.clear()` to remove all. You can also clear only toasts at a specific position.

PreviewCode

Fire toastDismiss itClear all

## Global Defaults

Use the `Toaster`'s `options` prop to set defaults for every toast. This is useful for applying a consistent dark theme across your app.

```
<Toaster
  position="top-right"
  options={{
    fill: "#171717",
    roundness: 16,
    styles: {
      title: "text-white!",
      description: "text-white/75!",
      badge: "bg-white/10!",
      button: "bg-white/10! hover:bg-white/15!",
    },
  }}
/>

```

## CSS Variables

Sileo exposes CSS custom properties you can override globally to change state colors, dimensions, or animation timing.

```
:root {
  /* State colors (oklch) */
  --sileo-state-success: oklch(0.723 0.219 142.136);
  --sileo-state-loading: oklch(0.556 0 0);
  --sileo-state-error: oklch(0.637 0.237 25.331);
  --sileo-state-warning: oklch(0.795 0.184 86.047);
  --sileo-state-info: oklch(0.685 0.169 237.323);
  --sileo-state-action: oklch(0.623 0.214 259.815);

  /* Dimensions */
  --sileo-width: 350px;
  --sileo-height: 40px;

  /* Animation */
  --sileo-duration: 600ms;
}

```

For example, to make all success toasts use a custom brand color:

```
:root {
  --sileo-state-success: oklch(0.7 0.2 200);
}

```

Sileo — MIT License[Playground →](https://sileo.aaryan.design/docs/styling/play)