# Graph Report - Registration-backend-service  (2026-11-12)

## Corpus Check
- В структурный анализ включено файлов исходного кода: 11. Сторонние зависимости, документация и файлы окружения исключены.

## Summary
- 71 nodes · 126 edges · 8 communities (6 shown, 2 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- main.py
- db_provider.py
- env.py
- sqlalchemy
- login_user
- Schemas.py
- settings.py

## God Nodes (most connected - your core abstractions)
1. `login_user()` - 7 edges
2. `UserSchema` - 6 edges
3. `add_user_to_db()` - 6 edges
4. `register_user()` - 6 edges
5. `LoginRequest` - 5 edges
6. `get_current_user()` - 5 edges
7. `produce_message()` - 5 edges
8. `Base` - 4 edges
9. `User` - 4 edges
10. `LoginResponse` - 4 edges

## Surprising Connections (you probably didn't know these)
- `login_user()` --uses--> `LoginRequest`  [INFERRED]
  main.py → Schemas.py
- `login_user()` --uses--> `LoginResponse`  [INFERRED]
  main.py → Schemas.py
- `add_user_to_db()` --uses--> `UserSchema`  [INFERRED]
  db_provider.py → Schemas.py
- `register_user()` --uses--> `UserSchema`  [INFERRED]
  main.py → Schemas.py
- `add_user_to_db()` --uses--> `User`  [INFERRED]
  db_provider.py → models.py

## Import Cycles
- None detected.

## Communities (8 total, 2 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.21
Nodes (4): get_current_user(), read_root(), create_access_token(), verify_access_token()

### Community 1 - "db_provider.py"
Cohesion: 0.24
Nodes (4): add_user_to_db(), get_db(), Base, User

### Community 2 - "env.py"
Cohesion: 0.27
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

### Community 3 - "sqlalchemy"
Cohesion: 0.36
Nodes (3): downgrade(), upgrade(), upgrade()

### Community 4 - "login_user"
Cohesion: 0.31
Nodes (4): produce_message(), producer_callback(), login_user(), register_user()

### Community 5 - "Schemas.py"
Cohesion: 0.39
Nodes (5): LoginRequest, LoginResponse, Token, TokenData, UserSchema

## Knowledge Gaps
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_current_user()` connect `main.py` to `login_user`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `login_user()` (e.g. with `LoginRequest` and `LoginResponse`) actually correct?**
  _`login_user()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Why does `add_user_to_db()` connect `db_provider.py` to `main.py`, `login_user`, `Schemas.py`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `UserSchema` (e.g. with `add_user_to_db()` and `register_user()`) actually correct?**
  _`UserSchema` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `add_user_to_db()` (e.g. with `User` and `UserSchema`) actually correct?**
  _`add_user_to_db()` has 2 INFERRED edges - model-reasoned connections that need verification._