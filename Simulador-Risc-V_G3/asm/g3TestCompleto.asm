# Inicializa registradores com valores imediatos usando addi
addi x0, x0, 56    # x2 = 56         1
addi x2, x0, 9    # x2 = 9           2
addi x3, x0, 55   # x3 = 55          3
# Inicializa x1 com 4
addi x1, x0, 10    # x1 = 10         4
# Inicializa x3 com 3
addi x3, x0, 3    # x3 = 3           5

# Operações com add e sub
add x4, x2, x1    # x4 = x2 + x1 (x4 = 9 + 4 = 13)   6
sub x5, x3, x1    # x5 = x3 - x1 (x5 = 3 - 10 = -7)  7

# Operações lógicas AND e OR
and x6, x2, x3    # x6 = x2 AND x3 (bitwise AND)     8
or x7, x2, x3     # x7 = x2 OR x3 (bitwise OR)       9

# Operação lógica com valor imediato usando ANDI
andi x1, x2, 7    # x8 = x2 AND 7 (bitwise AND com valor imediato) 10

#Salvando na memoria
sd x1, x2 #11
sd x5, x4 #quebra sd
sd x4, x5  #12

#Carregando da memória
ld x4, x5 #13

# Operação lógica com valor imediato Negativo usando ANDI
andi x1, x2, -7    # x8 = x2 AND 7 (bitwise AND com valor imediato) 14

jal x0, save         #15
loop:
    beq x3, x7, fim   #16
    addi x3, x3, 1    #17
    jal x0, loop      #18
save:
    addi x3, x0, 1    #19
    addi x6, x0, 2    #20
    add x7, x3, x6    #21
    jal x0, loop      #22
fim:
    nop               #23