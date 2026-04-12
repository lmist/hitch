---
title: "Sileo"
source: "https://sileo.aaryan.design/docs/api"
---

[Sileo](/)

[GitHub](https://github.com/hiaaryan/sileo)[Docs](https://sileo.aaryan.design/docs/api/docs)[Playground](https://sileo.aaryan.design/docs/api/play)

[Kickstart](https://sileo.aaryan.design/docs/api/docs)[sileo](https://sileo.aaryan.design/docs/api/docs/api)[Toaster](https://sileo.aaryan.design/docs/api/docs/api/toaster)[Styling](https://sileo.aaryan.design/docs/api/docs/styling)

Basics[Kickstart](https://sileo.aaryan.design/docs/api/docs)

API[sileo](https://sileo.aaryan.design/docs/api/docs/api)[Toaster](https://sileo.aaryan.design/docs/api/docs/api/toaster)

Guides[Styling](https://sileo.aaryan.design/docs/api/docs/styling)

# sileo

The global toast controller. Import it anywhere to fire toasts.

```
import { sileo } from "sileo";

```

## Methods

| Method                       | Description                                            |
| ---------------------------- | ------------------------------------------------------ |
| sileo.success(options)       | Green success toast                                    |
| sileo.error(options)         | Red error toast                                        |
| sileo.warning(options)       | Amber warning toast                                    |
| sileo.info(options)          | Blue info toast                                        |
| sileo.action(options)        | Toast with an action button                            |
| sileo.show(options)          | Generic toast (defaults to success state)              |
| sileo.promise(promise, opts) | Loading → success/error flow                           |
| sileo.dismiss(id)            | Dismiss a specific toast by id                         |
| sileo.clear(position?)       | Clear all toasts, or only those at a specific position |

All shortcut methods return the toast `id` as a string. `promise` returns the original promise. `dismiss` and `clear` return void.

---

## `SileoOptions`

Passed to every `sileo.*()` method.

| Prop        | Type                | Default         | Description                             |
| ----------- | ------------------- | --------------- | --------------------------------------- |
| title       | string              | —               | Toast heading                           |
| description | ReactNode \| string | —               | Body content, supports JSX              |
| position    | SileoPosition       | Toaster default | Override position for this toast        |
| duration    | number \| null      | 6000            | Auto-dismiss ms. null = sticky          |
| icon        | ReactNode \| null   | State icon      | Custom icon in the badge                |
| fill        | string              | "#FFFFFF"       | SVG fill color for the toast background |
| styles      | SileoStyles         | —               | Class overrides for sub-elements        |
| roundness   | number              | 16              | Border radius in pixels                 |
| autopilot   | boolean \| object   | true            | Auto expand/collapse timing             |
| button      | SileoButton         | —               | Action button config                    |

---

## `SileoButton`

```
interface SileoButton {
  title: string;
  onClick: () => void;
}

```

---

## `SileoStyles`

Override classes for individual toast sub-elements.

```
interface SileoStyles {
  title?: string;
  description?: string;
  badge?: string;
  button?: string;
}

```

```
sileo.success({
  title: "Custom styled",
  fill: "black",
  styles: {
    title: "text-white!",
    description: "text-white/75!",
    badge: "bg-white/20!",
    button: "bg-white/10!",
  },
});

```

---

## `SileoPromiseOptions`

Passed as the second argument to `sileo.promise()`.

```
interface SileoPromiseOptions<T = unknown> {
  loading: SileoOptions;
  success: SileoOptions | ((data: T) => SileoOptions);
  error: SileoOptions | ((err: unknown) => SileoOptions);
  action?: SileoOptions | ((data: T) => SileoOptions);
  position?: SileoPosition;
}

```

The `success` and `error` fields can be static options or callbacks that receive the resolved/rejected value. The optional `action` field, when provided, replaces the success toast with an action state instead.

```
sileo.promise(createUser(data), {
  loading: { title: "Creating account..." },
  success: (user) => ({
    title: `Welcome, ${user.name}!`,
  }),
  error: (err) => ({
    title: "Signup failed",
    description: err.message,
  }),
});

```

Sileo — MIT License[Playground →](https://sileo.aaryan.design/docs/api/play)