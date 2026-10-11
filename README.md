# PharmaSoft - Autónoma 08

Frontend Angular en raíz; backend Spring Boot en backend/. Base importada de la práctica 08 terminada. Repositorio: https://github.com/Irxui666/autonoma08.

## Ejecutar
Frontend: npm ci y npm start -- --port 4200. Backend: Java 21, Oracle local, variables DB_USERNAME y DB_PASSWORD; ejecutar mvnw.cmd spring-boot:run desde backend. El desarrollo local se conserva también en SEMANA7/tarea07-frontend y tarea07-backend.

## Entregables
- [PDF único para entregar en el aula](docs/Condori_LP2_S8_Autonoma.pdf): 29 páginas que reúnen el informe de cinco páginas con análisis B1-B5 y las 24 capturas del anexo.
- [Anexo de evidencias](docs/anexo-evidencias-s8.pdf): 24 capturas originales identificadas por caso.
- [Matriz de pruebas](docs/matriz-pruebas-s8.md): 14 casos base y cuatro propios, con resultados y enlaces a las capturas.
- docs/capturas-necesarias-s8.md: instrucciones de captura y preparación.
- postman/PharmaSoft-S8-Dependencias.json: colección v2.1 con 18 peticiones de casos y aserciones esperadas.
- [Informe en Markdown](docs/informe-hallazgos-s8.md): análisis B1-B5, correcciones propuestas y límites de la evidencia.

Resultado documental: 12 casos pasan con el alcance observado, un fallo comprobado (C-03), un fallo reportado con evidencia parcial (A-07), tres casos parciales (C-04, B-01 y B-03) y un caso pendiente (C-02). El informe distingue los resultados comprobados de los reportados y explica las evidencias faltantes. La navegación filtrada de Ver productos está implementada y cubierta por pruebas automatizadas; las capturas recibidas no prueban el recorrido completo.

La colección Postman fue preparada para ejecutar los casos; no es una exportación de la sesión del estudiante. No se presentan pruebas unitarias como ejecución manual ni se alteran fechas para simular commits en días distintos. La base usa ddl-auto=update; no incluye el historial Flyway del backend docente. La subida al aula virtual corresponde al estudiante.

## Verificación
Compilación Angular correcta y 20 pruebas aprobadas en 13 archivos. Pull request: https://github.com/Irxui666/autonoma08/pull/1. Las pruebas automatizadas no reemplazan los 18 casos manuales.

