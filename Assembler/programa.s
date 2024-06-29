.global _start

.section .data
filename:   .asciz "numeros.txt"
buffer:     .space 1024       // Espacio para el buffer

.section .bss
head:       .xword 0          // Puntero al primer nodo de la lista
sum:        .xword 0          // Variable para la suma

.section .text

_start:
    // Abrir el archivo
    ldr x0, =filename         // Nombre del archivo
    mov x1, 0                 // O_RDONLY
    mov x8, 56                // sys_open
    svc 0
    mov x19, x0               // Guardar el file descriptor

    // Leer el archivo en el buffer
    mov x0, x19               // File descriptor
    ldr x1, =buffer           // Dirección del buffer
    mov x2, 1024              // Tamaño del buffer
    mov x8, 63                // sys_read
    svc 0
    mov x20, x0               // Guardar el número de bytes leídos

    // Convertir los datos del buffer en números y agregar a la lista
    ldr x21, =buffer          // Puntero al inicio del buffer
    add x22, x21, x20         // Puntero al final del buffer

read_loop:
    cmp x21, x22              // Verificar si hemos llegado al final del buffer
    b.ge end_read_loop

    ldrb w0, [x21], #1        // Leer el siguiente byte del buffer
    cmp w0, 10                // Verificar si es un salto de línea (ASCII 10)
    b.eq read_loop            // Si es un salto de línea, continuar leyendo

    sub w0, w0, 48            // Convertir carácter ASCII a número
    bl insert_beginning       // Insertar el número en la lista
    b read_loop

end_read_loop:
    // Calcular la suma de los números en la lista
    ldr x0, =head
    ldr x0, [x0]
    mov x23, 0                // Variable para la suma
sum_loop:
    cmp x0, 0
    beq end_sum_loop

    ldr x1, [x0]              // Cargar el valor del nodo actual
    add x23, x23, x1          // Sumar al total
    ldr x0, [x0, #8]          // Cargar el siguiente nodo
    b sum_loop

end_sum_loop:
    // Almacenar la suma en la variable global 'sum'
    ldr x0, =sum
    str x23, [x0]

    // Imprimir la suma
    ldr x0, =sum
    bl print_number

    // Salir del programa
    mov x8, 93                // sys_exit
    mov x0, 0
    svc 0

print_number:
    // Convertir el número a cadena y escribirlo en stdout
    mov x1, x0                // Número a imprimir
    bl itoa                   // Llamar a la función itoa
    ldr x1, =buffer           // Dirección del buffer con el número convertido
    mov x2, #32               // Longitud máxima del número
    mov x8, 64                // sys_write
    svc 0
    ret

itoa:
    // Convertir un número a cadena (itoa)
    mov x2, x0                // Guardar el número original en x2
    add x0, x1, #32           // Dirección del buffer + 32
    mov x3, #0                // Contador de dígitos

itoa_loop:
    udiv x4, x2, x1           // Dividir el número por 10
    msub x5, x2, x4, x1, 10   // Calcular el residuo (residuo = x2 - (x4 * 10))
    add x5, x5, 48            // Convertir el residuo a carácter ASCII
    strb w5, [x0, -1]!        // Almacenar el carácter en el buffer
    mov x2, x4                // Actualizar el número
    add x3, x3, 1             // Incrementar el contador de dígitos
    cmp x2, 0                 // Comparar con 0
    b.ne itoa_loop            // Si no es 0, continuar

    // Invertir la cadena
    mov x1, x0                // Dirección del buffer
    sub x1, x1, x3            // Ajustar la dirección al inicio de la cadena
    ret

insert_beginning:
    // Función para insertar un nuevo nodo al principio de la lista
    stp x0, x1, [sp, #-16]!
    mov x1, x0                // Valor a insertar

    // Reservar memoria para el nuevo nodo
    ldr x0, =16               // Tamaño del nodo (8 bytes para el valor + 8 bytes para el puntero)
    bl malloc                 // Llamar a la función malloc para reservar memoria

    // Eax ahora contiene la dirección del nuevo nodo
    mov x24, x0               // Guardar en x24 para manipulación

    // Almacenar el valor en el nuevo nodo
    str x1, [x24]             // Guardar el valor en el campo 'valor'

    // Establecer el puntero al siguiente nodo (head)
    ldr x0, =head
    ldr x0, [x0]
    str x0, [x24, #8]         // El nuevo nodo apunta al nodo anterior 'head'

    // Actualizar head para que apunte al nuevo nodo
    ldr x0, =head
    str x24, [x0]

    ldp x0, x1, [sp], #16
    ret

malloc:
    // Función malloc para reservar memoria dinámica
    mov x0, x1                // Argumento: tamaño en x1
    mov x8, 64                // sys_brk (cambiar a sys_mmap si es necesario)
    svc 0
    ret
