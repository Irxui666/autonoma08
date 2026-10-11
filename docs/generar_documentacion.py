from pathlib import Path
import shutil
import re
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader, simpleSplit

ROOT=Path(__file__).resolve().parent
CAP=ROOT/'capturas'
CAP.mkdir(exist_ok=True)
TEMP=Path('C:/Users/jomac/AppData/Local/Temp')
evidencias=[
('A-01_spa','0273d41b-9fd8-44c5-81eb-2b0663c1162c','Alta de asdas: POST 201 y producto con categoría en listado.'),
('A-02_postman','c4af5a04-e617-41ac-afe9-83d0b73f2201','Sin categoriaId: 400 y validationErrors.categoriaId.'),
('A-02_spa','0756f4e5-ba13-4cde-8f40-63e8d5575f7d','Categoría requerida; Network vacío tras intento.'),
('A-03_postman','872c254f-a5e1-40ab-925f-f3a2826b0250','Categoría 999 inexistente: 404.'),
('A-04_postman','57d4de8d-8dfc-4b56-b25b-cf2647bf7170','Categoría 21 inactiva: 409 con mensaje.'),
('A-04_spa','929b81ef-326f-4cb2-ad0d-400e962aef49','Selector ofrece Analgesicos y Antibioticos; excluye relajantes, ID 21.'),
('A-05_spa','6b2704a1-ae9e-4d5f-8f5f-603aa2bffa77','AMOXICILINA 500MG duplicado: POST 409.'),
('A-06_postman','0246a8c7-327d-402a-b132-d9bf2cc40816','Precio 0 y stock -1: 400 con ambos errores.'),
('A-06_spa','08a1b8b8-6212-4ebe-a10f-879a5e97d45b','Validaciones de precio y stock; Network vacío.'),
('A-07_spa','5ac70a92-b637-4b9c-b91d-4a4d444702b9','Precio 0.001 y stock -1 bloqueados. No aísla la escala: también incumple mínimo y stock.'),
('A-07_listado','97b232c8-0a8d-49a4-93d4-0caa01fdb35b','Prueba A07 tres decimales aparece en listado con S/ 1.00. No demuestra por sí sola el valor persistido ni el HTTP del alta.'),
('A-08_postman','d32f8e06-4bfd-4f5c-b1c3-348ddc598933','Stock cero y precio 0.01: 201, producto ID 46.'),
('C-01_spa','598672b6-3d6a-433b-86fe-afa3668f76ce','PUT /productos/3 200; Amoxicilina cambia a Antibioticos.'),
('C-03_spa','f5f2821f-79ff-4a65-8b2e-36f9dd685943','PUT /categorias/1 200; Analgesicos queda inactiva pese a productos activos.'),
('C-04_categoria','56691a2e-9b93-43cc-bfc8-21fc364ac287','Segunda desactivación de categoría 1: 200. Evidencia de cambio de estado.'),
('C-04_spa','c32af13d-fd13-42d9-bed2-a080a58b12a1','Formulario de alta obsoleto muestra rechazo de categoría inactiva; no se ve Network ni HTTP.'),
('C-05_postman','e5385f9c-aa17-472a-ba33-0c89cbe46166','PUT /productos/32222: 404 Producto no encontrado.'),
('B-01_confirmacion','1d65a30b-db06-4586-9728-3b1be8ea7efe','Confirmación de baja de Amoxicilina; no incluye HTTP 204.'),
('B-02_postman','0df3ffff-31cc-449d-8b63-5440f2eedd32','DELETE /productos/3: 409, producto ya inactivo.'),
('B-03_spa','d2679c70-a53a-48e2-9f73-73b0e9005f92','Mensaje categoría eliminada y desaparición de relajantes; Network vacío, no se ve 204.'),
('B-04_spa','b9cffa91-33e8-4342-97c6-d05353534706','DELETE /categorias/22: 409 por productos asociados.'),
('B-04_productos','ef23d72b-94f0-491a-8e93-170986ffc836','Prueba1 de categoría prueba aparece inactivo; complemento de B-04.'),
('B-05_postman','6262f13a-7e52-43a5-ab45-9b5cecc9f5a2','DELETE /productos/32222: 404.'),
('Preparacion_categorias','e1e065fd-364b-43d1-993c-40911157cccb','Categorías 22, 2 y 23 activas; categoría 1 inactiva. Botón Ver productos visible.')
]
for name,uid,caption in evidencias:
 src=TEMP/f'codex-clipboard-{uid}.png'
 if src.exists():shutil.copy2(src,CAP/f'{name}.png')

