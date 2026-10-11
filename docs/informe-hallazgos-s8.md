# Informe de hallazgos S8 - borrador previo a ejecución

## B1. Resumen de ejecución
Matriz preparada: 18 casos (8 altas, 5 cambios y 5 bajas). Ejecutados manualmente con evidencia en esta entrega: 0. Pasa: 0. Falla: 0. Pendientes: 18. Los resultados deberán completarse a partir de la SPA y Postman. Los riesgos siguientes proceden de revisión estática y no se presentan como fallos observados en producción.

## B2. Riesgos a contrastar y fichas propuestas

### R-01 - C-03: desactivar una categoría con productos activos
Severidad propuesta: alta. Regla elegida: impedir la desactivación para evitar que el catálogo de venta conserve productos activos cuya clasificación no está operativa. Causa probable: `backend/src/main/java/com/example/Actividad01/service/impl/CategoriaServiceImpl.java`, método `update`, asigna estado sin consultar productos activos. Evidencia pendiente: C-03_spa.png y petición PUT de la colección. Corrección propuesta: en la capa de servicio, al pasar de activo a inactivo, consultar `existsByCategoriaIdAndEstadoTrue(id)` y devolver 409 si hay productos activos. Esa consulta debe añadirse a `ProductoRepository`. Al ejecutar, si se obtiene 200, convertir R-01 en H-01 con resultado real, cuerpo y evidencia.

### R-02 - A-07: precisión monetaria inconsistente
Severidad propuesta: media, por discrepancia entre validación y persistencia. `ProductoRequestDTO.precio` tiene DecimalMin pero no restricción de escala; la SPA valida dos decimales. Evidencia pendiente: A-07_postman.png. Corrección propuesta en el DTO de la API: `@Digits(integer = 8, fraction = 2)` si coincide con la precisión efectiva de la columna, para rechazar 1.001 con 400. Confirmar esquema antes de fijar el máximo entero. Verificar si la persistencia rechaza, redondea o acepta y registrar el comportamiento exacto.

### R-03 - C-04: concurrencia real
Severidad potencial: alta. `ProductoServiceImpl.buscarCategoria()` comprueba el estado al registrar/editar, por lo que debería rechazar un formulario obsoleto. Eso no equivale a garantizar dos transacciones simultáneas: leer activo y desactivar antes del commit todavía puede generar una carrera. La corrección completa debe coordinar el bloqueo de la categoría en los servicios de Productos y Categorías, validar después de adquirirlo y mantener un orden uniforme de bloqueo. C-04 comprueba el formulario obsoleto; una prueba concurrente adicional sería necesaria para acreditar atomicidad.

## B3. Cobertura de reglas

| Regla | SPA | API | Referencia |
|---|---|---|---|
| Categoría existente | Selección de catálogo; no garantiza vigencia | Sí, 404 | ProductoForm; ProductoServiceImpl.buscarCategoria |
| Categoría activa en alta/cambio | Sí | Sí, 409 | ProductoForm; buscarCategoria |
| Nombre único sin distinguir mayúsculas | Muestra rechazo del servidor | Sí | ProductoServiceImpl.create/update; ProductoRepository |
| No eliminar categoría con productos | Muestra rechazo del servidor | Sí, incluye inactivos | CategoriaServiceImpl.delete; existsByCategoriaId |
| Baja lógica y no repetida | Botón inactivo deshabilitado | Sí, 204/409 | ProductoList.darDeBaja; ProductoServiceImpl.delete |
| Desactivar categoría con productos activos | No hay bloqueo específico | No hay bloqueo específico | CategoriaServiceImpl.update |

Mostrar un error del backend en la SPA no significa que exista validación independiente en ambas capas. Las filas lo distinguen.

