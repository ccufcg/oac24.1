addi x1, x0, 3       # Carregar base x = 3 em x1
addi x2, x0, 4       # Carregar expoente y = 5 em x2 (mude aqui para testar outros expoentes)
addi x3, x0, 1       # Inicializar resultado (x^0 = 1) em x3
addi x4, x0, 0       # Inicializar contador em x4
loop:
    mul x3, x3, x1   # Multiplica resultado por x (x3 = x3 * x1)
    addi x4, x4, 1   # Incrementa o contador
    beq x4, x2, end
    jal x0, loop     # Salta de volta para o início do loop
end:
    nop              # Instrução de término