results={
'A-01':('Alta asdas con precio 123 y stock 1; POST 201; fila en Analgesicos.','Pasa','A-01_spa'),
'A-02':('SPA bloquea sin petición; API 400 con error categoriaId.','Pasa','A-02_spa, A-02_postman'),
'A-03':('POST con categoriaId 999: 404 Categoria no encontrada.','Pasa','A-03_postman'),
'A-04':('Selector excluye relajantes; POST categoriaId 21: 409 inactiva.','Pasa','A-04_spa, A-04_postman'),
'A-05':('POST AMOXICILINA 500MG: 409; mensaje de nombre duplicado.','Pasa','A-05_spa'),
'A-06':('SPA bloquea precio 0 y stock -1; API 400 con ambos validationErrors.','Pasa','A-06_spa, A-06_postman'),
'A-07':('Usuario reporta aceptación de 1.001; producto visible a S/ 1.00. Falta captura de POST/HTTP; SPA capturada usa 0.001 y stock -1.','Falla reportada; evidencia parcial','A-07_spa, A-07_listado'),
'A-08':('POST 201; ID 46 con precio 0.01 y stock 0.','Pasa','A-08_postman'),
'C-01':('PUT producto 3: 200; Amoxicilina cambia de Analgesicos a Antibioticos.','Pasa','C-01_spa'),
'C-02':('No se recibió PUT de producto a categoría inactiva ni edición bloqueada. El alta obsoleta corresponde a C-04.','Pendiente','Sin captura específica'),
'C-03':('PUT categoría 1: 200; queda inactiva conservando productos activos. Contradice regla elegida.','Falla','C-03_spa'),
'C-04':('Categoría desactivada; alta obsoleta muestra error de categoría inactiva. HTTP no visible.','Parcial','C-04_categoria, C-04_spa'),
'C-05':('PUT producto 32222 con cuerpo válido: 404.','Pasa','C-05_postman'),
'B-01':('Confirmación de baja; después Amoxicilina aparece inactiva y DELETE repetido devuelve 409. Falta HTTP 204 inicial.','Parcial','B-01_confirmacion, A-07_listado, B-02_postman'),
'B-02':('DELETE producto 3: 409 El producto ya está inactivo.','Pasa','B-02_postman'),
'B-03':('Mensaje de eliminación y categoría 21 ausente; falta 204 y selector posterior.','Parcial','B-03_spa'),
'B-04':('DELETE categoría 22: 409; producto asociado Prueba1 visible inactivo. No hay consulta exhaustiva de sus asociaciones.','Pasa con alcance observado','B-04_spa, B-04_productos'),
'B-05':('DELETE producto 32222: 404.','Pasa','B-05_postman')}
matrix=ROOT/'matriz-pruebas-s8.md'
s=matrix.read_text(encoding='utf-8')
s=re.sub(r'Estado inicial:.*?\n\n','Cierre documental: 12 casos pasan con el alcance observado, 1 falla comprobada, 1 falla reportada con evidencia parcial, 3 casos parciales y 1 pendiente. No se afirma ejecución completa de los 18 casos.\n\n',s,count=1,flags=re.S)
rows=[]
for line in s.splitlines():
 if line.startswith('| ') and line.split('|')[1].strip() in results:
  cols=[x.strip() for x in line.split('|')[1:-1]]
  ident=cols[0];obt,estado,ev=results[ident]
  cols[5:]=[obt,estado,', '.join(f'[captura](capturas/{x.strip()}.png)' for x in ev.split(',')) if ev!='Sin captura específica' else ev]
  if ident in ['C-05','B-05']:cols[2]='Producto 32222 inexistente';cols[3]=('PUT' if ident=='C-05' else 'DELETE')+' /productos/32222'
  if ident=='A-01':cols[3]='asdas; precio 123; stock 1; categoría Analgesicos'
  line='| '+' | '.join(cols)+' |'
 rows.append(line)
matrix.write_text('\n'.join(rows)+'\n',encoding='utf-8')

