# Capturas y ejecución de la autónoma 08

## Preparación
Usar categorías y productos de prueba. Tener al menos tres categorías activas, una inactiva y ocho productos repartidos entre ellas, incluido uno inactivo. No borrar categorías usadas en ventas. Crear además una categoría vacía y una que solo contenga productos inactivos. Los IDs dependen de tu base: consultar GET categorías y productos antes de configurar variables.

Importar postman/PharmaSoft-S8-Dependencias.json como colección v2.1. Completar catActiva, catOtra, catInactiva, catConActivos, catCarrera, catVacia, catSoloInactivos, productoCambio, productoBaja, nombreDuplicado (otra capitalización de un nombre real) y nombreCatConActivos. baseUrl ya está configurada. No ejecutar toda la colección sin preparar los datos: varias operaciones modifican estados o eliminan registros vacíos.

## Qué debe verse
En Postman: nombre del caso, método y URL, código HTTP y cuerpo JSON de respuesta. En SPA: mensaje o resultado y Red con la petición seleccionada. Si la SPA bloquea, limpiar Red antes de pulsar Guardar y capturar el error con Red vacía. Un 204 no tiene cuerpo. Nombrar archivos con ID: A-04_spa.png, A-04_postman.png. Un caso puede requerir dos o tres capturas.

## Secuencia

- **A-01 - Alta válida:** Categoría activa. Usar nombre único; precio 5.50; stock 10. Capturar SPA: POST 201 y fila con categoría.

- **A-02 - Alta sin categoría:** Formulario nuevo. Usar omitir categoriaId. Capturar SPA bloquea sin POST; API 400 con categoriaId.

- **A-03 - Alta categoría inexistente:** Confirmar que 999 no existe. Usar categoriaId=999. Capturar API 404; mensaje Categoria no encontrada.

- **A-04 - Alta categoría inactiva:** catInactiva estado false. Usar categoriaId={{catInactiva}}. Capturar SPA no la ofrece; API 409.

- **A-05 - Alta nombre duplicado:** Existe producto con nombreBase. Usar nombreBase en otra capitalización. Capturar SPA muestra mensaje; POST 409.

- **A-06 - Alta valores negativos:** Categoría activa. Usar precio=0; stock=-1. Capturar SPA bloquea; API 400 con precio y stock en validationErrors.

- **C-01 - Cambiar categoría:** Producto activo y otra categoría activa. Usar categoriaId={{catOtra}}. Capturar PUT 200; fila muestra nueva categoría.

- **C-02 - Cambiar a categoría inactiva:** Producto existente; catInactiva. Usar categoriaId={{catInactiva}}. Capturar SPA bloquea; API 409.

- **C-03 - Desactivar categoría con activos:** Categoría de prueba con producto activo. Usar estado=false. Capturar Regla elegida: impedir desactivación con 409 para proteger ventas.

- **C-04 - Categoría desactualizada en dos pestañas:** Nuevo producto abierto con categoría X. Usar Desactivar X en pestaña 2; registrar en pestaña 1. Capturar POST 409; no se guarda en categoría inactiva.

- **B-01 - Baja lógica:** productoBaja activo. Usar DELETE productoBaja. Capturar 204; permanece fila Inactivo y botón deshabilitado.

- **B-02 - Baja repetida:** Ejecutar B-01 primero. Usar DELETE mismo producto. Capturar 409; mensaje producto ya inactivo.

- **B-03 - Eliminar categoría vacía:** catVacia sin productos. Usar DELETE catVacia. Capturar 204; desaparece en categorías y selector al recargar.

- **B-04 - Eliminar categoría con productos inactivos:** catSoloInactivos solo contiene productos de baja. Usar DELETE catSoloInactivos. Capturar 409; conservar clasificación histórica.

- **A-07 - Alta precio con tres decimales:** Categoría activa. Usar precio=1.001. Capturar SPA bloquea; API debería devolver 400 por precisión monetaria.

- **C-05 - Editar producto inexistente:** Confirmar producto 999 inexistente. Usar PUT /productos/999 con datos válidos. Capturar 404; Producto no encontrado.

- **B-05 - Baja producto inexistente:** Confirmar producto 999 inexistente. Usar DELETE /productos/999. Capturar 404; Producto no encontrado.

- **A-08 - Alta stock cero:** Categoría activa; nombre único. Usar stock=0; precio=0.01. Capturar 201; stock cero permitido en inventario.

## Casos con preparación especial
C-02 SPA: asociar previamente un producto a una categoría activa, inactivar esa categoría y abrir su edición. Capturar categoría original (inactiva), aviso y guardado bloqueado. Probar también PUT directo en Postman.

C-03: intentar desactivar una categoría con productos activos. Si responde 200, registrar Falla; no cambiar la expectativa para ocultar el hallazgo. Nuestra regla elegida exige 409, pero la implementación heredada no tiene ese bloqueo. Restaurar la categoría al terminar si se usa fuera de pruebas.

C-04: en pestaña 1 dejar Nuevo producto preparado con categoría X activa; en pestaña 2 desactivar X; volver a pestaña 1 y registrar. Capturar el cambio y el rechazo 409. Usar categoría exclusivamente de prueba. Si el backend bloquea C-03, usar una categoría sin productos antes del registro.

B-01 antes de B-02. B-03 exige categoría vacía. B-04 exige que todos sus productos estén inactivos. A-07 puede revelar ausencia de precisión decimal en la API: registrar exactamente el resultado, incluso si es 201.

## Mejora Ver productos
Capturar Categorías con el botón y, después del clic, Productos con URL ?categoriaId=ID, opción seleccionada, tamaño 100, nota de primeros 100 registros y GET tamanio=100. No afirmar que muestra todo el catálogo si existen más de 100 productos.

Enviar las capturas y los resultados para completar la matriz y el PDF final. La guía exige tres commits en días distintos: los commits generados en esta sesión tienen su fecha real y aún no satisfacen ese requisito temporal.
