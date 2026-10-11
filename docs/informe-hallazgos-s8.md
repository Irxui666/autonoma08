# Informe de hallazgos - Autónoma 08


## B1. Resumen de la ejecución

Condori | Lenguaje de Programación II | 11 de octubre de 2026. Matriz de 18 casos: 14 base y 4 propios. Se analizaron las capturas aportadas por el estudiante; los casos incompletos conservan esa condición.


## Resultados por grupo

Altas (8): 7 Pasa y 1 Falla reportada con evidencia parcial (A-07). Cambios (5): 2 Pasa, 1 Falla comprobada (C-03), 1 Parcial (C-04) y 1 Pendiente (C-02). Bajas (5): 3 Pasa con alcance observado y 2 Parcial (B-01, B-03). Total: 12 Pasa, 2 hallazgos de distinta fuerza probatoria, 3 Parcial y 1 Pendiente.


## Evidencias y preparación

El anexo contiene 24 capturas originales identificadas por caso. Se observan tres categorías activas y una inactiva, y más de ocho productos, incluidos inactivos. La matriz enlaza las capturas. B-04 demuestra el bloqueo de categoría 22 y un producto asociado inactivo; no hay consulta exhaustiva de asociaciones.


## Alcance de entrega

Frontend compilado y 20 pruebas automatizadas aprobadas en 13 archivos. No sustituyen ejecución manual. Repositorio: https://github.com/Irxui666/autonoma08. PR: https://github.com/Irxui666/autonoma08/pull/1. Rama feature/pruebas-dependencias-condori hacia develop; se publican además frontend y backend.


## Límites expresos

C-02 no tiene evidencia específica. C-04 carece de HTTP visible; B-01 carece del DELETE 204 inicial; B-03 no muestra 204 ni selector posterior. La captura de Productos con tamaño 100 usa /productos sin queryParam y Todas; acredita tamaño 100, no navegación filtrada. El botón Ver productos sí está visible en Categorías.

# B2. Fichas de hallazgos


## H-01 | C-03 | Severidad alta

Se permite desactivar Analgesicos (categoría 1) con productos activos: PUT 200 y fila Inactivo. La regla elegida exige impedir esa transición para evitar catálogo activo bajo clasificación inactiva. Evidencias: C-03_spa.png y listados de productos activos en esa categoría.


## Causa y corrección de H-01

backend/src/main/java/com/example/Actividad01/service/impl/CategoriaServiceImpl.java, update: asigna estado sin consultar productos activos. Propuesta en servicio: antes de pasar a inactivo consultar existsByCategoriaIdAndEstadoTrue(id), añadido a ProductoRepository; si existen, devolver 409. Validar y escribir dentro de una transacción coordinada con altas y cambios de Productos. No se aplicó la corrección para conservar el comportamiento evaluado.


## H-02 | A-07 | Severidad media | Reportado

El estudiante informó que la API aceptó precio 1.001. El listado muestra Prueba A07 tres decimales a S/ 1.00. No hay captura del cuerpo y HTTP del POST: el formato monetario no demuestra redondeo persistido. La captura SPA usa 0.001 y stock -1; tampoco aísla la regla de dos decimales. La falla se registra como reportada, con evidencia parcial.


## Causa y corrección de H-02

backend/src/main/java/com/example/Actividad01/dto/ProductoRequestDTO.java, precio: tiene DecimalMin, sin Digits. Propuesta en API: añadir @Digits con fraction=2 y máximo entero compatible con la columna. Mantener la validación SPA. Repetir alta única con precio 1.001 y stock 10; comprobar POST 400 y consultar valor almacenado si antes respondió 201.


## Riesgo adicional: concurrencia

C-04 muestra que el formulario puede quedar obsoleto. ProductoServiceImpl.buscarCategoria valida al guardar, pero una lectura sin bloqueo no prueba atomicidad ante desactivación simultánea. Coordinar bloqueo de la categoría en ambos servicios y validar tras adquirirlo; diseñar prueba concurrente adicional. Se presenta como riesgo técnico, no como fallo observado.

# B3. Cobertura de reglas y B4. Filtro


## Cobertura actual

Existencia: SPA orienta con el selector; API valida existencia y devuelve 404 en buscarCategoria. Categoría activa: SPA filtra/bloquea y API devuelve 409. Nombre único: API valida sin distinguir mayúsculas; SPA presenta el error. Eliminación con productos: API usa existsByCategoriaId e incluye inactivos; SPA muestra el rechazo. Baja lógica: API cambia estado y rechaza repetición; SPA deshabilita el botón. Desactivar categoría con productos activos: no hay bloqueo específico en ninguna capa.


## Referencias de cobertura

Frontend: src/app/features/productos/pages/producto-form/producto-form.ts; producto-list/producto-list.ts; core/utils/http-error.ts. Backend: ProductoServiceImpl.create/update/delete/buscarCategoria, CategoriaServiceImpl.update/delete y ProductoRepository. Mostrar un error de API en la SPA no equivale a una segunda validación independiente.


