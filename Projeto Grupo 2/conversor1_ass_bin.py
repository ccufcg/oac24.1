import sys
import os

def registrador_para_binario(registrador):
    numero_registrador = int(registrador.replace('x', ''))
    return f'{numero_registrador:05b}'

def imediato_para_binario(imediato, tamanho):
    imediato = int(imediato)
    return f'{imediato & ((1 << tamanho) - 1):0{tamanho}b}'

def deslocamento_branch_para_binario(deslocamento):
    imediato = int(deslocamento)
    binario_imediato = f'{imediato & 0xFFF:012b}'
    return binario_imediato[0] + binario_imediato[2:8] + binario_imediato[8:12]
def deslocamento_jump_para_binario(deslocamento):
    imediato = int(deslocamento)
    binario_imediato = f'{imediato & 0xFFFFF:020b}'
    return binario_imediato[0] + binario_imediato[10:] + binario_imediato[9] + binario_imediato[1:9]

tabela_opcodes = {
    'add':  {'opcode': '0110011', 'funct3': '000', 'funct7': '0000000'}, 
    'addi': {'opcode': '0010011', 'funct3': '000'}, 
    'and':  {'opcode': '0110011', 'funct3': '111', 'funct7': '0000000'},  
    'andi': {'opcode': '0010011', 'funct3': '111'},  
    'beq':  {'opcode': '1100011', 'funct3': '000'},  
    'bne':  {'opcode': '1100011', 'funct3': '001'},  
    'jal':  {'opcode': '1101111'},  
    'ld':   {'opcode': '0000011', 'funct3': '011'},  
    'sd':   {'opcode': '0100011', 'funct3': '011'},  
    'nop':  {'opcode': '0010011', 'funct3': '000', 'rs1': '00000', 'rd': '00000', 'imm': '000000000000'},  # NOP
    'or':   {'opcode': '0110011', 'funct3': '110', 'funct7': '0000000'},  
    'sub':  {'opcode': '0110011', 'funct3': '000', 'funct7': '0100000'}, 
}

def assembly_para_binario(instrucao):
    partes = instrucao.split()
    mnemonico = partes[0]
    operandos = partes[1:]

    entrada = tabela_opcodes.get(mnemonico)

    if mnemonico == 'add':
        rd, rs1, rs2 = operandos
        binario = entrada['funct7'] + registrador_para_binario(rs2) + registrador_para_binario(rs1) + entrada['funct3'] + registrador_para_binario(rd) + entrada['opcode']
        return binario
    
    elif mnemonico == 'addi':
        rd, rs1, imediato = operandos
        binario = imediato_para_binario(imediato, 12) + registrador_para_binario(rs1) + entrada['funct3'] + registrador_para_binario(rd) + entrada['opcode']
        return binario

    elif mnemonico == 'and':
        rd, rs1, rs2 = operandos
        binario = entrada['funct7'] + registrador_para_binario(rs2) + registrador_para_binario(rs1) + entrada['funct3'] + registrador_para_binario(rd) + entrada['opcode']
        return binario

    elif mnemonico == 'andi':
        rd, rs1, imediato = operandos
        binario = imediato_para_binario(imediato, 12) + registrador_para_binario(rs1) + entrada['funct3'] + registrador_para_binario(rd) + entrada['opcode']
        return binario

    elif mnemonico == 'beq':
        rs1, rs2, deslocamento = operandos
        binario_deslocamento = deslocamento_branch_para_binario(deslocamento)
        binario = binario_deslocamento[0:7] + registrador_para_binario(rs2) + registrador_para_binario(rs1) + entrada['funct3'] + binario_deslocamento[7:] + entrada['opcode']
        return binario
    
    elif mnemonico == 'nop':
        binario = entrada['imm'] + entrada['rs1'] + entrada['funct3'] + entrada['rd'] + entrada['opcode']
        return binario

    elif mnemonico == 'or':
        rd, rs1, rs2 = operandos
        binario = entrada['funct7'] + registrador_para_binario(rs2) + registrador_para_binario(rs1) + entrada['funct3'] + registrador_para_binario(rd) + entrada['opcode']
        return binario

    elif mnemonico == 'sub':
        rd, rs1, rs2 = operandos
        binario = entrada['funct7'] + registrador_para_binario(rs2) + registrador_para_binario(rs1) + entrada['funct3'] + registrador_para_binario(rd) + entrada['opcode']
        return binario

    elif mnemonico == 'jal':
        rd, deslocamento = operandos
        binario_deslocamento = deslocamento_jump_para_binario(deslocamento)
        binario = binario_deslocamento + registrador_para_binario(rd) + entrada['opcode']
        return binario

    elif mnemonico == 'ld':
        rd, deslocamento, rs1 = operandos
        binario = imediato_para_binario(deslocamento, 12) + registrador_para_binario(rs1) + entrada['funct3'] + registrador_para_binario(rd) + entrada['opcode']
        return binario

    elif mnemonico == 'sd':
        rs2, deslocamento, rs1 = operandos
        binario = imediato_para_binario(deslocamento, 12) + registrador_para_binario(rs1) + entrada['funct3'] + registrador_para_binario(rs2) + entrada['opcode']
        return binario

    return None
    
def compilar_arquivo_asm(arquivo_entrada):
    with open(arquivo_entrada, 'r') as arquivo:
        linhas = arquivo.readlines()

    instrucoes_binarias = []
    
    for linha in linhas:
        linha = linha.strip()
        if linha:
            binario = assembly_para_binario(linha)
            if binario:
                instrucoes_binarias.append(binario)

    return instrucoes_binarias

def salvar_binario_em_arquivo(instrucoes_binarias, arquivo_saida):
    with open(arquivo_saida, 'w') as arquivo:
        for instrucao in instrucoes_binarias:
            arquivo.write(instrucao + '\n')

def main():
    if len(sys.argv) != 2:
        return
    
    arquivo_entrada = sys.argv[1]
    
    nome_base = os.path.splitext(arquivo_entrada)[0]
    arquivo_saida = nome_base + '.txt'
    
    instrucoes_binarias = compilar_arquivo_asm(arquivo_entrada)
    
    salvar_binario_em_arquivo(instrucoes_binarias, arquivo_saida)
    
    print(f"Instrucoes binarias salvas em {arquivo_saida}")

if __name__ == '__main__':
    main()
