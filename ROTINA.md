# Rotina "Radar de Notícias" → carrossel no Instagram

**Versão:** 1.0 · 03/11/2026 · Francisco Pytter Advocacia
**Origem:** `ROTINAS_DE_PESQUISA_DE_NOTICIAS_ULTIMAS_4_SEMANAS.md` (Radar Trabalhista Preventivo + Radar Empresarial, antes no ChatGPT)

## 1. Objetivo

Transformar a notícia jurídica/empresarial mais relevante do período em um carrossel de 2–3 cards para o @fpytter, ligando **fato → ganho de impacto e urgência → produto jurídico aplicável**, com aprovação humana apenas na arte final.

## 2. Decisões fixadas

| Item | Decisão |
|---|---|
| Formato | Carrossel de 2 a 3 cards (1080×1350). Card 1 em estilo manchete de portal (frame de notícia com domínio da fonte, editoria, headline, deck, fonte e data); card 2 impacto + risco; card 3 ação + CTA com produto. Com 2 cards, o 2º concentra impacto/risco + CTA. |
| Cadência | A cada 2 dias úteis. Exceção: notícia de alta demanda social/interesse publica no mesmo dia, mesmo fora da cadência. |
| Pesquisa | Automática, sem aprovação. Dias úteis às 06h44 (America/Belem). |
| Seleção | Automática, sem aprovação — critério: impacto financeiro × risco jurídico × utilidade preventiva × aderência ao posicionamento × potencial de conversão. |
| Aprovação | **Somente na arte final.** A rotina envia prévia (3 imagens + legenda) e aguarda "aprovar" / ajustes / "pular". Nada é publicado sem resposta. |
| Publicação | Windsor.ai → conector `instagram` (conta `fpytter`, id 17841402059490832) → ação `create_carousel_post` (`image_urls` + `caption`). Publicação imediata no momento da aprovação. |
| Hospedagem | GitHub público `fpytterleiteadv-cpu/radar-cards`, caminho `AAAA/MM/DD/card_N.jpg`, URL `raw.githubusercontent.com/.../main/...`. |
| Registro | Drive → FRANCISCO PYTTER ADVOCACIA → **Radar de Notícias** (id `15RDdA3L7C5gHEFADp7W8yhEv9DGuX71V`): um arquivo `edicao_AAAA-MM-DD.md` por execução (inclusive execuções sem pauta), com bloco técnico padronizado. Dedupe lê as últimas 10 edições. |
| Imagens | Sem print/foto de terceiros (rede do ambiente bloqueia download; marca/direito autoral do portal). Quando o usuário quiser foto, envia a imagem e ela entra como fundo do card 1. |

## 3. Fluxo da execução

1. **Dedupe:** listar as últimas 10 edições na pasta do Drive; extrair temas já publicados e data da última publicação.
2. **Pesquisa web (últimas 48–72h):** fontes oficiais primeiro — tst.jus.br, stj.jus.br, stf.jus.br, gov.br/trabalho-e-emprego, mpt.mp.br e PRTs, TRTs, rad.cvm.gov.br, PGFN, Câmara/Senado — depois Migalhas, Conjur, Valor, Folha, UOL Economia, Reuters Brasil, Agência Brasil. Duas frentes: trabalhista preventivo e empresarial/societário.
3. **Validação mínima:** data, órgão, processo/norma, status (liminar, sem trânsito, em apuração, PL em tramitação). Sem fonte primária localizável → pauta descartada.
4. **Decidir se publica hoje:** (a) última publicação há ≥ 2 dias úteis, ou (b) notícia de alta demanda social (repercussão nacional, números expressivos, afeta a maioria dos empregadores/empresários, prazo correndo). Caso contrário: só registra a edição, não gera card.
5. **Mapear produto** (catálogo FPL, `CATALOGO_PRODUTOS_JURIDICOS_FPL.md`):
   - Jornada, escala, 5x2, intervalos, ponto → **Sprint de Adequação à Escala 5x2** (enquanto houver campanha) ou **Raio-X Trabalhista Empresarial**
   - Assédio, lideranças, justa causa, demissões sensíveis, provas internas → **Raio-X Trabalhista Empresarial** (entrada) · **Academia Jurídica de Gestores** (treinamento) · **Blindagem Trabalhista** (implantação)
   - NR-1, SST, fiscalização MTE/MPT, terceirização, PcD → **Raio-X Trabalhista Empresarial** → **Blindagem Trabalhista**
   - Contratos, fornecedores, inadimplência, renovação → **Radar Contratual Empresarial** → **Arquitetura Contratual Empresarial**
   - Sócios, governança, dissolução, responsabilidade de administrador, RJ → **Diagnóstico de Maturidade Societária** → **Acordo de Sócios Estratégico** / **Governança Societária Essencial**
   - SaaS, dados, PI, plataformas → **SaaS/Tech Legal Readiness**
   - Recorrência/assessoria → **FPL Jurídico Contínuo**
