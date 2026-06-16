# Documentação Técnica Geral: Migração Web do Gestor Acadêmico

## 1. Visão Geral
Este documento delineia os requisitos técnicos gerais e a infraestrutura arquitetural estabelecidos para o processo de migração do sistema "Gestor Acadêmico". O projeto transita de uma arquitetura Desktop, originalmente desenvolvida com a interface gráfica PyQt, para uma moderna aplicação Web. O objetivo é assegurar escalabilidade, manutenibilidade e acesso distribuído aos usuários.

## 2. Requisitos Técnicos e Infraestrutura

### 2.1. Framework Web
O núcleo do desenvolvimento web, englobando o roteamento, o tratamento de requisições e a renderização das views, será construído sobre o **Flask (Python)**. A escolha por este microframework justifica-se pela sua leveza, flexibilidade e profunda sinergia com a linguagem base do sistema original (Python), o que facilitará o reaproveitamento das regras de negócio já consolidadas no domínio acadêmico.

### 2.2. Banco de Dados
A transição de um ambiente local (single-user) para a web exige a evolução do modelo de armazenamento de dados. O formato anterior em arquivos JSON será substituído de forma definitiva pelo **MySQL**. 
**Justificativa:** A migração para o MySQL é imperativa para suportar múltiplos acessos e transações simultâneas exigidos pela natureza da web. O MySQL fornecerá a consistência de dados (ACID), integridade referencial e o controle de concorrência necessários para garantir que as operações de leitura e escrita realizadas por diversos usuários não resultem em corrupção estrutural ou perdas de dados.

### 2.3. Gerenciamento de Configuração e Versionamento
Todo o controle de versão e configuração do projeto será hospedado e gerido via **GitHub**. Para assegurar que o desenvolvimento da nova arquitetura ocorra de forma independente e não interfira na base de código legado, adotou-se a estratégia de isolamento do código. O desenvolvimento da nova versão ocorrerá estritamente na branch `web`, permitindo iterações seguras e revisões de código isoladas da versão desktop original.

### 2.4. Infraestrutura e Deploy
A esteira de entrega e a arquitetura de execução (deploy) foram modernizadas para garantir alta disponibilidade e padronização dos ambientes:
- **Conteinerização:** A aplicação será inteiramente empacotada utilizando **Docker**. Isso garantirá paridade absoluta entre os ambientes de desenvolvimento, homologação e produção.
- **Servidor de Aplicação:** O tráfego de rede e a execução dos processos em Python serão gerenciados pelo **Gunicorn**, atuando como um servidor WSGI de alta performance para ambientes de produção.
- **Hospedagem e Orquestração:** Todo o conjunto será hospedado em uma **VPS**, cujo gerenciamento de ciclo de vida da aplicação e orquestração de deploy contínuo ficarão a cargo da plataforma **Dokploy**.

### 2.5. Métricas, Qualidade de Código e Guias de Estilo
A excelência e a legibilidade do código-fonte serão tratadas como prioridades técnicas incontestáveis:
- **Guias de Estilo:** Fica estabelecida a adoção rigorosa e impositiva da **PEP 8** (Python Enhancement Proposal 8) como o padrão oficial de formatação para todo o repositório.
- **Análise Estática e Métricas:** Para assegurar o cumprimento da PEP 8 e prevenir "code smells", formaliza-se o uso planejado do **Flake8** na esteira de integração. Complementarmente, a saúde arquitetural da aplicação será monitorada utilizando o **Radon**, ferramenta que ficará encarregada da medição contínua da complexidade ciclomática do código, visando evitar o acoplamento excessivo e funções de alta sobrecarga cognitiva.
