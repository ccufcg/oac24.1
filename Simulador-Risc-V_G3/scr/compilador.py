# Importa bibliotecas necessárias
import sys
import os

# Dicionário para armazenar rótulos e suas respectivas linhas
rotulos = {}
# Contador de linhas
contLine = 0

# Função principal que controla o fluxo do programa
def main():
    # Obtém o arquivo de entrada a partir dos argumentos do sistema
    entrada = sys.argv[1]
    # Define o nome do arquivo de saída, alterando a extensão para .txt
    nome_saida = os.path.splitext(entrada)[0] + '.txt'
    
    # Abre o arquivo de saída para escrita
    saida = open(nome_saida, 'w')
    # Abre o arquivo de entrada para leitura
    risc = open(entrada, 'r')

    cont = 0 
    # Lê cada linha do arquivo de entrada
    for line in risc:
        global rotulos
        # Chama a função para remover comentários
        retorno = retiraComentarios(line)
        
        # Se a linha não for None (ou seja, não estiver vazia ou composta apenas por comentários)
        if retorno != None:
            # Verifica se a linha é um rótulo (termina com ":")
            if retorno.strip()[-1] == ":":
                # Adiciona o rótulo ao dicionário com a linha correspondente
                rotulos[retorno.strip()[:-1]] = cont
                cont -= 1
            cont += 1

    # Retorna ao início do arquivo
    risc.seek(0)
    
    # Processa novamente cada linha do arquivo de entrada
    for line in risc:
        retorno = retiraComentarios(line)
        
        # Se a linha não for None, chama a função compilador
        if retorno != None:
            compilador(retorno, saida)

    # Fecha os arquivos
    saida.close()
    risc.close()
           
# Função que compila a linha de código e escreve o resultado no arquivo de saída
def compilador(line, saida):
    line = line.strip()  # Remove espaços em branco
    byte = operacao(line)  # Obtém o byte correspondente à operação
    
    # Se o byte não estiver vazio, escreve no arquivo de saída
    if byte != "":
        saida.write(f"{byte}\n")

# Função que remove comentários de uma linha
def retiraComentarios(line):
    line = line.strip()  # Remove espaços em branco
    indice = line.find("#")  # Encontra o índice do caractere #

    # Verifica diferentes casos para remover comentários
    if line == "":
        return
    elif indice == 0:
        return
    elif indice == -1:
        return line
    else:
        return line[:indice-1]  # Retorna a linha sem o comentário

# Função que mapeia a operação a um byte
def operacao(line):
    instrucoes = line.split(" ", 1)  # Divide a linha em instrução e operandos
    opcode = instrucoes[0].lower()  # Obtém o opcode em letras minúsculas
    
    if len(instrucoes) != 1:
        operandos = instrucoes[1].split(", ")  # Divide os operandos

    # Mapeia cada opcode a uma função de geração de byte específica
    if opcode == "add":
        byte = typeR(operandos, "0110011", "000", "0000000")
    elif opcode == "addi":
        byte = typeI(operandos, "0010011", "000")
    elif opcode == "sub":
        byte = typeR(operandos, "0110011", "000", "0100000")
    elif opcode == "or":
        byte = typeR(operandos, "0110011", "110", "0000000")
    elif opcode == "and":
        byte = typeR(operandos, "0110011", "111", "0000000")
    elif opcode == "andi":
        byte = typeI(operandos, "0010011", "111")
    elif opcode == "beq":
        byte = typeB(operandos, "1100011", "000")
    elif opcode == "bne":
        byte = typeB(operandos, "1100011", "001")
    elif opcode == "jal":
        byte = typeJ(operandos, "1101111")
    elif opcode == "ld":
        byte = typeILd(operandos, "0000011", "011")
    elif opcode == "sd":
        byte = typeS(operandos, "0100011", "000")
    elif opcode == "nop":
        byte = typeI(["x0", "x0", "0"], "0010011", "000")  # Código para 'nop' (no operation)
    else:
        byte = ""  # Se o opcode não for reconhecido, retorna vazio
        
    return byte  # Retorna o byte gerado

# Função para gerar o byte do tipo R
def typeR(operandos, code, fun3, fun7):
    rd, rs1, rs2 = filtra_registradores("r", operandos)  # Filtra registradores
    return f"{fun7}{rs2}{rs1}{fun3}{rd}{code}"  # Formata o byte

# Função para gerar o byte do tipo I
def typeI(operandos, code, fun3):
    rd, rs1, imd = filtra_registradores("i", operandos)
    return f"{imd}{rs1}{fun3}{rd}{code}"

# Função para gerar o byte do tipo I para carga
def typeILd(operandos, code, fun3):
    rd, rs1 = filtra_registradores("i", operandos)
    imd = "000000000000"  # Valor imediato padrão para carga
    return f"{imd}{rs1}{fun3}{rd}{code}"

# Função para gerar o byte do tipo B
def typeB(operandos, code, func3):
    rs1, rs2, imd = filtra_registradores("b", operandos)
    
    # Obtém os offsets necessários
    offset11 = imd[1]
    offset4_1 = imd[8:]
    offset10_5 = imd[2:8]
    offset12 = imd[0]
  
    return f"{offset12}{offset10_5}{rs2}{rs1}{func3}{offset4_1}{offset11}{code}"

# Função para gerar o byte do tipo J
def typeJ(operandos, code):
    rd, imd = filtra_registradores("j", operandos)
    
    # Obtém os offsets necessários
    offset19_12 = imd[1:9]
    offset11 = imd[9]
    offset10_1 = imd[10:]
    offset20 = imd[0]
    
    return f"{offset20}{offset10_1}{offset11}{offset19_12}{rd}{code}"

# Função para gerar o byte do tipo S
def typeS(operandos, code, func3):
    rs1, rs2 = filtra_registradores("s", operandos)
    imd = "000000000000"  # Valor imediato não utilizado
    offset4_0 = imd[7:]
    offset11_5 = imd[:7]
    
    return f"{offset11_5}{rs2}{rs1}{func3}{offset4_0}{code}"

# Função para filtrar registradores e imediatos e convertê-los em formato binário
def filtra_registradores(tipo, operandos):
    resultado = []
    global rotulos 
    global contLine
    
    # Filtra cada operando
    for elem in operandos:
        if elem[0] == "x":  # Se for um registrador
            resultado.append(filtra_reg(elem))
        else:
            try:
                resultado.append(complemento_de_dois(elem, bits=12))  # Converte para complemento de dois
            except:
                if elem in rotulos:
                    numero = rotulos[elem]  # Obtém o número correspondente ao rótulo

                    # Dependendo do tipo, formata o número corretamente
                    if tipo == "s":
                        resultado.append(f"{complemento_de_dois(numero, bits=7)}")
                    elif tipo == "b":
                        resultado.append(f"{complemento_de_dois(numero, bits=12)}")
                    else:
                        resultado.append(f"{complemento_de_dois(numero, bits=20)}")
    contLine += 1  # Incrementa o contador de linhas

    return resultado  # Retorna a lista de registradores filtrados

# Função que converte um número para complemento de dois
def complemento_de_dois(numero, bits=32):
    numero = int(numero)  # Converte para inteiro

    if numero >= 0:
        return f"{numero:0{bits}b}"  # Formata o número em binário positivo
    else:
        return f"{(1 << bits) + numero:0{bits}b}"  # Formata o número em binário negativo

# Função que filtra o registrador e o converte para binário
def filtra_reg(operando):
    return f"{int(operando[1:]):05b}"  # Converte o registrador para 5 bits binários
    
# Executa a função principal se o script for executado diretamente
if __name__ == "__main__":
    main()
