import { Component, computed, inject, input, OnInit, signal } from '@angular/core';
import { NonNullableFormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { forkJoin } from 'rxjs';
import { ProductoService } from '../../services/producto-service';
import { CategoriaService } from '../../../categorias/services/categoria-service';
import { Categoria } from '../../../categorias/models/categoria.model';
import { erroresDeValidacion, mensajeError } from '../../../../core/utils/http-error';
@Component({ selector: 'app-producto-form', imports: [ReactiveFormsModule, RouterLink], templateUrl: './producto-form.html', styleUrl: './producto-form.css' })
export class ProductoForm implements OnInit {
  private readonly fb = inject(NonNullableFormBuilder);
  private readonly service = inject(ProductoService);
  private readonly categoriaService = inject(CategoriaService);
  private readonly router = inject(Router);
  readonly id = input<string>();
  readonly categoriaOriginal = signal<number | null>(null);
  readonly erroresServidor = signal<Record<string, string>>({});
  readonly categorias = signal<Categoria[]>([]);
  readonly cargando = signal(true);
  readonly cargaFallida = signal(false);
  readonly guardando = signal(false);
  readonly error = signal('');
  readonly form = this.fb.group({ nombre: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(150), Validators.pattern(/.*\S.*/)]], precio: this.fb.control<number | null>(null, [Validators.required, Validators.min(0.01), Validators.pattern(/^\d+(\.\d{1,2})?$/)]), stock: [0, [Validators.required, Validators.min(0), Validators.pattern(/^\d+$/)]], categoriaId: this.fb.control<number | null>(null, [Validators.required, Validators.min(1), Validators.pattern(/^\d+$/)]), estado: [true] });
  readonly opciones = computed(() => this.categorias().filter(c => c.estado || c.id === this.categoriaOriginal()));
  readonly hayCategoriasActivas = computed(() => this.categorias().some(c => c.estado));
  private readonly categoriaElegida = toSignal(this.form.controls.categoriaId.valueChanges, {initialValue: null});
  readonly categoriaInactiva = computed(() => this.categorias().some(c => c.id === this.categoriaElegida() && !c.estado));
  ngOnInit() {
    const categorias = this.categoriaService.listar();
    if (this.id()) {
      forkJoin({ categorias, producto: this.service.obtener(Number(this.id())) }).subscribe({ next: ({ categorias, producto: p }) => { this.categorias.set(categorias); this.categoriaOriginal.set(p.categoriaId); this.form.setValue({ nombre:p.nombre, precio:p.precio, stock:p.stock, categoriaId:p.categoriaId, estado:p.estado }); this.cargando.set(false); }, error: e => this.fallo(e) });
    } else categorias.subscribe({ next: c => { this.categorias.set(c); this.cargando.set(false); }, error: e => this.fallo(e) });
  }
  private fallo(e: Parameters<typeof mensajeError>[0]) { this.cargando.set(false); this.cargaFallida.set(true); this.error.set(mensajeError(e)); }
  guardar() {
    if (this.cargando() || this.cargaFallida() || this.guardando()) return;
    this.form.controls.nombre.setValue(this.form.controls.nombre.value.trim());
    if (this.form.invalid || this.categoriaInactiva() || !this.hayCategoriasActivas() || !this.categorias().some(c => c.id === this.form.controls.categoriaId.value && c.estado)) { this.form.markAllAsTouched(); return; }
    const v = this.form.getRawValue(); const dto = { ...v, categoriaId: Number(v.categoriaId), precio:Number(v.precio), stock:Number(v.stock) };
    this.guardando.set(true); this.error.set(''); this.erroresServidor.set({});
    (this.id() ? this.service.actualizar(Number(this.id()), dto) : this.service.crear(dto)).subscribe({ next: () => this.router.navigate(['/productos'], { queryParams:{guardado:1} }), error: e => { this.error.set(mensajeError(e)); this.erroresServidor.set(erroresDeValidacion(e)); this.guardando.set(false); } });
  }
}
