# Exemplo de código assembly para calcular potenciação: x^y

# Inicializando os valores
addi x1, x0, 3       # Carregar base x = 3 em x1
addi x2, x0, 4       # Carregar expoente y = 4 em x2
addi x3, x0, 1       # Inicializar resultado (x^0 = 1) em x3
add x4, x0, x2       # Inicializar contador em x4
 
# Loop para calcular x^y
loop:
    mul x3, x3, x1   # Multiplica resultado por x (x3 = x3 * x1)
    jal x0, loop     # Salta de volta para o início do loop
    beq x2, x4, end  # Se o contador (x4) == expoente (x2), salta para 'end'

# Rótulo de término do loop
end:
    nop              # Instrução de término
