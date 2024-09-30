import sys
import os

rotulos = {}
contLine = 0

def main():

    entrada = sys.argv[1]
    nome_saida = os.path.splitext(entrada) [0] + '.txt'
    
    saida = open(nome_saida, 'w')
    risc = open(entrada, 'r')

    cont = 0 
    for line in risc:
        global rotulos
        retorno = retiraComentarios(line)
        
        if retorno != None:
            if(retorno.strip()[-1] == ":"):
                rotulos[retorno.strip()[:-1]] = cont
                cont -= 1
            cont += 1

    risc.seek(0)
     
    
    for line in risc:
        retorno = retiraComentarios(line)
        
        if retorno != None:
            compilador(retorno, saida)


    saida.close()
    risc.close()
           
def compilador(line, saida):
    line = line.strip()
    byte = operacao(line)
    
    if(byte != ""):
        saida.write(f"{byte}\n")

def retiraComentarios(line):
    line = line.strip()
    indice = line.find("#")
    
    if line == "":
        return
    elif indice == 0:
        return
    elif indice == -1:
        return line
    else:
        return line[:indice-1]
    

def operacao(line):
    instrucoes = line.split(" ", 1) 
    opcode = instrucoes[0].lower()
    
    if len(instrucoes) != 1:
        operandos = instrucoes[1].split(", ")
        

    if(opcode == "add"):
        byte = typeR(operandos, "0110011", "000", "0000000")
    elif(opcode == "addi"):
        byte = typeI(operandos, "0010011", "000")
    elif(opcode == "sub"):
        byte = typeR(operandos, "0110011", "000", "0100000")
    elif(opcode == "or"):
        byte = typeR(operandos, "0110011", "110", "0000000")
    elif(opcode == "and"):
        byte = typeR(operandos, "0110011", "111", "0000000")
    elif(opcode == "andi"):
        byte = typeI(operandos, "0010011", "111")
    elif(opcode == "beq"):
        byte = typeB(operandos, "1100011", "000")
    elif(opcode == "bne"):
        byte = byte = typeB(operandos, "1100011", "001")
    elif(opcode == "jal"):
        byte = typeJ(operandos, "1101111")
    elif(opcode == "ld"):
        byte = typeILd(operandos, "0000011" ,"011")
    elif(opcode == "sd"):
        byte = typeS(operandos, "0100011", "000")
    elif(opcode == "nop"):
        byte = typeI(["x0", "x0", "0"], "0010011", "000")
    else:
        byte = ""
        
    return byte

def typeR(operandos, code, fun3, fun7):
    rd, rs1, rs2 = filtra_registradores("r", operandos)
    return f"{fun7}{rs2}{rs1}{fun3}{rd}{code}"

def typeI(operandos, code, fun3):
    rd, rs1, imd = filtra_registradores("i", operandos)
    return f"{imd}{rs1}{fun3}{rd}{code}"

def typeILd(operandos, code, fun3):
    rd, rs1 = filtra_registradores("i", operandos)
    imd = "000000000000"
    return f"{imd}{rs1}{fun3}{rd}{code}"


def typeB(operandos, code, func3):
    rs1, rs2, imd = filtra_registradores("b", operandos)
    
    offset11 = imd[1]
    offset4_1 = imd[8:]
    offset10_5 = imd[2:8]
    offset12 = imd[0]
  
    return f"{offset12}{offset10_5}{rs2}{rs1}{func3}{offset4_1}{offset11}{code}"
    
def typeJ(operandos, code):
    rd, imd = filtra_registradores("j", operandos)
    
    offset19_12 = imd[1:9]
    offset11 = imd[9]
    offset10_1 = imd[10:]
    offset20 = imd[0]
    
    return f"{offset20}{offset10_1}{offset11}{offset19_12}{rd}{code}"

def typeS(operandos, code, func3):
    rs1, rs2 = filtra_registradores("s", operandos)
    #imd não utilizado
    imd = "000000000000"
    
    offset4_0 = imd[7:]
    offset11_5 = imd[:7]
    
    return f"{offset11_5}{rs2}{rs1}{func3}{offset4_0}{code}"

def filtra_registradores(tipo, operandos):
    resultado = []
    global rotulos 
    global contLine
    
    
    for elem in operandos:
        if(elem[0] == "x"):
            resultado.append(filtra_reg(elem))
        else:
            try:
                resultado.append(complemento_de_dois(elem, bits=12))
            except:
                if elem in rotulos:
                    
                    numero = rotulos[elem]

                    if tipo == "s":
                        resultado.append(f"{complemento_de_dois(numero, bits=7)}")
                    elif tipo == "b":
                        resultado.append(f"{complemento_de_dois(numero, bits=12)}")
                    else:
                        resultado.append(f"{complemento_de_dois(numero, bits=20)}")
    contLine += 1

    return resultado

def complemento_de_dois(numero, bits=32):

    numero = int(numero)

    if numero >= 0:
        return f"{numero:0{bits}b}"
    else:
        return f"{(1 << bits) + numero:0{bits}b}"
    
def filtra_reg(operando):
    return f"{int(operando[1:]):05b}"
    

if __name__ == "__main__":
    main()