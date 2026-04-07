# Engineering Roadmap: Automation Hub 2026

Este documento detalla la evolución arquitectónica del proyecto hacia **Arquitectura Hexagonal**, **DDD** y **Production-Ready Standards**.

## Fase 1: Saneamiento y Desacoplamiento (Corto Plazo)
*Objetivo: Separar la lógica de negocio de los detalles de infraestructura.*

- [ ] **1.1 Definición de Entidades de Dominio:** Migrar la lógica de `models.py` (SQLAlchemy) a Clases Puras de Python (POPOs).
- [ ] **1.2 Inversión de Dependencias (DIP):** Crear `AbstractPorts` para servicios externos (Google Calendar, Sheets).
- [ ] **1.3 Refactor de Inyección:** Usar `Dependency Injection` para pasar adaptadores a los servicios de dominio.

## Fase 2: Patrones Tácticos y Persistencia (Mediano Plazo)
*Objetivo: Lograr ignorancia de persistencia y atomicidad.*

- [ ] **2.1 Repository Pattern:** Implementar repositorios para abstraer las consultas de SQLAlchemy.
- [ ] **2.2 Unit of Work (UoW):** Implementar un manejador de contexto para transacciones atómicas de negocio.
- [ ] **2.3 Domain Events:** Definir eventos (e.g., `EventScheduled`) que el dominio pueda emitir.

## Fase 3: Mensajería y Observabilidad (Largo Plazo)
*Objetivo: Resiliencia y escalabilidad.*

- [ ] **3.1 Message Bus Interno:** Implementar un bus para manejar eventos de forma asíncrona.
- [ ] **3.2 Logs Estructurados (JSON):** Sustituir `print` por `structlog` para trazabilidad en producción.
- [ ] **3.3 Estrategia de Idempotencia:** Asegurar que reintentos de red no dupliquen acciones en las APIs.

## ADRs (Architecture Decision Records)
*Documentación de decisiones críticas.*

- [ ] ADR-001: Adopción de Arquitectura Hexagonal.
- [ ] ADR-002: Elección de Repository Pattern sobre Active Record.
