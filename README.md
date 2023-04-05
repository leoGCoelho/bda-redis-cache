# bda-redis-cache

---

## Como usar (no local)

1. Com o Docker instalado, usar o comando **docker compose -f docker-compose.yml up --build**.
  - Se não funcionar, use **docker-compose -f docker-compose.yml up --build**.
2. Use o **http://localhost:5000**, para acessar os endpoints

---

## Endpoints

- **/ :** Teste de ping da API
- **/carros :** Puxar lista de carros sem cache
- **/carros_cache :** Puxar lista de carros com cache
