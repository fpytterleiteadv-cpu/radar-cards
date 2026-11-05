import asyncio, json, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).parent
FONTS = (ROOT.parent / "fonts" / "node_modules" / "@fontsource").as_uri()
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

POSTS = [
    {
        "id": "01", "tag": "O PRAZO",
        "hook": "Sua escala tem data para quebrar: <em>16 de dezembro.</em>",
        "kicker": "A 6x1 acaba. A jornada normal cai de 44 para 42 horas e cada empregado passa a ter duas folgas remuneradas por semana.",
        "body": [
            "Salário não reduz. As folgas não precisam ser sábado e domingo, nem seguidas.",
            "Para a empresa, o prazo real é <b>15 de dezembro</b>: no dia 16 a escala nova já tem que estar rodando no ponto e na folha.",
            "Em dezembro de 2027, o teto cai para 40 horas. Quem planeja só a primeira etapa refaz tudo em um ano.",
        ],
        "cta": "Quer saber se a sua escala fecha a tempo? Me chama.",
    },
    {
        "id": "02", "tag": "OS 24 MINUTOS",
        "hook": "42 horas em 5 dias dá <em>8h24</em> por dia. O limite continua sendo 8.",
        "kicker": "Esses 24 minutos só viram jornada normal com convenção ou acordo coletivo compatível.",
        "body": [
            "Sem instrumento coletivo, sobram duas saídas: antecipar as 40 horas agora ou pagar hora extra todo dia.",
            "A segunda não é solução, é passivo: hora extra habitual reflete em férias, 13º, FGTS e rescisão.",
            "Acordo individual não transforma os 24 minutos em jornada normal.",
        ],
        "cta": "Eu verifico se a sua CCT autoriza ou não.",
    },
    {
        "id": "03", "tag": "O FALSO 5x2",
        "hook": "Já trabalha de segunda a sexta? <em>Ainda não está adequado.</em>",
        "kicker": "44 horas em 5 dias é 8h48 por dia. Em dezembro isso deixa de ser jornada normal.",
        "body": [
            "Vai ter que escolher: reduzir para 8 horas e antecipar as 40, ou negociar instrumento coletivo para 8h24 na transição.",
            "Estar no 5x2 não é o mesmo que cumprir a regra. A pergunta é quantas horas as pessoas realmente trabalham por dia.",
        ],
        "cta": "Me manda a sua escala atual que eu digo em qual cenário você está.",
    },
    {
        "id": "04", "tag": "A FOLGA COMPRADA",
        "hook": "Pagar em dobro <em>não compra</em> a segunda folga.",
        "kicker": "Emergência acontece: o empregado trabalhou na folga, a empresa devolve outra.",
        "body": [
            "Sem devolver, paga em dobro. Mas se isso se repete toda semana, não é emergência — é escala mal dimensionada, e o passivo cresce a cada semana.",
            "Folga pode ser remanejada. Não pode ser eliminada e trocada por dinheiro de forma permanente.",
        ],
        "cta": "Ajudo seu RH a montar o revezamento que fecha.",
    },
    {
        "id": "05", "tag": "A CCT ANTIGA",
        "hook": "Sua convenção foi escrita para 44 horas. <em>Ela não vai te proteger.</em>",
        "kicker": "Cláusulas de 8h48, compensação de sábado e uma folga só perdem efeito em dezembro.",
        "body": [
            "CCT vigente não é CCT compatível. E CCT omissa não autoriza 8h24 automaticamente.",
            "Banco de horas e limite genérico de 10 horas diárias também não resolvem, sozinhos, a jornada de transição.",
        ],
        "cta": "Eu faço a auditoria das cláusulas que ficam e das que caem.",
    },
    {
        "id": "06", "tag": "A EQUIPE QUE ENCOLHE",
        "hook": "A mesma equipe vai entregar <em>40 horas a menos</em> por semana.",
        "kicker": "Dez pessoas: 440 horas hoje, 420 em dezembro, 400 em 2027.",
        "body": [
            "Se a conta já fecha no limite, não fecha: férias, faltas, intervalos e pico não cabem.",
            "Não significa contratar automaticamente. Significa descobrir em que dia, horário e função as horas vão faltar.",
            "Uma hora administrativa na segunda não substitui uma hora de atendimento no domingo.",
        ],
        "cta": "Calculo a cobertura da sua operação com margem.",
    },
    {
        "id": "07", "tag": "O GERENTE SEM PONTO",
        "hook": "Seu “gerente” trabalha das 10h às 22h sem ponto. <em>Ele não é gerente.</em>",
        "kicker": "Cargo de confiança exige poder real de gestão, autonomia e salário compatível.",
        "body": [
            "Sem isso, o enquadramento cai e a jornada inteira é apurada — com horas extras, intervalos e repousos.",
            "E mesmo o gerente de verdade mantém o direito às duas folgas. Cargo de confiança dispensa o ponto; não dispensa o descanso.",
        ],
        "cta": "Reviso o enquadramento dos seus cargos de confiança.",
    },
    {
        "id": "08", "tag": "O ERRO DE COMEÇAR PELO PONTO",
        "hook": "Mudar o sistema de ponto não adequa a empresa. <em>Só registra o erro mais rápido.</em>",
        "kicker": "A ordem é outra: mapear, simular, decidir, formalizar — e só então parametrizar.",
        "body": [
            "1. Mapear a escala real, não a do contrato.<br>2. Calcular quantas horas a operação precisa.<br>3. Ler a CCT.<br>4. Decidir: 40 ou 42 horas.<br>5. Formalizar instrumentos e políticas.<br>6. Só então ajustar ponto e folha.",
            "O ponto registra a decisão. Não toma a decisão pela empresa.",
        ],
        "cta": "Eu conduzo esse diagnóstico com o seu RH antes do dia 15.",
    },
]

