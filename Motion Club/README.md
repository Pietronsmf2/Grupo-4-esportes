# Motion Club — Django

Comunidade esportiva: **landing page**, **login** e **gestão de usuários** (cadastrar,
listar, ver perfil com métricas e remover). Backend e dados em **Django + SQLite**.
Front-end **sem JavaScript** — os efeitos de rolagem são feitos com CSS moderno
(scroll-driven animations) e interações (menu, mostrar senha) com truque de checkbox.

> ✅ **Já está pronto aqui:** instalei um **Python portátil** em `.python/`, criei e
> **populei o banco** (`db.sqlite3`, 42 usuários etc.) e integrei suas imagens.
> **Não abra os arquivos `.html` direto no navegador** — um app Django só funciona com o
> servidor rodando (é por isso que "não abria com o CSS"). Veja "Como rodar".

## Requisitos

- Nada a instalar para rodar agora — use o Python portátil em `.python/` (Opção 0).
- Para um ambiente próprio: **Python 3.10+** (recomendado 3.12) —
  https://www.python.org/downloads/ (no Windows, marque *"Add python.exe to PATH"*).

## Como rodar

> **Não dê duplo-clique nos `.html`.** São templates Django — precisam do servidor no ar.

### Opção 0 — já configurado (rode agora)

```powershell
.\.python\python.exe manage.py runserver
```

Depois abra **http://127.0.0.1:8000/**. (No app, o botão de preview também sobe esse servidor.)

### Opção A — script com venv (Windows / PowerShell)

```powershell
powershell -ExecutionPolicy RemoteSigned -File setup.ps1
```

Ele cria a `.venv`, instala dependências, cria o banco, **popula** e sobe o servidor.

### Opção B — manual (qualquer SO)

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
python manage.py seed          # popula a comunidade de exemplo
python manage.py runserver
```

Acesse **http://127.0.0.1:8000/**. Para o admin: `python manage.py createsuperuser` e
entre em `/admin/`.

## Rotas

| URL | Página |
|---|---|
| `/` | Landing (modalidades, grupos, eventos e depoimentos vindos do banco) |
| `/login/` | Tela de login (apresentacional) |
| `/usuarios/` | Listar usuários (com busca) |
| `/usuarios/novo/` | Formulário de registro de usuário |
| `/usuarios/<id>/` | Perfil do usuário **com métricas** |
| `/usuarios/<id>/remover/` | Remoção de usuário (confirmação) |
| `/admin/` | Django admin |

## Modelagem (`core/models.py`)

- **Sport** — modalidade (corrida, futebol, ciclismo…).
- **Member** — usuário/atleta: nome, e-mail, cidade, nível, bio, **esportes de
  preferência** (M2M) e **conexões** (M2M consigo mesmo = pessoas que conheceu).
- **SportGroup** — grupo de uma modalidade, com membros.
- **Event** — evento aberto.
- **Participation** — cada presença de um usuário (base da métrica de frequência).
- **Testimonial** — depoimento exibido na landing.

### Métricas do usuário (tela de perfil)

Calculadas em Python a partir do banco:

- **Participações** — quantas vezes treinou/competiu (`Participation`).
- **Pessoas conhecidas** — conexões feitas no esporte (`connections`).
- **Grupos** — grupos de que participa.
- **Modalidades** — esportes de preferência.
- **Participações por esporte** — gráfico de barras por modalidade.

## Imagens

As fotos ficam em `static/images/` (veja `static/images/README.txt` com a **lista exata
de nomes** de arquivo). Enquanto não existirem, o site mostra blocos escuros no lugar —
nada quebra. Exporte os frames do Figma e solte os arquivos com os nomes indicados, ou
ajuste o campo *imagem* de cada modalidade no `/admin`.

## Efeitos (sem JS)

- Reveal on scroll, parallax e barra de progresso → CSS `animation-timeline` (scroll-driven).
- Menu mobile e mostrar/ocultar senha → checkbox + CSS.
- Em navegadores sem suporte a scroll-driven animations, o conteúdo simplesmente aparece
  sem animação (degradação graciosa). Respeita `prefers-reduced-motion`.

## Estrutura

```
manage.py            requirements.txt   setup.ps1
motionclub/          # settings, urls, wsgi/asgi
core/                # app: models, views, forms, urls, admin
  management/commands/seed.py   # popular o banco
templates/           # base, home, login, members/*
static/css/          # base, home, login, members  (zero JS)
static/images/       # <- coloque as imagens aqui
```
