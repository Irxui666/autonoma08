import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ProductoForm } from './producto-form';
describe('ProductoForm: dependencias', () => {
  beforeEach(() => TestBed.configureTestingModule({imports:[ProductoForm],providers:[provideRouter([]),provideHttpClient(),provideHttpClientTesting()]}));
  afterEach(() => TestBed.inject(HttpTestingController).verify());
  const categorias=[{id:1,nombre:'Activa',estado:true},{id:2,nombre:'Inactiva',estado:false}];
  it('ofrece solo activas y envía categoriaId numérico', () => {
    const fixture=TestBed.createComponent(ProductoForm); const c=fixture.componentInstance; fixture.detectChanges();
    const http=TestBed.inject(HttpTestingController);http.expectOne('/api/v1/categorias').flush(categorias);
    expect(c.opciones().map(x=>x.id)).toEqual([1]);
    c.guardar();http.expectNone('/api/v1/productos');
    c.form.setValue({nombre:'Paracetamol',precio:2.5,stock:10,estado:true,categoriaId:1});c.guardar();
    const req=http.expectOne('/api/v1/productos');expect(req.request.body.categoriaId).toBe(1);expect(req.request.body.categoria).toBeUndefined();
    req.flush({message:'Nombre repetido'},{status:409,statusText:'Conflict'});expect(c.error()).toBe('Nombre repetido');expect(c.guardando()).toBe(false);
  });
  it('precarga original inactiva y no permite guardarla', () => {
    const fixture=TestBed.createComponent(ProductoForm);fixture.componentRef.setInput('id','3');fixture.detectChanges();const c=fixture.componentInstance;const http=TestBed.inject(HttpTestingController);
    http.expectOne('/api/v1/productos/3').flush({nombre:'Producto',precio:1,stock:0,estado:true,categoriaId:2});
    expect(c.cargando()).toBe(true);http.expectOne('/api/v1/categorias').flush(categorias);
    expect(c.opciones().map(x=>x.id)).toEqual([1,2]);expect(c.categoriaInactiva()).toBe(true);c.guardar();http.expectNone(r=>r.method==='PUT');
    c.form.controls.categoriaId.setValue(1);c.guardar();const req=http.expectOne(r=>r.method==='PUT');expect(req.request.body.categoriaId).toBe(1);req.flush({message:'Fallo temporal'},{status:400,statusText:'Bad Request'});
  });
  it('sin categorías activas no envía altas', () => {
    const fixture=TestBed.createComponent(ProductoForm);fixture.detectChanges();const c=fixture.componentInstance;const http=TestBed.inject(HttpTestingController);http.expectOne('/api/v1/categorias').flush([categorias[1]]);
    expect(c.hayCategoriasActivas()).toBe(false);c.guardar();http.expectNone('/api/v1/productos');
  });
});
