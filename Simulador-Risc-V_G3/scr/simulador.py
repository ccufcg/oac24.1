import sys

run = 1
pc = 0
memoria = [0] * 128
registradores = [0] * 8

#Simulador executa as operações da arquivo binario com base no pc atual enquanto não atingir criterio de parada
def simulador(Operacoes):
    global run, pc
    
    limite_pc = len(Operacoes)
    
    while run == 1 and pc < limite_pc:
        opcode = Operacoes[pc][0]
        pc_anterior = pc
        texto_execução = executa(Operacoes[pc], opcode)
        pc += 1
        
        print(f'PC = {pc_anterior}, {texto_execução}')
    
    print(f"PC final: {pc_anterior}")
    print(f"Registradores: {registradores}")
    print(f"Memoria: {memoria}")

#Executa o binario e trata criterios de parada
def executa(operacao, opcode):
    global run, registradores, pc, memoria
                
    if opcode == "0110011":  # add, sub, or, and
        opcode, rd, func3, rs1, rs2, func7 = operacao

        rd = int(rd, 2)
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)

        op = indentificaOpR(func3 + func7)
        #Sem atribuição
        if rd == 0:
            return f"`{op} em r0 = 0/ r0 Constante em 0"
        #add
        elif func3 == "000" and func7 == "0000000":
            registradores[rd] = registradores[rs1] + registradores[rs2]
            return (f"{op} x{rd} = x{rs1} + x{rs2}")
        #sub
        elif func3 == "000" and func7 == "0100000":
            registradores[rd] = registradores[rs1] - registradores[rs2]
            return (f"{op} x{rd} = x{rs1} - x{rs2}")
        #and
        elif func3 == "111" and func7 == "0000000":
            registradores[rd] = registradores[rs1] & registradores[rs2]
            return (f"{op} x{rd} = x{rs1} & x{rs2}")
        #or
        elif func3 == "110" and func7 == "0000000":
            registradores[rd] = registradores[rs1] | registradores[rs2]
            return (f"{op} x{rd} = x{rs1} | x{rs2}")
        else:
            return  f"{op} Invalido(a), função não reconhecida \OPCODE valido para add, sub, or, and"
        
    elif opcode == "0010011":  # addi, andi, nop
        opcode, rd, func3, rs1, imd = operacao

        rd = int(rd, 2)
        rs1 = int(rs1, 2)
        imd = complemento2(imd)

        op = indentificaOpIMD(func3)
        #Sem atribuicao
        if rd == 0:
            return f"{op} em r0 = 0/ r0 Constante em 0"
        #addi << nop
        elif func3 == "000":
            registradores[rd] = registradores[rs1] + imd
            return (f"{op} x{rd} = x{rs1} + {imd}")
        #andi
        elif func3 == "111":
            registradores[rd] = registradores[rs1] & imd
            return (f"{op} x{rd} = x{rs1} & {imd}")
        else:
            return  f"{op} Invalido, função não reconhecida \OPCODE valido para addi, andi, nop"
    
    elif opcode == "0000011":  # ld
        opcode, rd, func3, rs1, imd = operacao
        #imd inutilizado pois e tratado diretamento por registrador
        
        rd = int(rd, 2)
        rs1 = int(rs1, 2)

        #Sem atribuicao
        if rd == 0:
            return "LD em r0 = 0/ r0 Constante em 0"
        elif func3 == "011":
            if rs1 < 0:
                run = 0
                return (f"LD Invalido x{rd} nâo Existe")
            else:
                registradores[rd] = memoria[registradores[rs1]]
                return (f"LD x{rd} = Memoria{registradores[rs1]} = {memoria[registradores[rs1]]}")
        else:
            return  f"Operação Invalida, função não reconhecida \OPCODE valido para ld"

    elif opcode == "0100011":  # sd
        opcode, offset, func3, rs1, rs2, offset2  = operacao
        #ofsset inutilizado pois e tratado diretamento por registrador
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)
        
        if func3 == "000":
            if registradores[rs1] < 0:
                run = 0
                return (f"SD Invalido Memoria {registradores[rs1]} nâo Existe")
            
            memoria[registradores[rs2]] = registradores[rs1]
            return (f'SD Memoria {registradores[rs2]} =  x{rs1}')
        else:
            return  f"Operação Invalida, função não reconhecida \OPCODE valido para sd"
    
    elif opcode == "1100011":  # bne, beq
        opcode, im, offset, func3, rs1, rs2, offset2, imm  = operacao
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)
        offset = int(im + offset, 2)
        offset2 = int(imm + offset2, 2)
        pulo = (offset + offset2)
        func = ""
        
        if(pulo >= 0):
            pulo -= 1

        op = indentificaOpB(func3)

        #beq
        if func3 == "000":
            if(registradores[rs1] == registradores[rs2]):
                pc = pc + pulo 
            func = (f"x{rs1} == x{rs2}")
              
        #bne
        elif func3 == "001":
            if(registradores[rs1] != registradores[rs2]):
                pc = pc + pulo
            func = (f"x{rs1} != x{rs2}")

        else:
            return  f"{op} Invalido, função não reconhecida \OPCODE valido para bne, beq"

        return f'{op} {func} Se Condição Verdadeira Salto Para {pc +1}'  
       
    elif opcode == "1101111":  # jal
        opcode, rd, im8, im, im10, imm  = operacao
        rd = int(rd, 2)
        
        im8 = int(im + im8, 2)
        im10 = int(imm + im10, 2)
        
        pulo = (im8 + im10)
        if(pulo >= 0):
            pulo -= 1

        historico = ""
        #Sem atribuicao
        if rd == 0:
            historico = f"Registro de salto em r0 = 0/ r0 Constante em 0"
        else:
            historico = f"Registro de salto em r{rd} = {registradores[rd]}"

        pc = pulo
        return  (f"JAL PC = pulo = {pulo + 1} /{historico}")
        
    else:
        run = 0  # Finaliza o simulador se a instrução não for reconhecida.
        return "OPCODE INVALIDO SIMULAÇÃO ENCERRADA"     

