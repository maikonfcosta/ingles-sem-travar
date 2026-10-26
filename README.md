# Inglês sem travar

Painel de estudos B1 com 28 dias de atividades, 30 minutos por dia e foco em continuidade da fala.

Abra `index.html` no navegador. Não há instalação, build, fontes externas ou serviços necessários para visualizar o plano. Os exercícios usam sua série, gravador, cartões e IA de preferência.

- Quatro semanas com speaking, listening, reading e writing.
- Shadowing, revisão de expressões e checks semanais.
- Checklist e notas salvos no navegador; exportação/importação JSON.
- Impressão de todas as semanas com notas, mesmo com filtro ativo.

Use **Salvar em PDF** e escolha o destino **Salvar como PDF** no navegador. O PDF é estático; as interações pertencem ao HTML. Para transferir progresso entre o arquivo local e o site, exporte e importe o JSON. Não envie esse arquivo pessoal ao repositório.

## Validação

Com Python, Playwright e Chromium já disponíveis:

```sh
python checks/validate.py
```

Valida 28 dias de 30 minutos, persistência, filtro, importação/exportação e layout mobile. Gera captura e PDF em `artifacts/` (ignorado no Git).

## Publicação

Site estático na Vercel; `vercel --prod` publica o diretório. Sem variáveis de ambiente.
