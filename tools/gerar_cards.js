// Gerador de carrossel "Radar de Notícias" — Francisco Pytter Advocacia
// Uso: node gerar_cards.js conteudo.json pasta_saida
// Requer: playwright (chromium) e @fontsource/cormorant-garamond + @fontsource/inter instalados ao lado.
// Saída: card_1.jpg, card_2.jpg, card_3.jpg (1080x1350, 4:5)

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const [,, jsonPath, outDir] = process.argv;
if (!jsonPath || !outDir) { console.error('uso: node gerar_cards.js conteudo.json pasta_saida'); process.exit(1); }
const c = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
fs.mkdirSync(outDir, { recursive: true });

const fontDir = (pkg) => path.join(__dirname, 'node_modules', '@fontsource', pkg, 'files');
const b64 = (p) => fs.readFileSync(p).toString('base64');
const font = (fam, pkg, file, w) =>
  `@font-face{font-family:'${fam}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(fontDir(pkg), file))}) format('woff2');}`;

const fonts = [
  font('Cormorant', 'cormorant-garamond', 'cormorant-garamond-latin-600-normal.woff2', 600),
  font('Cormorant', 'cormorant-garamond', 'cormorant-garamond-latin-700-normal.woff2', 700),
  font('Inter', 'inter', 'inter-latin-400-normal.woff2', 400),
  font('Inter', 'inter', 'inter-latin-500-normal.woff2', 500),
  font('Inter', 'inter', 'inter-latin-600-normal.woff2', 600),
  font('Inter', 'inter', 'inter-latin-700-normal.woff2', 700),
].join('\n');

const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

const css = `
${fonts}
:root{--navy:#0D1F33;--gold:#B8894A;--cream:#EBE7DB;--navy2:#132A45;--muted:rgba(235,231,219,.62);}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;background:var(--navy);color:var(--cream);font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased}
.card{position:relative;width:1080px;height:1350px;padding:88px 84px 76px;display:flex;flex-direction:column;overflow:hidden;background:
  radial-gradient(900px 700px at 110% -10%, rgba(184,137,74,.16), transparent 60%),
  linear-gradient(180deg,#0D1F33 0%,#0B1A2C 100%)}
.rail{position:absolute;left:0;top:0;bottom:0;width:10px;background:var(--gold)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(235,231,219,.035) 1px,transparent 1px);background-size:100% 54px;pointer-events:none}
.top{display:flex;justify-content:space-between;align-items:center;font-size:21px;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);font-weight:600}
.top .date{color:var(--muted);letter-spacing:.12em;font-weight:500}
.kicker{margin-top:70px;display:inline-flex;align-items:center;gap:14px;font-size:22px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--cream)}
.kicker:before{content:'';width:46px;height:3px;background:var(--gold)}
h1{font-family:'Cormorant',serif;font-weight:700;font-size:86px;line-height:1.02;margin-top:36px;letter-spacing:-.01em}
h1 em{font-style:normal;color:var(--gold)}
.lead{margin-top:40px;font-size:31px;line-height:1.42;color:rgba(235,231,219,.88);max-width:860px;font-weight:400}
.src{margin-top:auto;font-size:21px;color:var(--muted);line-height:1.4}
.src b{color:var(--cream);font-weight:600}
.foot{margin-top:34px;display:flex;justify-content:space-between;align-items:flex-end;border-top:1px solid rgba(235,231,219,.18);padding-top:28px}
.sig{font-family:'Cormorant',serif;font-size:34px;font-weight:600;line-height:1.1}
.sig small{display:block;font-family:'Inter',sans-serif;font-size:18px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);margin-top:8px;font-weight:600}
.swipe{font-size:20px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);font-weight:600}
.num{position:absolute;right:84px;bottom:76px;font-family:'Cormorant',serif;font-size:30px;color:var(--muted)}
/* card 2 */
h2{font-family:'Cormorant',serif;font-weight:700;font-size:70px;line-height:1.05;margin-top:28px}
.items{margin-top:44px;display:flex;flex-direction:column;gap:30px}
.it{display:grid;grid-template-columns:64px 1fr;gap:22px;align-items:start}
.it .n{font-family:'Cormorant',serif;font-size:58px;font-weight:700;color:var(--gold);line-height:.9}
.it h3{font-size:30px;font-weight:600;line-height:1.25}
.it p{margin-top:8px;font-size:25px;line-height:1.42;color:rgba(235,231,219,.78)}
.risk{margin-top:auto;background:rgba(184,137,74,.12);border-left:6px solid var(--gold);padding:28px 32px;font-size:27px;line-height:1.4}
.risk b{display:block;font-size:19px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);margin-bottom:10px}
/* card 3 */
.steps{margin-top:40px;display:flex;flex-direction:column;gap:22px}
.st{display:flex;gap:20px;align-items:flex-start;font-size:28px;line-height:1.38}
.st:before{content:'';flex:none;width:16px;height:16px;border:3px solid var(--gold);border-radius:3px;margin-top:12px}
.cta{margin-top:auto;background:var(--cream);color:var(--navy);padding:40px 44px;border-radius:6px}
.cta .p{font-size:19px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);font-weight:700}
.cta h4{font-family:'Cormorant',serif;font-size:50px;font-weight:700;line-height:1.05;margin-top:10px}
.cta p.t{font-size:26px;line-height:1.4;margin-top:16px;color:#1f2f44}
.cta .w{margin-top:22px;font-size:24px;font-weight:600;color:var(--navy)}
.cta .w span{color:var(--gold)}
`;

