.section .data
segmento:   .asciz "Segmento de datos\n"

.section .bss
head:       .long 0            @ Puntero al primer nodo de la lista

.section .text
.global _start

_start:
    @ Inicializar el puntero head a NULL (0)
    mov x0, #0
    str x0, [head]

    @ Ingresar los valores [3, 2, 1] a la lista (simulando una pila)
    mov x0, #3
    bl insert_beginning
    mov x0, #2
    bl insert_beginning
    mov x0, #1
    bl insert_beginning

    @ Imprimir la lista
    bl print_list

    @ Salir del programa
    mov x8, 93          @ Código de salida (sys_exit)
    mov x0, 0           @ Código de error (0)
    svc 0

@ Función para insertar un nuevo nodo al principio de la lista
insert_beginning:
    push {lr}           @ Guardar el registro de enlace (lr)

    @ Llamar a malloc para reservar memoria para el nuevo nodo
    mov x1, #8          @ Tamaño del nodo (4 bytes para el valor + 4 bytes para el puntero)
    bl malloc           @ Llamar a la función malloc

    @ Eax ahora contiene la dirección del nuevo nodo
    mov x3, x0          @ Guardar en x3 para manipulación

    @ Almacenar el valor en el nuevo nodo
    str x0, [x3]        @ Guardar el valor en el campo 'valor'

    @ Establecer el puntero al siguiente nodo (head)
    ldr x0, [head]
    str x0, [x3, #4]    @ El nuevo nodo apunta al nodo anterior 'head'

    @ Actualizar head para que apunte al nuevo nodo
    str x3, [head]

    pop {lr}            @ Restaurar el registro de enlace
    ret                 @ Volver

@ Función para imprimir la lista
print_list:
    push {lr}           @ Guardar el registro de enlace (lr)

    ldr x0, [head]
    cmp x0, #0          @ Verificar si head es NULL
    beq end_print       @ Si es NULL, la lista está vacía y terminar

.print_loop:
    @ Imprimir el valor del nodo actual
    ldr x0, [x0]        @ Cargar el valor del nodo actual
    ldr x1, =segmento
    add x1, x1, x0      @ Preparar el puntero a la cadena para imprimir
    bl printf           @ Llamar a printf para imprimir el valor

    @ Mover al siguiente nodo
    ldr x0, [x0, #4]    @ Cargar el puntero al siguiente nodo
    cmp x0, #0
    bne .print_loop     @ Si no es NULL, continuar imprimiendo

.end_print:
    pop {lr}            @ Restaurar el registro de enlace
    ret                 @ Volver

@ Función malloc para reservar memoria dinámica
@ Implementación simple de malloc para este ejemplo
malloc:
    mov x8, #0          @ Código de llamada al sistema para brk (sys_brk)
    svc 0               @ Llamar al sistema para incrementar el tamaño del espacio de datos

    ret                 @ Retornar el nuevo puntero a la memoria