#indentifica Operação de Registrador a ser executada retorna uma String
def indentificaOpR(func):
    if func == "0000000000":
        return "ADD"
    elif func == "0000100000":
        return "SUB"
    elif func == "1110000000":
        return "AND"
    elif func == "1100000000":
        return "OR"
    else:
        return "Operação"

#indentifica Operação Imediata a ser executada retorna uma String
def indentificaOpIMD(func):
    if func == "000":
        return "ADDi"
    elif func == "111":
        return "ANDI"
    else:
        return "Operação"

#indentifica Operação Condicional a ser executada retorna uma String   
def indentificaOpB(func):
    if func == "000":
        return "BEQ"
    elif func == "001":
        return "BNE"
    else:
        return "Operação"

#Retorna o binario convertido
def complemento2(binario):
    if binario[0] == '1':
        invertido = ''.join('1' if b == '0' else '0' for b in binario)
        decimal = int(invertido, 2) + 1
        decimal = -decimal
    else:
        decimal = int(binario, 2) 
    return decimal

#Recebe o arquivo e trata cada intrução em binario retornado uma lista de operações
def lista(binario):
    Operacoes = []
    
    for line in binario:
        line = cleaner(line)
        opcode = line[25:32]
        Operacoes.append(organizaInstrucao(line, opcode))
        
    return Operacoes

#Limpa a linha para receber o binario puro
def cleaner(line):
    line = line.split("b")
    return line[-1]

#Verifica o tipo de Instrução e retorna os valores separados
def organizaInstrucao(line, opcode):
    # Decodifica as instruções com base no opcode
    if opcode == "0110011":  # add, sub, or, and
        return [opcode, line[20:25], line[17:20], line[12:17], line[7:12], line[0:7]]
    elif opcode == "1100011":  # beq, bne
        return [opcode, line[24:25], line[20:24], line[17:20], line[12:17], line[7:12], line[1:7], line[0:1]]
    elif opcode == "1101111":  # jal
        return [opcode, line[20:25], line[12:20], line[11:12], line[1:11], line[0:1]]
    elif opcode == "0100011":  # sd
        return [opcode, line[20:25], line[17:20], line[12:17], line[7:12], line[0:7]]
    else:  # addi, andi, nop, ld
        return [opcode, line[20:25], line[17:20], line[12:17], line[0:12]]
        
def main():
    global run, pc, memoria, registradores
    
    binario = open(sys.argv[1], 'r')  # Arquivo com binário
    # Organiza instruções
    binario = lista(binario)
    
    # Executa simulador
    run = 1
    pc = 0
    memoria = [0] * 128
    registradores = [0] * 8
    simulador(binario)

if __name__ == "__main__":
    main()