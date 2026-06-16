# Documentação de Análise de Sistemas: Modelagem UML da Arquitetura Web

## 1. Visão Geral
Este documento exibe as reestruturações aplicadas na modelagem estrutural e comportamental da aplicação (Diagramas UML) do "Gestor Acadêmico", evidenciando o contraste gerado pela modernização de um sistema Desktop autônomo (Windows/PyQt) para a nova arquitetura baseada em rede, operando sob o ecossistema Web (Flask/MySQL).

## 2. Diagrama de Casos de Uso (Use Cases)
No escopo de produto e requisitos funcionais, as regras de negócio basilares mantêm-se intactas: o fluxo de Adicionar Nota, Computar Faltas e Gerir Semestres não sofre mutação do ponto de vista do domínio. Contudo, a **fronteira do sistema** expande drasticamente. Abandonamos o confinamento de um "Sistema Operacional Local" e passamos a representar a nova barreira de uma "Aplicação Web" global, exigindo que o Ator interaja remotamente por meio de um cliente padronizado.

```mermaid
flowchart LR
    User(["Usuário (Via Navegador)"])
    
    subgraph "Fronteira: Gestor Acadêmico (Aplicação Web)"
        direction TB
        UC1(Adicionar Nova Matéria)
        UC2(Adicionar Nota em Avaliação)
        UC3(Registrar Nova Falta)
        UC4(Gerenciar Ciclo de Semestres)
        UC5(Consultar Índices de Desempenho)
    end
    
    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5
```

## 3. Diagrama de Classes
Em termos de estática arquitetural, as classes do projeto passaram por uma cirurgia de *Decoupling* rigorosa:
1. Houve a erradicação imediata das antigas superclasses oriundas do design visual do Qt Desktop (heranças de `QMainWindow`, `QDialog`, `QWidget`).
2. Adotou-se fisicamente a tríade MVC: O diagrama reflete a inserção explícita dos **Controladores** (as funções de Rota dinâmicas providas pelo Flask), e a representação passiva e delegada das **Views** através de templates HTML formatados via Jinja2. O back-end foca agora unicamente em orquestrar entidades (Model) e persistência (DAO).

```mermaid
classDiagram
    class FlaskRouteController {
        <<Controller>>
        +route_dashboard(request)
        +route_adicionar_nota(request)
        +route_adicionar_falta(request)
    }
    
    class JinjaTemplateHTML {
        <<View>>
        +render_template()
        +exibir_dados_formatados()
    }
    
    class EntidadeDAO {
        <<Repository / DAO>>
        -ConexaoMySQL db_pool
        +buscar_registros()
        +executar_insert_sql()
        +executar_update_sql()
    }

    class MateriaModel {
        <<Entity / Domain>>
        +String nome
        +Float media_calculada
        +Int total_faltas
        +calcular_aprovação()
    }

    FlaskRouteController --> JinjaTemplateHTML : Injeta Dados e Renderiza
    FlaskRouteController --> EntidadeDAO : Transaciona Dados e Lógica
    EntidadeDAO --> MateriaModel : Retorna/Persiste Objeto
```

## 4. Diagrama de Sequência
O comportamento do sistema e o eixo temporal de vida das transações deixaram de ser baseados em reações elétricas locais.
No ecossistema Desktop, o fluxo era guiado por *"Clique no UI -> Evento de SO -> Processamento Thread Local"*. Agora, adotamos estritamente o ciclo de vida stateless da Web. O fluxo comportamental muda para: *"Usuário submete formulário de dados -> Navegador encapsula requisição HTTP POST -> Servidor de Rotas Flask processa -> Camada DAO salva/altera no MySQL -> Servidor finaliza com resposta HTTP contendo HTML/JSON atualizado"*.

```mermaid
sequenceDiagram
    actor Usuario
    participant Navegador as Navegador Web (Client)
    participant Controller as Rota Flask (Controller)
    participant DAO as Data Access Object (DAO)
    participant BD as Banco MySQL (Database)

    Usuario->>Navegador: Preenche formulário web e clica 'Salvar'
    Navegador->>Controller: Envia requisição HTTP POST (com payload JSON/Form)
    Controller->>DAO: Extrai dados, valida e aciona método de persistência
    DAO->>BD: Estabelece conexão e executa Query SQL (Ex: INSERT)
    BD-->>DAO: Confirmação de operação atômica e Ids
    DAO-->>Controller: Retorna flag de Sucesso / Regra confirmada
    Controller-->>Navegador: Devolve Resposta HTTP (302 Redirect ou 200 OK com novo HTML)
    Navegador-->>Usuario: Atualiza a tela (DOM) refletindo a nova ação
```
