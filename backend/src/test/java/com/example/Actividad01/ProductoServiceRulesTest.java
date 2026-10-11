package com.example.Actividad01;
import com.example.Actividad01.entity.*;
import com.example.Actividad01.dto.ProductoRequestDTO;
import com.example.Actividad01.repository.*;
import com.example.Actividad01.service.impl.ProductoServiceImpl;
import com.example.Actividad01.exception.ReglaNegocioException;
import com.example.Actividad01.exception.RecursosNoEncontradoException;
import org.junit.jupiter.api.Test;
import java.util.Optional;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
class ProductoServiceRulesTest {
 final ProductoRepository productos=mock(ProductoRepository.class);
 final CategoriaRepository categorias=mock(CategoriaRepository.class);
 final ProductoServiceImpl service=new ProductoServiceImpl(productos,categorias);
 final ProductoRequestDTO dto=new ProductoRequestDTO("Producto",new BigDecimal("1.00"),1,true,2L);
 @Test void impideCategoriaInactiva(){Categoria c=new Categoria();c.setEstado(false);when(categorias.findById(2L)).thenReturn(Optional.of(c));assertThrows(ReglaNegocioException.class,()->service.create(dto));verify(productos,never()).save(any());}
 @Test void inexistenteProduce404(){assertThrows(RecursosNoEncontradoException.class,()->service.create(dto));}
 @Test void bajaLogicaYConflicto(){Producto p=new Producto();p.setEstado(true);when(productos.findById(1L)).thenReturn(Optional.of(p));service.delete(1L);assertFalse(p.getEstado());verify(productos).save(p);verify(productos,never()).delete(any());assertThrows(ReglaNegocioException.class,()->service.delete(1L));}
 @Test void ordenNoPermitido(){assertThrows(ReglaNegocioException.class,()->service.listar(0,10,"categoria","asc"));verifyNoInteractions(productos);}
 @Test void nombreDuplicado(){when(productos.existsByNombreIgnoreCase("Producto")).thenReturn(true);assertThrows(ReglaNegocioException.class,()->service.create(dto));verifyNoInteractions(categorias);}
}