pages=[
('Informe de hallazgos - Autónoma 08',[
('B1. Resumen de la ejecución','Condori | Lenguaje de Programación II | 11 de octubre de 2026. Matriz de 18 casos: 14 base y 4 propios. Se analizaron las capturas aportadas por el estudiante; los casos incompletos conservan esa condición.'),
('Resultados por grupo','Altas (8): 7 Pasa y 1 Falla reportada con evidencia parcial (A-07). Cambios (5): 2 Pasa, 1 Falla comprobada (C-03), 1 Parcial (C-04) y 1 Pendiente (C-02). Bajas (5): 3 Pasa con alcance observado y 2 Parcial (B-01, B-03). Total: 12 Pasa, 2 hallazgos de distinta fuerza probatoria, 3 Parcial y 1 Pendiente.'),
('Evidencias y preparación','El anexo contiene 24 capturas originales identificadas por caso. Se observan tres categorías activas y una inactiva, y más de ocho productos, incluidos inactivos. La matriz enlaza las capturas. B-04 demuestra el bloqueo de categoría 22 y un producto asociado inactivo; no hay consulta exhaustiva de asociaciones.'),
('Alcance de entrega','Frontend compilado y 20 pruebas automatizadas aprobadas en 13 archivos. No sustituyen ejecución manual. Repositorio: https://github.com/Irxui666/autonoma08. PR: https://github.com/Irxui666/autonoma08/pull/1. Rama feature/pruebas-dependencias-condori hacia develop; se publican además frontend y backend.'),
('Límites expresos','C-02 no tiene evidencia específica. C-04 carece de HTTP visible; B-01 carece del DELETE 204 inicial; B-03 no muestra 204 ni selector posterior. La captura de Productos con tamaño 100 usa /productos sin queryParam y Todas; acredita tamaño 100, no navegación filtrada. El botón Ver productos sí está visible en Categorías.')]),
('B2. Fichas de hallazgos',[
('H-01 | C-03 | Severidad alta','Se permite desactivar Analgesicos (categoría 1) con productos activos: PUT 200 y fila Inactivo. La regla elegida exige impedir esa transición para evitar catálogo activo bajo clasificación inactiva. Evidencias: C-03_spa.png y listados de productos activos en esa categoría.'),
('Causa y corrección de H-01','backend/src/main/java/com/example/Actividad01/service/impl/CategoriaServiceImpl.java, update: asigna estado sin consultar productos activos. Propuesta en servicio: antes de pasar a inactivo consultar existsByCategoriaIdAndEstadoTrue(id), añadido a ProductoRepository; si existen, devolver 409. Validar y escribir dentro de una transacción coordinada con altas y cambios de Productos. No se aplicó la corrección para conservar el comportamiento evaluado.'),
('H-02 | A-07 | Severidad media | Reportado','El estudiante informó que la API aceptó precio 1.001. El listado muestra Prueba A07 tres decimales a S/ 1.00. No hay captura del cuerpo y HTTP del POST: el formato monetario no demuestra redondeo persistido. La captura SPA usa 0.001 y stock -1; tampoco aísla la regla de dos decimales. La falla se registra como reportada, con evidencia parcial.'),
('Causa y corrección de H-02','backend/src/main/java/com/example/Actividad01/dto/ProductoRequestDTO.java, precio: tiene DecimalMin, sin Digits. Propuesta en API: añadir @Digits con fraction=2 y máximo entero compatible con la columna. Mantener la validación SPA. Repetir alta única con precio 1.001 y stock 10; comprobar POST 400 y consultar valor almacenado si antes respondió 201.'),
('Riesgo adicional: concurrencia','C-04 muestra que el formulario puede quedar obsoleto. ProductoServiceImpl.buscarCategoria valida al guardar, pero una lectura sin bloqueo no prueba atomicidad ante desactivación simultánea. Coordinar bloqueo de la categoría en ambos servicios y validar tras adquirirlo; diseñar prueba concurrente adicional. Se presenta como riesgo técnico, no como fallo observado.')]),
('B3. Cobertura de reglas y B4. Filtro',[
('Cobertura actual','Existencia: SPA orienta con el selector; API valida existencia y devuelve 404 en buscarCategoria. Categoría activa: SPA filtra/bloquea y API devuelve 409. Nombre único: API valida sin distinguir mayúsculas; SPA presenta el error. Eliminación con productos: API usa existsByCategoriaId e incluye inactivos; SPA muestra el rechazo. Baja lógica: API cambia estado y rechaza repetición; SPA deshabilita el botón. Desactivar categoría con productos activos: no hay bloqueo específico en ninguna capa.'),
('Referencias de cobertura','Frontend: src/app/features/productos/pages/producto-form/producto-form.ts; producto-list/producto-list.ts; core/utils/http-error.ts. Backend: ProductoServiceImpl.create/update/delete/buscarCategoria, CategoriaServiceImpl.update/delete y ProductoRepository. Mostrar un error de API en la SPA no equivale a una segunda validación independiente.'),
('B4. Por qué el filtro es local','ProductoList.productos filtra resultado.contenido, que solo contiene la página recibida. Aumentar tamanio a 100 amplía el tramo visible pero no vuelve global el filtro ni garantiza mostrar todos los productos de la categoría.'),
('Cambio completo propuesto','Endpoint ProductoController.findAll: añadir categoriaId opcional y positivo; propagarlo por ProductoService.listar backend. Repositorio: Page<Producto> findByCategoriaId(Long categoriaId, Pageable pageable). Usar findAll cuando no llegue ID y consulta filtrada cuando llegue; construir PaginaResponse desde esa página para obtener totales correctos.'),
('Servicio frontend y presentación','Ampliar ProductoService.listar con categoriaId opcional; agregarlo con HttpParams solo si existe. Al cambiar categoría reiniciar pagina=0 y consultar API; retirar filtrado local duplicado y nota de primeros 100. Definir contrato para ID inexistente. Es una propuesta; la mejora exigida por la guía conserva filtro local y tamaño 100.')]),
('B5. Preguntas de análisis',[
('1. ¿Por qué no basta con ocultar categorías?','Postman puede enviar cualquier ID y la categoría puede cambiar después de abrir el formulario. A-04 demuestra el rechazo 409 de categoría 21; C-02 todavía requiere ejecución específica. ProductoForm orienta; ProductoServiceImpl.buscarCategoria impone la dependencia para todos los clientes.'),
('2. ¿Qué hacer al desactivar con productos activos?','Se elige impedirlo con 409, obligando a reclasificar o dar de baja antes. Evita productos vendibles bajo categoría inactiva. CategoriaServiceImpl.update debe consultar activos; H-01 documenta que actualmente permite 200. El cierre de una venta también debería comprobar disponibilidad y estados en la API.'),
('3. ¿Contar productos dados de baja al eliminar?','Sí. Conservan referencias, trazabilidad y clasificación para reportes. CategoriaServiceImpl.delete usa existsByCategoriaId sin filtro de estado. Una eliminación física puede romper claves foráneas o perder clasificación histórica. B-04 confirma bloqueo de la categoría probada; conservarla o archivarla es preferible.'),
('4. ¿Qué revela C-04?','Que la validez de una opción al cargar no garantiza su validez al guardar. La API es la capa que puede coordinar clientes y transacciones con la base de datos. create/update llaman buscarCategoria; para transacciones simultáneas se necesita coordinación de bloqueo, no solo validación visual.'),
('5. ¿Qué cambia en la SPA si se corrige A-04?','Esta base ya rechaza A-04 con 409. Frente a una versión que antes aceptaba, la SPA debe mantener formulario y mostrar mensajeError; puede refrescar categorías. El selector activo, [ngValue], categoriaId numérico y validaciones siguen iguales. No debe convertir el rechazo en éxito.')]),
('Mejora, trazabilidad y cierre',[
('Parte C. Ver productos implementado','categoria-list.html incorpora routerLink=/productos y queryParams categoriaId. ProductoList recibe input<string>(), valida ID, preselecciona categoría y tamanio=100 antes de cargar. El selector conserva la selección después de cargar categorías; muestra nota de primeros 100 registros. app.config.ts ya tiene withComponentInputBinding. Pruebas automatizadas cubren entrada e ID inválido.'),
('Evidencia visual de la mejora','Las capturas muestran Ver productos en Categorías y GET tamanio=100. La imagen del listado usa Todas y URL sin categoriaId: no acredita el recorrido filtrado. La implementación y tests están disponibles para repetir la navegación; no se declara esa captura como prueba visual completa.'),
('Colección Postman y resultados','postman/PharmaSoft-S8-Dependencias.json contiene las peticiones preparadas y aserciones esperadas. Es una colección generada para las pruebas, no una exportación de la sesión del usuario. Las respuestas visibles están acreditadas por las capturas; no se inventaron cuerpos ni códigos para las operaciones restantes.'),
('Versionamiento y entrega','Base de práctica importada al repositorio inicialmente vacío; no se modificó tarea08 para esta entrega documental. Hay al menos tres commits convencionales, todos con fecha real del mismo día: aún no satisfacen días distintos. No se alteraron fechas. Backend local usa Oracle y ddl-auto=update, sin migraciones del repositorio docente.'),
('Archivos y pendientes','docs/matriz-pruebas-s8.md; docs/informe-hallazgos-s8.pdf; docs/anexo-evidencias-s8.pdf; copia para aula Condori_LP2_S8_Autonoma.pdf. Cerrar C-02 y las evidencias parciales requeriría más ejecución del estudiante. Este documento termina el análisis disponible sin declarar cumplimiento íntegro de las 18 pruebas. La subida al aula virtual corresponde al estudiante.'),
('Fuente','Guía s8_lp2_actividad_autonoma_v4jm5dlo8u (1).pdf, Partes A-D y lista de cotejo; código del repositorio autonoma08; capturas aportadas durante la sesión de pruebas del 11/10/2026.')])]
styles=getSampleStyleSheet()
styles['Normal'].fontSize=10
styles['Normal'].leading=14
styles['Heading2'].fontSize=12
styles['Heading2'].leading=15
story=[]
md=[]
for i,(title,sections) in enumerate(pages):
 if i:story.append(PageBreak())
 story.append(Paragraph(escape(title),styles['Title']))
 md.append('# '+title)
 for subtitle,body in sections:
  story.extend([Paragraph(escape(subtitle),styles['Heading2']),Paragraph(escape(body),styles['Normal']),Spacer(1,6)])
  md.extend(['\n## '+subtitle,body])
