import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ProductoService } from '../../services/producto-service';
import { Producto, OrdenProducto, Direccion } from '../../models/producto.model';
import { CategoriaService } from '../../../categorias/services/categoria-service';
import { Categoria } from '../../../categorias/models/categoria.model';
import { PaginaResponse } from '../../../../core/models/pagina-response';
import { mensajeError } from '../../../../core/utils/http-error';
@Component({selector: 'app-producto-list', imports: [RouterLink, CurrencyPipe], templateUrl: './producto-list.html', styleUrl: './producto-list.css'})
export class ProductoList implements OnInit {
  private readonly service = inject(ProductoService);
  private readonly categoriaService = inject(CategoriaService);
  readonly pagina = signal(0);
  readonly tamanio = signal(10);
  readonly ordenarPor = signal<OrdenProducto>('nombre');
  readonly direccion = signal<Direccion>('asc');
  readonly resultado = signal<PaginaResponse<Producto> | null>(null);
  readonly categorias = signal<Categoria[]>([]);
  readonly categoriaFiltro = signal<number | null>(null);
  readonly cargando = signal(false);
  readonly dandoBaja = signal(false);
  readonly error = signal('');
  readonly errorCategorias = signal('');
  readonly productos = computed(() => {
    const lista = this.resultado()?.contenido ?? [];
    return this.categoriaFiltro() === null ? lista : lista.filter(p => p.categoriaId === this.categoriaFiltro());
  });
  ngOnInit() {
    this.categoriaService.listar().subscribe({next: c => this.categorias.set(c), error: e => this.errorCategorias.set(mensajeError(e))});
    this.cargar();
  }
  cargar() {
    this.cargando.set(true); this.error.set('');
    this.service.listar(this.pagina(), this.tamanio(), this.ordenarPor(), this.direccion()).subscribe({
      next: r => { this.resultado.set(r); this.pagina.set(r.pagina); this.cargando.set(false); },
      error: e => { this.error.set(mensajeError(e)); this.cargando.set(false); }
    });
  }
  irA(pagina: number) { if (this.cargando() || pagina < 0) return; this.pagina.set(pagina); this.cargar(); }
  cambiarTamanio(valor: string) { this.tamanio.set(Number(valor)); this.irA(0); }
  ordenar(campo: OrdenProducto) {
    this.direccion.set(this.ordenarPor() === campo && this.direccion() === 'asc' ? 'desc' : 'asc');
    this.ordenarPor.set(campo); this.irA(0);
  }
  filtrarPorCategoria(valor: string) { this.categoriaFiltro.set(valor ? Number(valor) : null); }
  darDeBaja(producto: Producto) {
    if (!producto.estado || this.dandoBaja() || !confirm(`¿Dar de baja el producto "${producto.nombre}"?`)) return;
    this.dandoBaja.set(true); this.error.set('');
    this.service.darDeBaja(producto.id).subscribe({next: () => { this.dandoBaja.set(false); this.cargar(); }, error: e => { this.dandoBaja.set(false); this.error.set(mensajeError(e)); }});
  }
}