CSS = f"""
@font-face {{ font-family:'Cormorant'; src:url('{FONTS}/cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2'); font-weight:500; }}
@font-face {{ font-family:'Cormorant'; src:url('{FONTS}/cormorant-garamond/files/cormorant-garamond-latin-600-normal.woff2'); font-weight:600; }}
@font-face {{ font-family:'Cormorant'; src:url('{FONTS}/cormorant-garamond/files/cormorant-garamond-latin-600-italic.woff2'); font-weight:600; font-style:italic; }}
@font-face {{ font-family:'Manrope'; src:url('{FONTS}/manrope/files/manrope-latin-400-normal.woff2'); font-weight:400; }}
@font-face {{ font-family:'Manrope'; src:url('{FONTS}/manrope/files/manrope-latin-500-normal.woff2'); font-weight:500; }}
@font-face {{ font-family:'Manrope'; src:url('{FONTS}/manrope/files/manrope-latin-600-normal.woff2'); font-weight:600; }}
@font-face {{ font-family:'Manrope'; src:url('{FONTS}/manrope/files/manrope-latin-700-normal.woff2'); font-weight:700; }}
:root {{ --navy:#0D1F33; --gold:#B8894A; --cream:#EBE7DB; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html,body {{ width:1080px; height:1350px; }}
body {{ font-family:'Manrope',sans-serif; -webkit-font-smoothing:antialiased; }}
.card {{ position:relative; width:1080px; height:1350px; padding:84px 84px 76px; display:flex; flex-direction:column; overflow:hidden; }}
.c1 {{ background:var(--navy); color:var(--cream); }}
.c2 {{ background:var(--cream); color:var(--navy); }}
.top {{ display:flex; justify-content:space-between; align-items:flex-start; font-size:21px; letter-spacing:.22em; text-transform:uppercase; font-weight:600; }}
.c1 .top {{ color:var(--gold); }}
.c2 .top {{ color:var(--gold); }}
.top .n {{ font-family:'Cormorant'; font-size:34px; letter-spacing:.05em; font-weight:600; }}
.c2 .top .n {{ color:var(--navy); }}
.rule {{ width:120px; height:4px; background:var(--gold); margin:48px 0 40px; }}
.tag {{ font-size:22px; letter-spacing:.28em; text-transform:uppercase; font-weight:700; color:var(--gold); margin-bottom:34px; }}
.hook {{ font-family:'Cormorant'; font-weight:500; font-size:104px; line-height:1.02; letter-spacing:-.012em; }}
.hook em {{ font-style:italic; font-weight:600; color:var(--gold); }}
.c1 .mid {{ flex:1; display:flex; flex-direction:column; justify-content:center; }}
.c1 .kicker {{ margin-top:56px; font-size:30px; line-height:1.45; font-weight:400; color:rgba(235,231,219,.82); max-width:820px; }}
.c2 .mid {{ flex:1; }}
.c2 .hook2 {{ font-family:'Cormorant'; font-weight:600; font-size:66px; line-height:1.08; max-width:900px; }}
.c2 .hook2 em {{ font-style:italic; color:var(--gold); }}
.c2 .kicker {{ margin-top:34px; font-size:31px; line-height:1.4; font-weight:600; color:var(--navy); max-width:880px; }}
.c2 .body p {{ margin-top:30px; font-size:28px; line-height:1.5; font-weight:400; color:rgba(13,31,51,.86); max-width:880px; }}
.c2 .body b {{ font-weight:700; color:var(--navy); }}
.cta {{ margin-top:auto; background:var(--navy); color:var(--cream); padding:40px 48px; display:flex; gap:36px; align-items:center; }}
.cta .arrow {{ font-family:'Cormorant'; font-size:72px; line-height:1; color:var(--gold); font-weight:600; }}
.cta .t {{ font-size:30px; line-height:1.35; font-weight:600; }}
.cta .w {{ font-size:22px; font-weight:500; color:var(--gold); margin-top:12px; letter-spacing:.04em; }}
.foot {{ margin-top:44px; display:flex; justify-content:space-between; align-items:flex-end; }}
.foot .brand {{ font-family:'Cormorant'; font-size:34px; font-weight:600; letter-spacing:.02em; }}
.foot .sub {{ font-size:19px; letter-spacing:.2em; text-transform:uppercase; font-weight:600; color:var(--gold); margin-top:6px; }}
.foot .ig {{ font-size:22px; font-weight:600; letter-spacing:.06em; }}
.c1 .foot .ig {{ color:rgba(235,231,219,.75); }}
.c1 .swipe {{ position:absolute; right:84px; bottom:76px; font-size:21px; letter-spacing:.22em; text-transform:uppercase; font-weight:600; color:var(--gold); }}
.c1 .foot .ig {{ display:none; }}
.grid {{ position:absolute; right:-140px; top:230px; width:520px; height:520px; border:1px solid rgba(184,137,74,.28); border-radius:50%; }}
.grid2 {{ position:absolute; right:-40px; top:330px; width:320px; height:320px; border:1px solid rgba(184,137,74,.22); border-radius:50%; }}
.c2 .bar {{ position:absolute; left:0; top:0; width:18px; height:1350px; background:var(--navy); }}
.c2 .card-in {{ }}
"""

