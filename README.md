# Motion Club 🏃‍♂️⚽🏀

> **Move people. Make club.** — Train together. Belong together.

O **Motion Club** é uma plataforma de comunidade esportiva que conecta pessoas que querem praticar esportes em grupo. O usuário encontra grupos e eventos esportivos por modalidade e localização, participa de treinos coletivos e constrói consistência através da companhia e do incentivo mútuo — transformando exercício físico em hábito sustentável.

Projeto desenvolvido pelo **Grupo 4** na disciplina de desenvolvimento de software (PUC-Rio), seguindo metodologia ágil com entregas por sprint.

---

## 💡 O problema

A maioria das pessoas abandona aplicativos fitness e rotinas de exercício por falta de motivação, companhia e senso de pertencimento. O Motion Club ataca esse problema com foco em **comunidade**: grupos, eventos presenciais e incentivo social, sem competitividade tóxica nem pressão exagerada.

## ⚙️ Funcionalidades principais (MVP)

- **Cadastro e login** de usuários
- **Perfil editável** com esportes de interesse e nível (iniciante, intermediário, avançado)
- **Catálogo de esportes** por categoria (coletivo, individual, aquático)
- **Busca de grupos** por esporte e localização
- **Criação e participação em grupos** (abertos ou fechados, com papéis de admin/membro)
- **Eventos esportivos** com confirmação de presença, lista de espera e controle de status (aberto, lotado, cancelado, encerrado)

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python + Django |
| Frontend | HTML5, CSS3 |
| Banco de dados | SQLite (dev) — modelagem em `sprint 5/schema.sql` |
| Design | Figma (mockups) — identidade dark + verde neon |

## 🚀 Como rodar o projeto

Pré-requisitos: **Python 3.10+** instalado.

```bash
# 1. Clone o repositório
git clone https://github.com/Pietronsmf2/Grupo-4-esportes.git
cd Grupo-4-esportes/motionClub

# 2. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Aplique as migrações e inicie o servidor
cd MeuSite
python manage.py migrate
python manage.py runserver
```

As telas estáticas de gestão de usuários (login, registro, listagem, edição, exclusão) podem ser visualizadas abrindo diretamente os arquivos `.html` da pasta `sprint 5/` no navegador.

## 📁 Estrutura do repositório

```
├── motionClub/          # Aplicação Django (backend + templates)
│   └── MeuSite/
│       ├── core/        # Models: Usuario, Grupo, Evento, etc.
│       └── MeuSite/     # Configurações, URLs e views do projeto
├── sprint-1/            # Concorrentes, diferenciais, slogan, 20 soluções
├── sprint-2/            # Personas, requisitos funcionais e não funcionais, entrevistas
├── sprint-3/            # Arquitetura de informação, modelagem de dados, estudo de cor, pesquisa de mercado
├── sprint-4 e sprint 4/ # MVP, casos de uso, mockups, matriz de risco, monetização
├── sprint 5/            # Telas de gestão de usuários (HTML/CSS), schema SQL, estudos de engajamento
├── sprint 6/            # Identidade verbal, moderação, retenção, menu lateral, FAQs
├── sprint 7/            # Planos de assinatura e busca por localização
├── calculadora/         # Exercícios introdutórios em Python
└── Informações/         # Materiais de apoio e identidade visual
```

## 📋 Documentação por sprint

Cada pasta de sprint contém os artefatos produzidos na iteração, incluindo:

- **Pesquisa e validação:** análise de concorrentes, entrevistas, pesquisa de mercado, validação de hipóteses
- **Produto:** personas, requisitos, casos de uso, jornada do usuário, arquitetura de informação
- **Estratégia:** modelos de monetização, planos de assinatura, estratégia de aquisição e retenção de usuários
- **Impacto social:** análises de impactos positivos e negativos, segurança em encontros presenciais, prevenção de dependência digital e competitividade tóxica

## 👥 Equipe

Projeto desenvolvido pelo **Grupo 4 — Esportes**.

| Integrante | GitHub |
|---|---|
| Pietro Novello | [@Pietronsmf2](https://github.com/Pietronsmf2) |
| Caua Carnovali | [@cauacarnovali1-hue](https://github.com/cauacarnovali1-hue) |
| Artur Gutierrez | [@arturgutierrez](https://github.com/arturgutierrez) |
| Antonio Varejao | [@antoniovarejao](https://github.com/antoniovarejao) |


## 📄 Licença

Projeto acadêmico desenvolvido para fins educacionais.
 
