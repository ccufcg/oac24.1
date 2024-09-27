addi x1, x0, 5 #atribui 5 ao registrador x1
addi x2, x0, 1 #atribui 1 ao registrador x2
loop: #loop enquanto o registrador x1 for maior que x0
    beq x1, x0, fim #sai do loop se x1 = x0
    add x2, x2, x1 #soma x2 com x1
    addi x1, x1, -1 #subtrai 1 de x1 para poder sair do loop quando chegar em 0
    jal x0, loop #salta para o início do loop
fim: #programa encerra quando x1 = x0
    nop