const foot = (n, total, swipe) => `
  <div class="foot">
    <div class="sig">Francisco Pytter<small>Advocacia Empresarial · @fpytter</small></div>
    <div class="swipe">${swipe ? 'deslize →' : ''}</div>
  </div>`;

// Card 1 — estilo "manchete de portal": frame de notícia sobre fundo navy
const cssNews = `
.bgword{position:absolute;right:-30px;top:120px;font-family:'Cormorant',serif;font-weight:700;font-size:420px;line-height:1;color:rgba(184,137,74,.07);letter-spacing:-.04em;user-select:none}
.tag{display:inline-flex;align-self:flex-start;align-items:center;gap:12px;background:var(--gold);color:var(--navy);font-weight:700;font-size:20px;letter-spacing:.2em;text-transform:uppercase;padding:12px 18px;margin-top:54px}
.tag:before{content:'';width:12px;height:12px;border-radius:50%;background:var(--navy)}
.news{position:relative;z-index:1;margin-top:34px;background:#F6F3EA;color:#101826;border-radius:10px;overflow:hidden;box-shadow:0 40px 80px rgba(0,0,0,.45)}
.bar{display:flex;align-items:center;gap:10px;padding:16px 22px;background:#E6E1D3;border-bottom:1px solid #d6d0bf}
.bar i{width:14px;height:14px;border-radius:50%;background:#c9c2ae;display:inline-block}
.bar .url{margin-left:14px;flex:1;background:#F6F3EA;border-radius:8px;padding:8px 14px;font-size:17px;color:#6b7280;font-family:'Inter',sans-serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nb{padding:40px 46px 42px}
.cat{font-size:18px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#9a2f2f}
.hl{font-family:'Inter',sans-serif;font-weight:700;font-size:54px;line-height:1.12;margin-top:16px;letter-spacing:-.015em;color:#0D1F33}
.hl em{font-style:normal;color:#9a2f2f}
.deck{margin-top:22px;font-size:26px;line-height:1.42;color:#3a4454}
.by{margin-top:28px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid #d6d0bf;padding-top:18px;font-size:18px;color:#6b7280}
.by b{color:#0D1F33;font-weight:600}
.hook{margin-top:auto;font-family:'Cormorant',serif;font-weight:600;font-size:52px;line-height:1.08;color:var(--cream)}
.hook em{font-style:normal;color:var(--gold)}
`;

const card1 = `
<style>${cssNews}</style>
<div class="card"><div class="rail"></div><div class="grid"></div>
  <div class="bgword">${esc(c.bgword || '!')}</div>
  <div class="top"><span>${esc(c.radar)}</span><span class="date">${esc(c.data)}</span></div>
  <div class="tag">${esc(c.tag || 'Notícia da semana')}</div>
  <div class="news">
    <div class="bar"><i></i><i></i><i></i><span class="url">${esc(c.fonte_url || c.fonte)}</span></div>
    <div class="nb">
      <div class="cat">${esc(c.kicker)}</div>
      <div class="hl">${c.manchete_html || c.titulo_html}</div>
      <p class="deck">${esc(c.lead)}</p>
      <div class="by"><span><b>Fonte:</b> ${esc(c.fonte)}${c.status ? ' · ' + esc(c.status) : ''}</span><span>${esc(c.data_fonte || c.data)}</span></div>
    </div>
  </div>
  <div class="hook">${c.gancho_html || ''}</div>
  ${foot(1, 3, true)}
</div>`;

const card2 = `
<div class="card"><div class="rail"></div><div class="grid"></div>
  <div class="top"><span>Impacto para a empresa</span><span class="date">${esc(c.data)}</span></div>
  <h2>${esc(c.impacto_titulo)}</h2>
  <div class="items">
    ${(c.impactos || []).slice(0, 3).map((it, i) => `
    <div class="it"><div class="n">0${i + 1}</div><div><h3>${esc(it.t)}</h3><p>${esc(it.p)}</p></div></div>`).join('')}
  </div>
  <div class="risk"><b>Risco se nada mudar</b>${esc(c.risco)}</div>
  ${foot(2, 3, true)}
</div>`;

const card3 = `
<div class="card"><div class="rail"></div><div class="grid"></div>
  <div class="top"><span>O que fazer agora</span><span class="date">${esc(c.data)}</span></div>
  <h2>${esc(c.acao_titulo)}</h2>
  <div class="steps">
    ${(c.acoes || []).slice(0, 4).map((a) => `<div class="st">${esc(a)}</div>`).join('')}
  </div>
  <div class="cta">
    <div class="p">${esc(c.produto)}</div>
    <h4>${esc(c.cta_titulo)}</h4>
    <p class="t">${esc(c.cta_texto)}</p>
    <div class="w">WhatsApp <span>(96) 99103-1818</span> · franciscopytteradvocacia.com</div>
  </div>
  ${foot(3, 3, false)}
</div>`;

const page = (body) => `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${body}</body></html>`;

(async () => {
  const browser = await chromium.launch();
  const pg = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  const cards = [card1, card2, card3].slice(0, c.n_cards || 3);
  for (let i = 0; i < cards.length; i++) {
    await pg.setContent(page(cards[i]), { waitUntil: 'load' });
    await pg.evaluate(() => document.fonts.ready);
    const out = path.join(outDir, `card_${i + 1}.jpg`);
    await pg.screenshot({ path: out, type: 'jpeg', quality: 92 });
    console.log(out);
  }
  await browser.close();
})();
