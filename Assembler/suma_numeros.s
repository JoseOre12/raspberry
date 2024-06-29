.data
filename:   .asciz "numbers.txt"
buffer:     .space 1024
result:     .asciz "La suma es: %d\n"

.text
.global main

main:
    push {ip, lr}

    @ Abrir el archivo
    ldr r0, =filename
    mov r1, #0          @ modo de lectura
    bl fopen
    mov r4, r0          @ guardar el puntero del archivo

    @ Leer el archivo en el buffer
    ldr r1, =buffer
    mov r2, #1024
    mov r0, r4
    bl fread

    @ Cerrar el archivo
    mov r0, r4
    bl fclose

    @ Inicializar variables
    ldr r4, =buffer
    mov r5, #0          @ suma total
    mov r6, #0          @ número actual

loop:
    ldrb r0, [r4], #1   @ cargar byte y avanzar puntero
    cmp r0, #0          @ comprobar fin de archivo
    beq end_loop

    cmp r0, #'\n'       @ comprobar fin de línea
    beq end_number

    sub r0, r0, #'0'    @ convertir ASCII a número
    mov r1, r6
    mov r2, #10
    mul r6, r1, r2      @ multiplicar número actual por 10
    add r6, r6, r0      @ añadir nuevo dígito

    b loop

end_number:
    add r5, r5, r6      @ añadir número a la suma total
    mov r6, #0          @ reiniciar número actual
    b loop

end_loop:
    @ Imprimir resultado
    ldr r0, =result
    mov r1, r5
    bl printf

    @ Salir
    mov r0, #0
    pop {ip, pc}