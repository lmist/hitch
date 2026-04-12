---
title: "Sileo"
source: "https://sileo.aaryan.design/docs"
---

[Sileo](/)

[GitHub](https://github.com/hiaaryan/sileo)[Docs](https://sileo.aaryan.design/docs/docs)[Playground](https://sileo.aaryan.design/docs/play)

[Kickstart](https://sileo.aaryan.design/docs/docs)[sileo](https://sileo.aaryan.design/docs/docs/api)[Toaster](https://sileo.aaryan.design/docs/docs/api/toaster)[Styling](https://sileo.aaryan.design/docs/docs/styling)

Basics[Kickstart](https://sileo.aaryan.design/docs/docs)

API[sileo](https://sileo.aaryan.design/docs/docs/api)[Toaster](https://sileo.aaryan.design/docs/docs/api/toaster)

Guides[Styling](https://sileo.aaryan.design/docs/docs/styling)

# Getting Started

Sileo is a tiny, opinionated toast component for React. It uses gooey SVG morphing and spring physics to create buttery smooth notifications — beautiful by default, no configuration required.

## Installation

```
npm install sileo

```

## Quick Setup

Add the `Toaster` component to your app's root layout, then call `sileo` from anywhere.

```
import { sileo, Toaster } from "sileo";

export default function App() {
  return (
    <>
      <Toaster position="top-right" />
      <YourApp />
    </>
  );
}

```

## Fire a Toast

PreviewCode

SuccessErrorWarningInfo

## Action Toast

Toasts can include a button for user interaction.

PreviewCode

Try it

## Promise Toast

Chain loading, success, and error states from a single promise.

PreviewCode

Try it

The promise method returns the original promise, so you can chain further.

## Positions

Sileo supports six positions. Set it on the `Toaster` as a default, or override per-toast.

```
<Toaster position="top-right" />

sileo.success({
  title: "Saved",
  position: "bottom-center",
});

```

Available positions: `top-left`, `top-center`, `top-right`, `bottom-left`, `bottom-center`, `bottom-right`.

Sileo — MIT License[Playground →](https://sileo.aaryan.design/docs/play)