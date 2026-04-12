---
title: "Sileo"
source: "https://sileo.aaryan.design/docs/api/toaster"
---

[Sileo](/)

[GitHub](https://github.com/hiaaryan/sileo)[Docs](https://sileo.aaryan.design/docs/api/toaster/docs)[Playground](https://sileo.aaryan.design/docs/api/toaster/play)

[Kickstart](https://sileo.aaryan.design/docs/api/toaster/docs)[sileo](https://sileo.aaryan.design/docs/api/toaster/docs/api)[Toaster](https://sileo.aaryan.design/docs/api/toaster/docs/api/toaster)[Styling](https://sileo.aaryan.design/docs/api/toaster/docs/styling)

Basics[Kickstart](https://sileo.aaryan.design/docs/api/toaster/docs)

API[sileo](https://sileo.aaryan.design/docs/api/toaster/docs/api)[Toaster](https://sileo.aaryan.design/docs/api/toaster/docs/api/toaster)

Guides[Styling](https://sileo.aaryan.design/docs/api/toaster/docs/styling)

# Toaster

The viewport component that renders toasts. Add it once to your layout.

```
import { Toaster } from "sileo";

```

| Prop     | Type                  | Default     | Description                             |                                                                                 |
| -------- | --------------------- | ----------- | --------------------------------------- | ------------------------------------------------------------------------------- |
| children | ReactNode             | —           | App content to render alongside toasts  |                                                                                 |
| position | SileoPosition         | "top-right" | Default position for all toasts         |                                                                                 |
| offset   | number \| string      | object      | —                                       | Distance from viewport edges                                                    |
| options  | Partial<SileoOptions> | —           | Default options merged into every toast |                                                                                 |
| theme    | "light" \| "dark"     | "system"    | —                                       | Automatically sets fill based on color scheme. system follows the OS preference |

## Offset

The `offset` prop accepts a number, string, or per-side config.

```
<Toaster offset={20} />

<Toaster offset={{ top: 20, right: 16 }} />

```

## Default Options

Set global defaults that apply to every toast.

```
<Toaster
  options={{
    fill: "#171717",
    styles: { description: "text-white/75!" },
  }}
/>

```

---

## `SileoPosition`

```
type SileoPosition =
  | "top-left"
  | "top-center"
  | "top-right"
  | "bottom-left"
  | "bottom-center"
  | "bottom-right";

```

Sileo — MIT License[Playground →](https://sileo.aaryan.design/docs/api/toaster/play)