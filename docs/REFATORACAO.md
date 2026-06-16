# Documentação de Engenharia de Software: Refatoração e Migração do Gestor Acadêmico

## 1. Visão Geral
Este documento relata o processo de modernização do código-fonte do "Gestor Acadêmico", detalhando as estratégias de refatoração formal aplicadas durante a sua evolução de um monólito Desktop (Windows/PyQt) para uma aplicação Web orientada a serviços gerida pelo Flask. O foco é preservar a base lógica enquanto a infraestrutura e a tecnologia de apresentação são totalmente substituídas.

## 2. Novos Requisitos (Vida Real)
O deslocamento da aplicação de uma máquina local para o escopo global da web trouxe complexidades que demandaram soluções técnicas robustas. O novo sistema agora lida de forma nativa com:

- **Acessibilidade e Responsividade:** Diferentemente da janela travada no ecossistema Windows, a nova aplicação exige acessibilidade irrestrita via navegadores. A interface de usuário deve se comportar dinamicamente e de forma responsiva, acomodando perfeitamente a renderização tanto em dimensões de telas de Desktop quanto em dispositivos Mobile.
- **Gerenciamento e Controle de Sessões:** No contexto Desktop "single-user", o software confiava que havia apenas uma pessoa atrás da tela. Na web, o sistema atende diversos usuários assincronamente. Implementamos o isolamento absoluto de contextos através do controle de sessões HTTP, rastreando quem fez a requisição e qual o seu pacote de dados acadêmicos correspondente.
- **Segurança e Proteção de Rotas:** O sistema exposto à internet exigiu a instauração de barreiras de segurança nos *endpoints*. Nenhuma página, painel ou ação de edição é acessível de forma anônima; todas as rotas do Flask agora implementam mecanismos de proteção que validam o estado da sessão antes de renderizar os *templates* ou processar formulários.

## 3. Técnicas de Refactoring Utilizadas
A transformação da arquitetura legado obedeceu a um processo formal de Engenharia de Software visando limpar o código (Clean Code) e mitigar débitos técnicos de acoplamento. As seguintes técnicas consagradas foram aplicadas:

### 3.1. *Substitute Algorithm* (Substituição de Algoritmo)
- **O que foi feito:** Toda a mecânica pesada de renderização baseada na biblioteca gráfica Qt foi trocada de forma cirúrgica.
- **Explicação Técnica:** Os antigos arquivos de design XML (`.ui` do PyQt) foram sumariamente descartados. O algoritmo de geração de telas pesadas do Windows foi substituído pelo paradigma moderno de renderização server-side, adotando **Templates HTML5** interpolados dinamicamente com a engine de marcação **Jinja2**.

### 3.2. *Extract Method* (Extração de Método)
- **O que foi feito:** Desacoplamento vertical das regras de negócio que sofriam do anti-pattern *Fat UI* (lógica dentro da interface).
- **Explicação Técnica:** Na versão Qt, regras acadêmicas severas — como recálculo do IRA ou persistência de novos semestres — estavam reagindo e atreladas intimamente aos eventos de UI (conceito de *Signals e Slots* do Qt). Utilizamos o *Extract Method* para arrancar todo esse código de dentro da camada de apresentação, transformando-os em métodos e funções "puras" no back-end da aplicação que não têm conhecimento de quem os invocou.

### 3.3. *Move Method* (Movimentação de Método)
- **O que foi feito:** Realocação da camada de sanitização e verificação de integridade dos dados fornecidos pelo usuário.
- **Explicação Técnica:** As pesadas validações de formulários e tipos numéricos, que antes repousavam como métodos encapsulados na classe da janela principal (`janela_principal.py`), sofreram *Move Method* em duas frentes distintas. Primeiramente, as validações de feedback instantâneo e usabilidade (UX) foram transferidas para o front-end web, delegadas ao **JavaScript**. Em uma segunda frente primária de segurança de dados, as validações core da aplicação foram movidas para as rotas (**Controllers do Flask**), sendo executadas antes do envio dos *payloads* aos Daos.
