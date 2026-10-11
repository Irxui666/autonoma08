# PharmaSoft - Autónoma 08

Frontend Angular en raíz; backend Spring Boot en backend/. Base importada de la práctica 08 terminada. Repositorio: https://github.com/Irxui666/autonoma08.

## Ejecutar
Frontend: npm ci y npm start -- --port 4200. Backend: Java 21, Oracle local, variables DB_USERNAME y DB_PASSWORD; ejecutar mvnw.cmd spring-boot:run desde backend. El desarrollo local se conserva también en SEMANA7/tarea07-frontend y tarea07-backend.

## Entregables
- docs/matriz-pruebas-s8.md: 14 casos base y cuatro propios; resultados pendientes de ejecución manual.
- docs/capturas-necesarias-s8.md: instrucciones de captura y preparación.
- postman/PharmaSoft-S8-Dependencias.json: colección v2.1 con 18 peticiones de casos y aserciones esperadas.
- docs/informe-hallazgos-s8.md: análisis B1-B5 y riesgos detectados por revisión estática.

El PDF final requiere resultados y capturas reales. No se presentan pruebas unitarias como ejecución manual ni se alteran fechas para simular commits en días distintos. La base usa ddl-auto=update; no incluye el historial Flyway del backend docente.
