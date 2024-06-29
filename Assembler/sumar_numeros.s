.global _start

.section .data
filename:   .asciz "numeros.txt"
buffer:     .space 1024       // Espacio para el buffer

.section .bss
sum:        .quad 0           // Variable para la suma

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

    // Inicializar punteros y la suma
    ldr x21, =buffer          // Puntero al inicio del buffer
    mov x22, x21              // Puntero para recorrer el buffer
    mov x23, 0                // Variable para la suma parcial

sum_loop:
    // Verificar si hemos terminado de leer el buffer
    cmp x22, x21
    b.ge end_sum_loop

    // Leer el siguiente byte
    ldrb w0, [x22]
    add x22, x22, 1

    // Verificar si es un salto de línea (ASCII 10)
    cmp w0, 10
    b.eq add_to_sum

    // Convertir el carácter ASCII a número y agregar a la suma parcial
    sub w0, w0, 48
    mov x1, 10
    mul x23, x23, x1          // Multiplicar por 10 la suma parcial
    add x23, x23, x0          // Agregar el dígito a la suma parcial
    b sum_loop

add_to_sum:
    // Agregar la suma parcial a la suma total
    ldr x0, [x21, sum]
    add x0, x0, x23
    str x0, [x21, sum]

    // Resetear la suma parcial
    mov x23, 0
    b sum_loop

end_sum_loop:
    // Agregar la última suma parcial si no fue procesada
    ldr x0, [x21, sum]
    add x0, x0, x23
    str x0, [x21, sum]

    // Imprimir el resultado
    ldr x0, [x21, sum]
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
    msub x5, x1, x4, x2, x4   // Calcular el residuo (residuo = x2 - (x4 * x1))
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
