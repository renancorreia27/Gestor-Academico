# Documentação de Gestão de Engenharia: Processo de Desenvolvimento do Gestor Acadêmico Web

## 1. Visão Geral
Este documento detalha o arcabouço metodológico, as ferramentas operacionais de controle e os processos de automação de infraestrutura estabelecidos pela liderança técnica para conduzir a transição estrutural do "Gestor Acadêmico" para a plataforma Web.

## 2. Gerenciamento do Projeto

### 2.1. Metodologia Ágil (Scrum)
Visando previsibilidade, cadência e adaptação contínua, o ciclo de vida do desenvolvimento de software foi alicerçado no framework **Scrum**. A vasta arquitetura da migração foi fragmentada em ciclos iterativos de tempo limitado (Sprints). Esse processo garantiu entregas funcionais incrementais, reduzindo os riscos severos associados à reescrita de código e permitindo a validação precoce de módulos essenciais, como a nova interface e o banco de dados.

### 2.2. Ferramenta de Gestão (Trello e Kanban)
A organização tática e o mapeamento das tarefas diárias foram concentrados na plataforma **Trello**, que atua no projeto como um legítimo quadro **Kanban**.
- **Product Backlog:** Os grandes Épicos de desenvolvimento exigidos pela migração (ex: "Migrar camada visual do PyQt para Jinja2", "Estruturação em Docker") formaram o alicerce do Product Backlog no Trello.
- **Sprint Backlogs:** Durante os planejamentos, as grandes entregas foram quebradas em cards acionáveis para compor os Sprint Backlogs. O fluxo de colunas tradicionais do Kanban (como "To Do", "In Progress", "Code Review" e "Done") ofereceu rastreabilidade transparente e visual sobre os eventuais gargalos de código da equipe.

## 3. Integração e Entrega Contínuas (CI/CD)
O processo de disponibilização em produção da versão Web foi inteiramente modernizado. O paradigma de "Deploy Manual" foi abolido e substituído por uma esteira automatizada eficiente, segura e baseada em eventos.

### 3.1. O Fluxo Automatizado
A arquitetura de entrega contínua que leva o código da máquina do desenvolvedor até o ambiente em produção segue este encadeamento rigoroso:

1. **Versionamento e Disparo (Trigger):** Todo o repositório lógico e estrutural do Gestor Acadêmico é controlado no **GitHub**. O ciclo de deploy se inicia estritamente quando há um novo *push* (ou merge de *Pull Request*) concretizado de forma auditável na branch isolada `web`.
2. **Mensageria via Webhook:** A própria nuvem do GitHub detecta a mutação na branch e invoca um gatilho de rede programado (Webhook). Esse Webhook dispara uma notificação segura por meio de uma requisição HTTP para a interface da nossa VPS.
3. **Orquestração pelo Dokploy:** A plataforma **Dokploy**, em execução na VPS, intercepta e autoriza o alerta do Webhook. Sem necessidade de aprovação humana, o Dokploy executa a sincronização (*pull*) da versão mais recente do código no GitHub. 
4. **Build Docker e Deploy Silencioso:** Com o novo código baixado, o Dokploy aciona a engine local do Docker. O `Dockerfile` focado em produção é lido para reinstalar dependências, processar o projeto Python/Flask e construir (Build) uma imagem docker otimizada. Por fim, o Dokploy substitui o container atual em execução pelo recém-criado, aplicando as atualizações no ambiente de produção instantaneamente e sem qualquer intervenção manual da equipe de infraestrutura.
