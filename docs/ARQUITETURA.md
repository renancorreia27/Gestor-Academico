# Documentação de Engenharia de Software: Arquitetura do Gestor Acadêmico Web

## 1. Visão Geral
Este documento estabelece as diretrizes de Engenharia de Software aplicadas à nova versão Web do sistema "Gestor Acadêmico". O propósito desta documentação é mapear as decisões arquiteturais, princípios de engenharia estrutural e os Padrões de Projeto (Design Patterns) adotados, garantindo a manutenibilidade, testabilidade e escabilidade do código-fonte.

## 2. Estilos Arquiteturais
A estrutura macro e micro do sistema foi fundamentada em dois estilos arquiteturais consolidados, atuando em diferentes camadas de abstração:

### 2.1. Cliente-Servidor
Em nível de topologia de rede e distribuição física, adota-se o estilo **Cliente-Servidor**. O Cliente (Navegador Web do usuário) é o agente ativo responsável pela interface e captura de interações, comunicando-se via requisições HTTP estritas. O Servidor atua no processamento lógico; este reside no container da aplicação hospedado na VPS, gerando e devolvendo respostas apropriadas à solicitação.

### 2.2. MVC (Model-View-Controller)
No nível de arquitetura interna de software, adota-se o paradigma **MVC**, particionando as responsabilidades de negócio e apresentação:
- **Model:** Gerenciado pelo MySQL aliado aos componentes de acesso a dados (DAO). Retém a lógica de domínio, entidades de negócio e o estado persistido da aplicação.
- **View:** Construída mediante a renderização de documentos HTML combinados ao motor de templates Jinja acoplado ao Flask. Representa puramente a interface gráfica devolvida ao usuário.
- **Controller:** Constituído pelas rotas e lógicas orquestradoras do Flask. É o intermediador que reage às interações do usuário, manipula as regras no Model e aciona a View correta.

## 3. Princípio SOLID Aplicado

### 3.1. SRP (Single Responsibility Principle - Princípio da Responsabilidade Única)
A base de refatoração do código fundamenta-se estritamente no **SRP**. Promovemos a separação de escopos para garantir que cada módulo possua um único motivo para ser alterado.
Isso se materializa na **separação estrita entre a lógica de roteamento web e a lógica de persistência**. Os controladores do Flask (`app.py` e arquivos de rotas) têm o único papel de tratar requisições HTTP, gerenciar a sessão web e retornar respostas. Em hipótese alguma uma rota deve possuir instruções SQL diretas; toda a responsabilidade de acesso a dados e formatação de queries é delegada a módulos específicos do banco de dados, promovendo altíssimo nível de coesão e baixo acoplamento.

## 4. Design Patterns (Padrões de Projeto)
Na estruturação dos componentes lógicos, foram aplicados deliberadamente os seguintes padrões de projeto:

### 4.1. MVC (Model-View-Controller)
Além de um estilo arquitetural amplo, o **MVC** é o padrão base fundamental que orienta o design de todo o fluxo de entrada e saída do aplicativo, separando claramente visualização, controle de fluxo e armazenamento.

### 4.2. Singleton
Empregado na camada de conectividade de dados. A adoção do **Singleton** garante a existência de uma instância única e global do pool de conexões (ou objeto conector) com o banco de dados MySQL ao longo do ciclo de execução, mitigando severos impactos de performance relacionados à abertura excessiva e desnecessária de conexões simultâneas.

### 4.3. Application Factory
Adotado para o provisionamento do servidor web através da função `create_app()` do Flask. O padrão **Application Factory** centraliza a montagem, o registro de blueprints e a configuração em uma fábrica de instâncias. Isso propicia escalabilidade segura do código e viabiliza a execução de múltiplos ambientes (ex.: teste automatizado local isolado do ambiente de produção) sem colisões de variáveis globais.

### 4.4. Decorator
O roteamento declarativo da aplicação apoia-se nativamente no padrão estrutural **Decorator**. A marcação explícita de funções orquestradoras usando anotações como `@app.route` do Flask mapeia URLs de requisições de forma dinâmica, adicionando comportamentos no ciclo de vida da execução sem modificar intrinsecamente a estrutura da função alvo subjacente.

### 4.5. DAO (Data Access Object) / Repository
Toda a interação com a base de dados subjacente será encapsulada em classes especializadas, fundamentadas nos padrões **DAO / Repository**. Este padrão determina um isolamento de todas as queries SQL, escondendo dos Controllers a complexidade técnica do mecanismo relacional (MySQL). O banco de dados passa a ser tratado pelo resto do sistema de maneira puramente orientada a objetos (enviando e recebendo informações abstraídas).
