# Matriz de pruebas S8

Estado inicial: 0 casos de aceptación ejecutados en esta entrega. No confundir pruebas unitarias con ejecución SPA/Postman. Completar resultados reales y evidencias antes del PDF final.

Reglas elegidas: C-03 impide desactivar categorías con productos activos; B-04 impide eliminar categorías con cualquier producto, incluso inactivo.

| ID | Operación | Precondición | Datos | Resultado esperado | Resultado obtenido (SPA y HTTP) | Estado | Evidencia |
|---|---|---|---|---|---|---|---|
| A-01 | Alta válida | Categoría activa | nombre único; precio 5.50; stock 10 | SPA: POST 201 y fila con categoría | Pendiente de ejecución | Pendiente | capturas/A-01_spa.png y/o A-01_postman.png |
| A-02 | Alta sin categoría | Formulario nuevo | omitir categoriaId | SPA bloquea sin POST; API 400 con categoriaId | Pendiente de ejecución | Pendiente | capturas/A-02_spa.png y/o A-02_postman.png |
| A-03 | Alta categoría inexistente | Confirmar que 999 no existe | categoriaId=999 | API 404; mensaje Categoria no encontrada | Pendiente de ejecución | Pendiente | capturas/A-03_spa.png y/o A-03_postman.png |
| A-04 | Alta categoría inactiva | catInactiva estado false | categoriaId={{catInactiva}} | SPA no la ofrece; API 409 | Pendiente de ejecución | Pendiente | capturas/A-04_spa.png y/o A-04_postman.png |
| A-05 | Alta nombre duplicado | Existe producto con nombreBase | nombreBase en otra capitalización | SPA muestra mensaje; POST 409 | Pendiente de ejecución | Pendiente | capturas/A-05_spa.png y/o A-05_postman.png |
| A-06 | Alta valores negativos | Categoría activa | precio=0; stock=-1 | SPA bloquea; API 400 con precio y stock en validationErrors | Pendiente de ejecución | Pendiente | capturas/A-06_spa.png y/o A-06_postman.png |
| C-01 | Cambiar categoría | Producto activo y otra categoría activa | categoriaId={{catOtra}} | PUT 200; fila muestra nueva categoría | Pendiente de ejecución | Pendiente | capturas/C-01_spa.png y/o C-01_postman.png |
| C-02 | Cambiar a categoría inactiva | Producto existente; catInactiva | categoriaId={{catInactiva}} | SPA bloquea; API 409 | Pendiente de ejecución | Pendiente | capturas/C-02_spa.png y/o C-02_postman.png |
| C-03 | Desactivar categoría con activos | Categoría de prueba con producto activo | estado=false | Regla elegida: impedir desactivación con 409 para proteger ventas | Pendiente de ejecución | Pendiente | capturas/C-03_spa.png y/o C-03_postman.png |
| C-04 | Categoría desactualizada en dos pestañas | Nuevo producto abierto con categoría X | Desactivar X en pestaña 2; registrar en pestaña 1 | POST 409; no se guarda en categoría inactiva | Pendiente de ejecución | Pendiente | capturas/C-04_spa.png y/o C-04_postman.png |
| B-01 | Baja lógica | productoBaja activo | DELETE productoBaja | 204; permanece fila Inactivo y botón deshabilitado | Pendiente de ejecución | Pendiente | capturas/B-01_spa.png y/o B-01_postman.png |
| B-02 | Baja repetida | Ejecutar B-01 primero | DELETE mismo producto | 409; mensaje producto ya inactivo | Pendiente de ejecución | Pendiente | capturas/B-02_spa.png y/o B-02_postman.png |
| B-03 | Eliminar categoría vacía | catVacia sin productos | DELETE catVacia | 204; desaparece en categorías y selector al recargar | Pendiente de ejecución | Pendiente | capturas/B-03_spa.png y/o B-03_postman.png |
| B-04 | Eliminar categoría con productos inactivos | catSoloInactivos solo contiene productos de baja | DELETE catSoloInactivos | 409; conservar clasificación histórica | Pendiente de ejecución | Pendiente | capturas/B-04_spa.png y/o B-04_postman.png |
| A-07 | Alta precio con tres decimales | Categoría activa | precio=1.001 | SPA bloquea; API debería devolver 400 por precisión monetaria | Pendiente de ejecución | Pendiente | capturas/A-07_spa.png y/o A-07_postman.png |
| C-05 | Editar producto inexistente | Confirmar producto 999 inexistente | PUT /productos/999 con datos válidos | 404; Producto no encontrado | Pendiente de ejecución | Pendiente | capturas/C-05_spa.png y/o C-05_postman.png |
| B-05 | Baja producto inexistente | Confirmar producto 999 inexistente | DELETE /productos/999 | 404; Producto no encontrado | Pendiente de ejecución | Pendiente | capturas/B-05_spa.png y/o B-05_postman.png |
| A-08 | Alta stock cero | Categoría activa; nombre único | stock=0; precio=0.01 | 201; stock cero permitido en inventario | Pendiente de ejecución | Pendiente | capturas/A-08_spa.png y/o A-08_postman.png |