6. **Redigir conteúdo** no JSON do gerador (sequência Fato → Impacto → Risco → Prevenção → CTA) + legenda (até 2.200 caracteres: gancho, 3 linhas de contexto, 3 bullets de ação, CTA, fonte, 5–8 hashtags).
7. **Gerar cards:** clonar `radar-cards`, `cd tools && npm install`, `node gerar_cards.js conteudo.json ../AAAA/MM/DD`, commit e push.
8. **Salvar edição no Drive** (`edicao_AAAA-MM-DD.md`) com conteúdo, legenda, URLs e bloco técnico.
9. **Enviar prévia e aguardar aprovação:** mensagem com as 3 imagens (URLs públicas), a legenda e três respostas possíveis: `aprovar` · `ajustar: <o que mudar>` · `pular`.
10. **Ao receber "aprovar":** `execute_action` Windsor `instagram` / `create_carousel_post` com as URLs em ordem e a legenda. Registrar `publicado_em` e link na edição do Drive.

## 4. Guardrails (OAB Prov. 205/2021 + posicionamento)

- Tom informativo, sóbrio, sem promessa de resultado, sem "risco zero", sem "ganhamos", sem linguagem de medo nem menção a prisão/cadeia como ameaça.
- Fonte primária creditada; status processual explícito; sem nome de cliente, valores de acordo ou caso identificável.
- "Blindagem" nunca como imunidade. Métrica institucional (R$ 500 mil evitados) no máximo uma vez por peça e só se fizer sentido.
- CTA direto, oferecendo auxílio pessoal ao RH/empresa ("eu ajudo seu RH a…"), com produto nomeado, WhatsApp (96) 99103-1818 e site.
- Sem pauta forte = sem post (registrar saída negativa).
- Assinatura: "Francisco Pytter — Advocacia Empresarial · @fpytter".

## 5. Bloco técnico por edição

```text
Data e hora da pesquisa:
Janela temporal consultada:
Consultas executadas:
Fontes oficiais verificadas:
Fontes secundárias verificadas:
Notícias encontradas / descartadas (motivo):
Duplicidades identificadas:
Pauta selecionada e critério (cadência | alta demanda):
Produto mapeado:
Cards gerados (URLs):
Status: aguardando aprovação | publicado (link) | pulado | sem pauta
```

## 6. Pendências

- Nomes de produto: o catálogo (31/10) usa "Raio-X Trabalhista Empresarial", "Radar Contratual" etc.; o posicionamento (01/10) usa "Diagnóstico e Blindagem Trabalhista", "Check-up Contratual", "Quick Start Jurídico". A rotina segue o **catálogo**; confirmar qual nomenclatura vai a público.
- Foto/print real no card 1: depende de o usuário fornecer a imagem.
- Avaliar após 2 semanas: taxa de aprovação, ajustes pedidos, encaminhamentos gerados.
