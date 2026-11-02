// Incluir la API de tensores de ATen y los tipos internos que se inspeccionan.
#include <ATen/ATen.h>
#include <c10/core/Storage.h>
#include <c10/core/TensorImpl.h>
#include <c10/core/impl/SizesAndStrides.h>
#include <iostream>

/**
 * Inspecciona tamaños de tipos y propiedad de datos de esta compilación.
 *
 * No presupone offsets privados ni dereferencia direcciones de otro proceso.
 * Los valores de sizeof y alignof son resultados del compilador y ABI usados.
 *
 * @return Cero cuando la inspección termina correctamente.
 */
int main() {
    // Crear un tensor denso float32 de CPU con seis valores.
    at::Tensor tensor = at::arange(6, at::TensorOptions().dtype(at::kFloat)).reshape({2, 3});
    // Conservar un handle del almacenamiento mientras se inspecciona su DataPtr.
    c10::Storage storage = tensor.storage();
    // Obtener una referencia; DataPtr representa propiedad única y no se copia aquí.
    const c10::DataPtr& dataptr = storage.data_ptr();
    // Medir los tipos de esta compilación, sin presentarlos como constantes portables.
    std::cout << "sizeof(at::Tensor) = " << sizeof(at::Tensor) << "\n";
    std::cout << "sizeof(c10::TensorImpl) = " << sizeof(c10::TensorImpl) << "\n";
    std::cout << "sizeof(c10::StorageImpl) = " << sizeof(c10::StorageImpl) << "\n";
    std::cout << "sizeof(c10::DataPtr) = " << sizeof(c10::DataPtr) << "\n";
    std::cout << "alignof(c10::DataPtr) = " << alignof(c10::DataPtr) << "\n";
    std::cout << "sizeof(SizesAndStrides) = " << sizeof(c10::impl::SizesAndStrides) << "\n";
    // Mostrar propiedades públicas del almacenamiento y del puntero de datos.
    std::cout << "Bytes de datos = " << storage.nbytes() << "\n";
    std::cout << "Dispositivo = " << dataptr.device() << "\n";
    std::cout << "Contexto presente = " << (dataptr.get_context() != nullptr) << "\n";
    // Obtener otra vista y comprobar que apunta al mismo bloque.
    at::Tensor vista = tensor.transpose(0, 1);
    std::cout << "Vista comparte bloque = " << (vista.storage().data_ptr().get() == dataptr.get()) << "\n";
    // Indicar que el programa terminó sin errores.
    return 0;
}
