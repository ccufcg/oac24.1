addi x3, x0, 1
addi x6, x0, 2
add x7, x3, x6
loop:
    beq x3, x7, fim
    addi x3, x3, 1
    jal x0, loop
fim:
    nop