# Book Queue

- Meu objetivo é que este projeto seja o back-end para um pequeno site estilo blog no qual planejo publicar anotações
  sobre
  livros técnicos e tópicos que estou estudando atualmente.
- Estou usando TDD para este projeto, de forma pragmatica (pode não eu não faça muitos testes unitários,
  já que os modeloss são acoplados ao banco de dados).

> O front-end estará em um repositório separado, mas será em React (link será adicionado posteriormente)

## Arquitetura do Projeto

- Estou usando uma arquitetura em camadas durante o desenvolvimento desta aplicação, tendo camadas da seguinte forma:
    - Camada de apresentação -> a API em sí;
    - Camada de lógica de negócio -> services;
    - Camada de acesso a dados -> os models (que estão acoplados ao banco de pelo ORM);

## Stack

- FastAPI para a camada de apresentação
- SQLAlchemy para mapeamento ORM;
- PostgreSQL para o banco de dados;
- Pytest para testes;
- Alembic para migração de bacnos de dados