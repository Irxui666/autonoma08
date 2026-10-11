import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ProductoList } from './producto-list';
describe('ProductoList: consultas y baja', () => {
 beforeEach(()=>TestBed.configureTestingModule({imports:[ProductoList],providers:[provideRouter([]),provideHttpClient(),provideHttpClientTesting()]}));
 afterEach(()=>{TestBed.inject(HttpTestingController).verify();vi.restoreAllMocks();});
 it('recibe la categoría y consulta los primeros cien productos',()=>{
 const fixture=TestBed.createComponent(ProductoList);fixture.componentRef.setInput('categoriaId','2');fixture.detectChanges();
 const http=TestBed.inject(HttpTestingController);
 http.expectOne(r=>r.url.endsWith('/categorias')).flush([{id:2,nombre:'Prueba',estado:true}]);
 http.expectOne(r=>r.url.endsWith('/productos') && r.params.get('tamanio')==='100' && r.params.get('pagina')==='0').flush({contenido:[{id:1,nombre:'Visible',precio:1,stock:1,estado:true,categoriaId:2,categoriaNombre:'Prueba'},{id:2,nombre:'Otra',precio:1,stock:1,estado:true,categoriaId:3,categoriaNombre:'Otra'}],pagina:0,totalPaginas:1,totalElementos:2,ultima:true});
 fixture.detectChanges();expect(fixture.componentInstance.productos().map(p=>p.nombre)).toEqual(['Visible']);
 expect(fixture.nativeElement.querySelector('select').value).toBe('2');expect(fixture.nativeElement.textContent).toContain('Mostrando productos de la categoría Prueba en los primeros 100 registros');
 });
 it('ignora un identificador de categoría inválido',()=>{
 const fixture=TestBed.createComponent(ProductoList);fixture.componentRef.setInput('categoriaId','incorrecto');fixture.detectChanges();
 const http=TestBed.inject(HttpTestingController);http.expectOne(r=>r.url.endsWith('/categorias')).flush([]);
 http.expectOne(r=>r.url.endsWith('/productos') && r.params.get('tamanio')==='10').flush({contenido:[],pagina:0,totalPaginas:0,totalElementos:0,ultima:true});
 expect(fixture.componentInstance.categoriaFiltro()).toBeNull();
 });
 it('ordena, pagina y filtra localmente; recarga después de baja',()=>{
 const c=TestBed.createComponent(ProductoList).componentInstance;const http=TestBed.inject(HttpTestingController);
 const p={id:1,nombre:'Producto',precio:1,stock:3,estado:true,categoriaId:1,categoriaNombre:'Activa',fechaCreacion:'',fechaModificacion:null};
 c.ordenar('precio');http.expectOne(r=>r.params.get('ordenarPor')==='precio' && r.params.get('direccion')==='asc').flush({contenido:[p],pagina:0,totalPaginas:2,totalElementos:6,ultima:false});
 c.filtrarPorCategoria('2');expect(c.productos()).toEqual([]);c.filtrarPorCategoria('1');expect(c.productos()).toEqual([p]);
 c.ordenar('precio');http.expectOne(r=>r.params.get('direccion')==='desc').flush({contenido:[p],pagina:0,totalPaginas:2,ultima:false});
 c.cambiarTamanio('5');http.expectOne(r=>r.params.get('tamanio')==='5' && r.params.get('pagina')==='0').flush({contenido:[p],pagina:0,ultima:false});
 c.irA(1);http.expectOne(r=>r.params.get('pagina')==='1').flush({contenido:[p],pagina:1,ultima:true});
 vi.spyOn(window,'confirm').mockReturnValue(true);c.darDeBaja(p);http.expectOne(r=>r.method==='DELETE').flush(null,{status:204,statusText:'No Content'});
 http.expectOne(r=>r.method==='GET').flush({contenido:[{...p,estado:false}],pagina:1,ultima:true});expect(c.productos()[0].estado).toBe(false);
 c.darDeBaja({...p,estado:false});http.expectNone(r=>r.method==='DELETE');
 });
});
