import type { DocsThemeConfig } from 'nextra-theme-docs'

const config: DocsThemeConfig = {
  logo: <strong>Agentic Engineering</strong>,
  project: {
    link: 'https://github.com/lmist/hitch',
  },
  docsRepositoryBase: 'https://github.com/lmist/hitch/tree/main/site',
  footer: {
    content: 'The Hitchhiker\u2019s Guide to Agentic Engineering',
  },
  sidebar: {
    defaultMenuCollapseLevel: 1,
    toggleButton: true,
  },
  toc: {
    float: true,
  },
  color: {
    hue: 358,
    saturation: 52,
  },
  darkMode: true,
  nextThemes: {
    defaultTheme: 'dark',
  },
}

export default config
