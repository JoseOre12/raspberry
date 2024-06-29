.global _start

.data
head:
    .quad 0  // Puntero al primer nodo, inicializado a 0 (NULL)

.text
_start:
    // Inicializar x20 con la dirección de head
    ldr x20, =head

    // Crear el primer nodo (valor 3)
    mov x0, 16         // Tamaño del nodo (8 bytes para valor, 8 bytes para puntero)
    mov x8, 214        // Número de syscall para brk (obtener/establecer el final del segmento de datos)
    svc 0              // Llamada al sistema
    mov x19, x0        // Guardar la dirección del nuevo nodo en x19

    mov x1, 3          // Valor del nodo
    str x1, [x19]      // Almacenar el valor en el nodo
    ldr x1, [x20]      // Cargar el valor actual de head
    str x1, [x19, 8]   // Almacenar el puntero al siguiente nodo (actualmente head)
    str x19, [x20]     // Actualizar head para que apunte al nuevo nodo

    // Crear el segundo nodo (valor 2)
    mov x0, 16         // Tamaño del nodo
    mov x8, 214        // Número de syscall para brk
    svc 0
    mov x19, x0        // Guardar la dirección del nuevo nodo en x19

    mov x1, 2          // Valor del nodo
    str x1, [x19]      // Almacenar el valor en el nodo
    ldr x1, [x20]      // Cargar el valor actual de head
    str x1, [x19, 8]   // Almacenar el puntero al siguiente nodo (actualmente head)
    str x19, [x20]     // Actualizar head para que apunte al nuevo nodo

    // Crear el tercer nodo (valor 1)
    mov x0, 16         // Tamaño del nodo
    mov x8, 214        // Número de syscall para brk
    svc 0
    mov x19, x0        // Guardar la dirección del nuevo nodo en x19

    mov x1, 1          // Valor del nodo
    str x1, [x19]      // Almacenar el valor en el nodo
    ldr x1, [x20]      // Cargar el valor actual de head
    str x1, [x19, 8]   // Almacenar el puntero al siguiente nodo (actualmente head)
    str x19, [x20]     // Actualizar head para que apunte al nuevo nodo

    // Salir del programa
    mov x0, 0          // Código de salida
    mov x8, 93         // Número de syscall para exit
    svc 0