## B4. Recomendación para el filtro por categoría
Hoy `ProductoList.productos` filtra `resultado.contenido`; este arreglo solo contiene una página. La mejora Ver productos amplía a 100 registros y avisa del límite, pero no cambia esa semántica. Para un filtro global, añadir `@RequestParam(required = false) Long categoriaId` a `ProductoController.findAll`; transmitirlo en la interfaz y servicio backend; añadir `Page<Producto> findByCategoriaId(Long categoriaId, Pageable pageable)` en `ProductoRepository`. Elegir `findAll(pageable)` cuando el parámetro sea nulo y la consulta filtrada cuando exista; mapear esa página al DTO. Así totales y páginas corresponden al subconjunto.

En el frontend, ampliar `ProductoService.listar(pagina, tamanio, ordenarPor, direccion, categoriaId?)`; usar HttpParams y agregar categoriaId solo si existe. Al cambiar el filtro, reiniciar pagina a 0 y consultar la API. Eliminar el filtrado local duplicado, mostrar el contenido devuelto y retirar la nota de primeros 100 registros. Validar ID positivo y definir si un ID inexistente devuelve página vacía o 404. Esta es una propuesta; la guía pide mantener el filtro local en la mejora de la Parte C.

## B5. Preguntas de análisis

1. Ocultar opciones inactivas solo orienta al usuario. Un cliente HTTP puede enviar cualquier categoriaId y un formulario abierto puede quedar desactualizado. A-04 y C-02 deben contrastar ese bypass. `ProductoForm` filtra opciones y `ProductoServiceImpl.buscarCategoria` impone la regla en la API; aún falta registrar la evidencia de los casos.

2. Se elige impedir desactivar una categoría con productos activos. Evita un catálogo contradictorio y obliga a reclasificar o dar de baja productos antes de la desactivación. Las ventas deben validar tanto estado del producto como categoría en el momento de confirmar. `CategoriaServiceImpl.update` requiere la consulta de activos propuesta en R-01; la decisión es explícita y no se acomoda al comportamiento actual.

3. Sí: B-04 debe rechazar la eliminación incluso si todos los productos están inactivos. La baja lógica conserva referencias necesarias para trazabilidad y reportes de ventas. `CategoriaServiceImpl.delete` usa `ProductoRepository.existsByCategoriaId`, sin filtrar estado. Eliminar la categoría podría romper claves foráneas o perder clasificación histórica; un archivo lógico sería una alternativa a evaluar.

4. C-04 revela que validar al cargar el select no es suficiente: hay que hacerlo al guardar. Solo la API, coordinada con transacciones y base de datos, puede garantizar la regla ante todos los clientes. `ProductoServiceImpl.create/update` llaman `buscarCategoria`; el bloqueo transaccional propuesto en R-03 cubre el intervalo entre lectura y escritura.

5. En esta base A-04 ya se contempla en `buscarCategoria`; falta demostrarlo con Postman. Si una versión previa aceptara 201 y se corrigiera a 409, la SPA debe conservar el formulario y mostrar el mensaje mediante `mensajeError`; podría refrescar categorías tras el rechazo. Las opciones activas, [ngValue], validaciones y contrato categoriaId seguirían iguales. No debe duplicar la autoridad de la regla ni convertir el rechazo en un mensaje de éxito.

## C. Mejora implementada
`categoria-list.html` navega con routerLink y queryParams. `ProductoList` recibe `input<string>()`, valida el identificador, fija categoría y tamaño 100 antes de cargar. El selector refleja la categoría; la nota informa el límite. `app.config.ts` ya incorpora withComponentInputBinding. Se agregaron pruebas del enlace de entrada y de IDs inválidos. Las capturas de la navegación se solicitarán con las evidencias de aceptación.

## D. Entrega y pendientes
Repositorio autonoma08; rama feature/pruebas-dependencias-condori hacia develop. Se importó la práctica terminada como base del repositorio vacío. Los commits tienen fecha real; el requisito de días distintos exige trabajo en fechas adicionales. El PDF de 3 a 5 páginas se completará con resultados reales y se entregará también como Condori_LP2_S8_Autonoma.pdf. Subir al aula virtual corresponde al usuario.