def card1(p):
    return f"""<html><head><style>{CSS}</style></head><body>
<div class="card c1">
  <div class="grid"></div><div class="grid2"></div>
  <div class="top"><span>Fim da 6x1 · EC 141/2026</span><span class="n">{p['id']} / 08</span></div>
  <div class="mid">
    <div class="tag">{p['tag']}</div>
    <div class="hook">{p['hook']}</div>
    <div class="rule"></div>
    <div class="kicker">{p['kicker']}</div>
  </div>
  <div class="foot">
    <div><div class="brand">Francisco Pytter</div><div class="sub">Advocacia Empresarial</div></div>
  </div>
  <div class="swipe">Arraste →</div>
</div></body></html>"""

def card2(p):
    body = "".join(f"<p>{b}</p>" for b in p["body"])
    return f"""<html><head><style>{CSS}</style></head><body>
<div class="card c2">
  <div class="bar"></div>
  <div class="top"><span>Fim da 6x1 · EC 141/2026</span><span class="n">{p['id']} / 08</span></div>
  <div class="mid">
    <div class="rule" style="margin:48px 0 32px"></div>
    <div class="hook2">{p['hook']}</div>
    <div class="kicker">{p['kicker']}</div>
    <div class="body">{body}</div>
  </div>
  <div class="cta"><div class="arrow">→</div><div><div class="t">{p['cta']}</div><div class="w">WhatsApp (96) 99103-1818 · @fpytter</div></div></div>
  <div class="foot">
    <div><div class="brand">Francisco Pytter</div><div class="sub">Advocacia Empresarial</div></div>
    <div class="ig">franciscopytteradvocacia.com</div>
  </div>
</div></body></html>"""

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width":1080,"height":1350}, device_scale_factor=1)
        for p in POSTS:
            for k, html in (("1", card1(p)), ("2", card2(p))):
                f = ROOT / f"p{p['id']}_c{k}.html"; f.write_text(html)
                await pg.goto(f.as_uri()); await pg.wait_for_timeout(250)
                await pg.screenshot(path=str(OUT / f"post{p['id']}_card{k}.png"), full_page=False)
        await b.close()
    (ROOT / "posts.json").write_text(json.dumps(POSTS, ensure_ascii=False, indent=1))

asyncio.run(main())
