#Carrega o valor N da memória (endereço de memória 1024) para o registrador x2
addi x2, x0, 1
addi x3, x0, 55
#Inicializa x1 com 4
addi x1, x0, 4
# Inicializa o resultado em x3 com imd
addi x3, x3, 5
# Incrementa x1 em 1
addi x1, x1, 1
add x4, x2, x1
#modificações com memória
sd x3, x2
sd x1, x4
ld x7, x2
nop
