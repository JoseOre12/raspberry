.global _start

.data
    points:     .quad 1, 1, 1, 3, 2, 1, 3, 5, 4, 5, 5, 5, 5, 3  // Los puntos como enteros
    num_points: .quad 7
    k:          .quad 2
    centroids:  .quad 0, 0, 0, 0  // Espacio para 2 centroides
    clusters:   .quad 0, 0, 0, 0, 0, 0, 0  // Asignación de cluster para cada punto
    temp:       .quad 0, 0  // Espacio temporal para cálculos

.text
_start:
    // Inicializar centroides
    bl initialize_centroids

    // Bucle principal de K-means
kmeans_loop:
    // Asignar puntos a centroides
    bl assign_points

    // Actualizar centroides
    bl update_centroids

    // Comprobar convergencia (simplificado: siempre hace 5 iteraciones)
    sub x21, x21, #1
    cbnz x21, kmeans_loop

    // Imprimir resultados
    bl print_results

    // Salir del programa
    mov x0, 0
    mov x8, 93  // syscall exit
    svc 0

initialize_centroids:
    // Inicializar centroides con los dos primeros puntos
    ldr x0, =points
    ldr x1, =centroids
    ldp x2, x3, [x0]
    stp x2, x3, [x1]
    ldp x2, x3, [x0, #16]
    stp x2, x3, [x1, #16]
    mov x21, #5  // Contador para el número de iteraciones
    ret

assign_points:
    ldr x0, =points
    ldr x1, =centroids
    ldr x2, =clusters
    ldr x3, =num_points
    ldr x3, [x3]
    mov x4, #0  // Índice del punto actual

assign_loop:
    // Cargar punto actual
    lsl x5, x4, #4
    ldp x5, x6, [x0, x5]
    
    // Calcular distancia al primer centroide
    ldp x7, x8, [x1]
    sub x9, x5, x7
    mul x9, x9, x9
    sub x10, x6, x8
    mul x10, x10, x10
    add x11, x9, x10  // Distancia^2 al primer centroide
    
    // Calcular distancia al segundo centroide
    ldp x7, x8, [x1, #16]
    sub x9, x5, x7
    mul x9, x9, x9
    sub x10, x6, x8
    mul x10, x10, x10
    add x12, x9, x10  // Distancia^2 al segundo centroide
    
    // Comparar distancias y asignar cluster
    cmp x11, x12
    csel x13, xzr, x3, lt  // 0 si más cerca del primer centroide, 1 si más cerca del segundo
    str x13, [x2, x4, lsl #3]
    
    add x4, x4, #1
    cmp x4, x3
    b.lt assign_loop
    
    ret

update_centroids:
    ldr x0, =points
    ldr x1, =centroids
    ldr x2, =clusters
    ldr x3, =num_points
    ldr x3, [x3]
    
    // Reiniciar centroides y contadores
    mov x4, xzr
    mov x5, xzr
    mov x6, xzr
    mov x7, xzr
    mov x8, xzr
    mov x9, xzr
    
    mov x10, #0  // Índice del punto actual

update_loop:
    ldr x11, [x2, x10, lsl #3]  // Cargar cluster del punto
    lsl x12, x10, #4
    ldp x12, x13, [x0, x12]  // Cargar coordenadas del punto
    
    cmp x11, #0
    b.ne second_centroid
    
    // Actualizar primer centroide
    add x4, x4, x12
    add x5, x5, x13
    add x8, x8, #1
    b continue_update

second_centroid:
    // Actualizar segundo centroide
    add x6, x6, x12
    add x7, x7, x13
    add x9, x9, #1

continue_update:
    add x10, x10, #1
    cmp x10, x3
    b.lt update_loop
    
    // Calcular nuevos centroides (división entera)
    udiv x4, x4, x8
    udiv x5, x5, x8
    udiv x6, x6, x9
    udiv x7, x7, x9
    
    // Guardar nuevos centroides
    stp x4, x5, [x1]
    stp x6, x7, [x1, #16]
    
    ret

print_results:
    // Esta función es un placeholder. En un sistema real, necesitarías
    // implementar la lógica para imprimir los resultados, probablemente
    // usando syscalls para escribir en stdout.
    ret