def footer(c,doc):
 c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#617086'))
 c.drawString(40,25,'Condori | LP II | Autónoma 08');c.drawRightString(A4[0]-40,25,str(doc.page))
out=ROOT/'informe-hallazgos-s8.pdf'
SimpleDocTemplate(str(out),pagesize=A4,rightMargin=40,leftMargin=40,topMargin=32,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
(ROOT/'informe-hallazgos-s8.md').write_text('\n\n'.join(md),encoding='utf-8')
shutil.copy2(out,ROOT/'Condori_LP2_S8_Autonoma.pdf')
W,H=landscape(A4)
c=canvas.Canvas(str(ROOT/'anexo-evidencias-s8.pdf'),pagesize=(W,H))
c.setTitle('Anexo de evidencias - Autónoma 08')
for i,(name,uid,caption) in enumerate(evidencias,1):
 c.setFillColor(colors.HexColor('#12315c'));c.rect(0,H-48,W,48,fill=1,stroke=0)
 c.setFillColor(colors.white);c.setFont('Helvetica-Bold',17);c.drawString(25,H-31,name.replace('_',' - '))
 c.setFillColor(colors.HexColor('#173251'));c.setFont('Helvetica',10)
 y=H-66
 for line in simpleSplit(caption,'Helvetica',10,W-50):c.drawString(25,y,line);y-=14
 ir=ImageReader(str(CAP/f'{name}.png'));iw,ih=ir.getSize();avail=y-40;scale=min((W-40)/iw,avail/ih)
 c.drawImage(ir,(W-iw*scale)/2,35+(avail-ih*scale)/2,width=iw*scale,height=ih*scale)
 c.setFont('Helvetica',8);c.drawString(25,15,'Captura original aportada por el estudiante');c.drawRightString(W-25,15,str(i));c.showPage()
c.save()
from pypdf import PdfWriter
unificado=PdfWriter()
unificado.append(ROOT/'informe-hallazgos-s8.pdf')
unificado.append(ROOT/'anexo-evidencias-s8.pdf')
unificado.write(ROOT/'Condori_LP2_S8_Autonoma.pdf')
print('Informe, anexo y PDF unificado generados')
