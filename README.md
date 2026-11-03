# radar-cards

Imagens públicas dos carrosséis do **Radar de Notícias** — Francisco Pytter Advocacia (@fpytter).

- `AAAA/MM/DD/card_N.jpg` — cards publicados ou aguardando aprovação (1080×1350, JPEG).
- `tools/gerar_cards.js` — gerador do carrossel (HTML → JPEG via Playwright/Chromium).
- `tools/exemplo.json` — exemplo de conteúdo no formato esperado.

URL pública de cada imagem:
`https://raw.githubusercontent.com/fpytterleiteadv-cpu/radar-cards/main/AAAA/MM/DD/card_N.jpg`

## Gerar cards

```bash
cd tools && npm install --silent
node gerar_cards.js conteudo.json ../2026/11/03
```

Campos do JSON (ver `exemplo.json`): `radar`, `data`, `data_fonte`, `tag`, `bgword`, `kicker`, `manchete_html`, `lead`, `fonte`, `fonte_url`, `status`, `gancho_html`, `impacto_titulo`, `impactos[{t,p}]`, `risco`, `acao_titulo`, `acoes[]`, `produto`, `cta_titulo`, `cta_texto`, `n_cards` (2 ou 3).
