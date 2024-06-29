.global _start

.section .data
filename:   .asciz "numeros.txt"
buffer:     .space 1024       // Espacio para el buffer

.section .bss
sum:        .quad 0           // Variable para la suma

.section .text

_start:
    // Abrir el archivo
    mov x0, filename          // Nombre del archivo
    mov x1, 0                 // O_RDONLY
    mov x8, 56                // sys_open
    svc 0
    mov x19, x0               // Guardar el file descriptor

    // Leer el archivo en el buffer
    mov x0, x19               // File descriptor
    mov x1, buffer            // Dirección del buffer
    mov x2, 1024              // Tamaño del buffer
    mov x8, 63                // sys_read
    svc 0
    mov x20, x0               // Guardar el número de bytes leídos

    // Inicializar punteros y la suma
    mov x21, buffer           // Puntero al inicio del buffer
    mov x22, buffer           // Puntero para recorrer el buffer
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
    mul x23, x23, 10          // Multiplicar por 10 la suma parcial
    add x23, x23, x0          // Agregar el dígito a la suma parcial
    b sum_loop

add_to_sum:
    // Agregar la suma parcial a la suma total
    ldr x0, [sum]
    add x0, x0, x23
    str x0, [sum]

    // Resetear la suma parcial
    mov x23, 0
    b sum_loop

end_sum_loop:
    // Agregar la última suma parcial si no fue procesada
    ldr x0, [sum]
    add x0, x0, x23
    str x0, [sum]

    // Imprimir el resultado
    ldr x0, [sum]
    bl print_number

    // Salir del programa
    mov x8, 93                // sys_exit
    mov x0, 0
    svc 0

print_number:
    // Convertir el número a cadena y escribirlo en stdout
    mov x1, x0                // Número a imprimir
    mov x2, 10                // Base 10
    mov x8, 64                // sys_write
    svc 0
    ret