## B4. Por qué el filtro es local

ProductoList.productos filtra resultado.contenido, que solo contiene la página recibida. Aumentar tamanio a 100 amplía el tramo visible pero no vuelve global el filtro ni garantiza mostrar todos los productos de la categoría.


## Cambio completo propuesto

Endpoint ProductoController.findAll: añadir categoriaId opcional y positivo; propagarlo por ProductoService.listar backend. Repositorio: Page<Producto> findByCategoriaId(Long categoriaId, Pageable pageable). Usar findAll cuando no llegue ID y consulta filtrada cuando llegue; construir PaginaResponse desde esa página para obtener totales correctos.


## Servicio frontend y presentación

Ampliar ProductoService.listar con categoriaId opcional; agregarlo con HttpParams solo si existe. Al cambiar categoría reiniciar pagina=0 y consultar API; retirar filtrado local duplicado y nota de primeros 100. Definir contrato para ID inexistente. Es una propuesta; la mejora exigida por la guía conserva filtro local y tamaño 100.

# B5. Preguntas de análisis


## 1. ¿Por qué no basta con ocultar categorías?

Postman puede enviar cualquier ID y la categoría puede cambiar después de abrir el formulario. A-04 demuestra el rechazo 409 de categoría 21; C-02 todavía requiere ejecución específica. ProductoForm orienta; ProductoServiceImpl.buscarCategoria impone la dependencia para todos los clientes.


## 2. ¿Qué hacer al desactivar con productos activos?

Se elige impedirlo con 409, obligando a reclasificar o dar de baja antes. Evita productos vendibles bajo categoría inactiva. CategoriaServiceImpl.update debe consultar activos; H-01 documenta que actualmente permite 200. El cierre de una venta también debería comprobar disponibilidad y estados en la API.


## 3. ¿Contar productos dados de baja al eliminar?

Sí. Conservan referencias, trazabilidad y clasificación para reportes. CategoriaServiceImpl.delete usa existsByCategoriaId sin filtro de estado. Una eliminación física puede romper claves foráneas o perder clasificación histórica. B-04 confirma bloqueo de la categoría probada; conservarla o archivarla es preferible.


## 4. ¿Qué revela C-04?

Que la validez de una opción al cargar no garantiza su validez al guardar. La API es la capa que puede coordinar clientes y transacciones con la base de datos. create/update llaman buscarCategoria; para transacciones simultáneas se necesita coordinación de bloqueo, no solo validación visual.


## 5. ¿Qué cambia en la SPA si se corrige A-04?

Esta base ya rechaza A-04 con 409. Frente a una versión que antes aceptaba, la SPA debe mantener formulario y mostrar mensajeError; puede refrescar categorías. El selector activo, [ngValue], categoriaId numérico y validaciones siguen iguales. No debe convertir el rechazo en éxito.

# Mejora, trazabilidad y cierre


## Parte C. Ver productos implementado

categoria-list.html incorpora routerLink=/productos y queryParams categoriaId. ProductoList recibe input<string>(), valida ID, preselecciona categoría y tamanio=100 antes de cargar. El selector conserva la selección después de cargar categorías; muestra nota de primeros 100 registros. app.config.ts ya tiene withComponentInputBinding. Pruebas automatizadas cubren entrada e ID inválido.


## Evidencia visual de la mejora

Las capturas muestran Ver productos en Categorías y GET tamanio=100. La imagen del listado usa Todas y URL sin categoriaId: no acredita el recorrido filtrado. La implementación y tests están disponibles para repetir la navegación; no se declara esa captura como prueba visual completa.


## Colección Postman y resultados

postman/PharmaSoft-S8-Dependencias.json contiene las peticiones preparadas y aserciones esperadas. Es una colección generada para las pruebas, no una exportación de la sesión del usuario. Las respuestas visibles están acreditadas por las capturas; no se inventaron cuerpos ni códigos para las operaciones restantes.


## Versionamiento y entrega

Base de práctica importada al repositorio inicialmente vacío; no se modificó tarea08 para esta entrega documental. Hay al menos tres commits convencionales, todos con fecha real del mismo día: aún no satisfacen días distintos. No se alteraron fechas. Backend local usa Oracle y ddl-auto=update, sin migraciones del repositorio docente.


## Archivos y pendientes

docs/matriz-pruebas-s8.md; docs/informe-hallazgos-s8.pdf; docs/anexo-evidencias-s8.pdf; copia para aula Condori_LP2_S8_Autonoma.pdf. Cerrar C-02 y las evidencias parciales requeriría más ejecución del estudiante. Este documento termina el análisis disponible sin declarar cumplimiento íntegro de las 18 pruebas. La subida al aula virtual corresponde al estudiante.


## Fuente

Guía s8_lp2_actividad_autonoma_v4jm5dlo8u (1).pdf, Partes A-D y lista de cotejo; código del repositorio autonoma08; capturas aportadas durante la sesión de pruebas del 11/10/2026.