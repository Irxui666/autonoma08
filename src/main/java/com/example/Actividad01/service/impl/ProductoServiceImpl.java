package com.example.Actividad01.service.impl;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.example.Actividad01.dto.ProductoRequestDTO;
import com.example.Actividad01.dto.ProductoResponseDTO;
import com.example.Actividad01.entity.Categoria;
import com.example.Actividad01.entity.Producto;
import com.example.Actividad01.exception.RecursosNoEncontradoException;
import com.example.Actividad01.exception.ReglaNegocioException;
import com.example.Actividad01.repository.CategoriaRepository;
import com.example.Actividad01.repository.ProductoRepository;
import com.example.Actividad01.service.service.ProductoService;

@Service
public class ProductoServiceImpl implements ProductoService{
    private static final Logger LOG = LoggerFactory.getLogger(ProductoServiceImpl.class);

    private final ProductoRepository productoRepository;
    private final CategoriaRepository categoriaRepository;

    public ProductoServiceImpl(ProductoRepository productoRepository,
                               CategoriaRepository categoriaRepository) {
        this.productoRepository = productoRepository;
        this.categoriaRepository = categoriaRepository;
    }

    @Override
    @Transactional
    public ProductoResponseDTO create(ProductoRequestDTO t) {
        String nombre = t.getNombre().trim();
        if(productoRepository.existsByNombreIgnoreCase(nombre)){
            throw new ReglaNegocioException(
                    "Ya existe un producto con el nombre "+ nombre
            );
        }

        Categoria categoria = buscarCategoria(t.getCategoriaId());

        Producto producto = new Producto();
        producto.setNombre(nombre);
        producto.setPrecio(t.getPrecio());
        producto.setStock(t.getStock());
        producto.setEstado(t.getEstado());
        producto.setCategoria(categoria);

        Producto prodCreado = productoRepository.save(producto);

        return convertirResponse(prodCreado);
    }

    @Override
    @Transactional
    public ProductoResponseDTO update(Long aLong, ProductoRequestDTO t) {
        Producto producto = productoRepository.findById(aLong).orElseThrow(()->
                new RecursosNoEncontradoException(
                        "Producto no encontrado con id: "+ aLong
                )
        );

        String nombre = t.getNombre().trim();
        if(productoRepository.existsByNombreIgnoreCaseAndIdNot(nombre, aLong)){
            throw new ReglaNegocioException(
                    "Ya existe un producto con el nombre "+ nombre
            );
        }

        Categoria categoria = buscarCategoria(t.getCategoriaId());

        producto.setNombre(nombre);
        producto.setPrecio(t.getPrecio());
        producto.setStock(t.getStock());
        producto.setEstado(t.getEstado());
        producto.setCategoria(categoria);

        Producto prodActualizado = productoRepository.saveAndFlush(producto);

        return convertirResponse(prodActualizado);
    }

    @Override
    @Transactional(readOnly = true)
    public ProductoResponseDTO read(Long aLong) {
        Producto producto = productoRepository.findById(aLong)
                .orElseThrow(()->
                        new RecursosNoEncontradoException(
                                "Producto no encontrado con id: "+ aLong
                        )
                );
        return convertirResponse(producto);
    }

    @Override
    @Transactional
    public void delete(Long aLong) {
        Producto producto = productoRepository.findById(aLong).orElseThrow(()->
                new RecursosNoEncontradoException(
                        "Producto no encontrado con id: "+ aLong
                )
        );
        if (!Boolean.TRUE.equals(producto.getEstado()))
            throw new ReglaNegocioException("El producto ya está inactivo");
        producto.setEstado(false);
        productoRepository.save(producto);
    }

    @Override
    @Transactional(readOnly = true)
    public Iterable<ProductoResponseDTO> readAll() {
        return productoRepository.findAll()
                .stream()
                .map(this::convertirResponse)
                .toList();
    }

    @Override
    @Transactional(readOnly = true)
    public com.example.Actividad01.dto.PaginaResponseDTO<ProductoResponseDTO> listar(int pagina, int tamanio, String ordenarPor, String direccion) {
        if (!java.util.Set.of("id", "nombre", "precio", "stock").contains(ordenarPor))
            throw new ReglaNegocioException("Campo de orden no permitido: " + ordenarPor);
        if (pagina < 0 || tamanio < 1 || tamanio > 100 || !("asc".equals(direccion) || "desc".equals(direccion)))
            throw new ReglaNegocioException("Parámetros de paginación inválidos");
        var sort = org.springframework.data.domain.Sort.by(org.springframework.data.domain.Sort.Direction.fromString(direccion), ordenarPor).and(org.springframework.data.domain.Sort.by("id"));
        var page = productoRepository.findAll(org.springframework.data.domain.PageRequest.of(pagina, tamanio, sort)).map(this::convertirResponse);
        return com.example.Actividad01.dto.PaginaResponseDTO.from(page);
    }

    private Categoria buscarCategoria(Long categoriaId){
        Categoria categoria = categoriaRepository.findById(categoriaId).orElseThrow(() ->
                new RecursosNoEncontradoException("Categoria no encontrada con id: " + categoriaId));
        if (!Boolean.TRUE.equals(categoria.getEstado()))
            throw new ReglaNegocioException("La categoría elegida está inactiva. Elija una categoría activa.");
        return categoria;
    }

    private ProductoResponseDTO convertirResponse(Producto producto){
        return new ProductoResponseDTO(
                producto.getId(),
                producto.getNombre(),
                producto.getPrecio(),
                producto.getStock(),
                producto.getEstado(),
                producto.getCategoria().getId(),
                producto.getCategoria().getNombre(),
                producto.getFechaCreacion(),
                producto.getFechaModificacion()
        );
    }
}
