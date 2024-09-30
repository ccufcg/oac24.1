class Maquina:
    def __init__(self):
        self.registradores = [0] * 32
        self.memoria = [0] * 1024
        self.pc = 0
        self.instrucoes = []

    def carregar_instrucoes(self, arquivo_binario):
        try:
            with open(arquivo_binario, 'r') as arquivo:
                self.instrucoes = [linha.strip() for linha in arquivo.readlines()]
        except FileNotFoundError:
            print(f"Erro: O arquivo {arquivo_binario} não foi encontrado.")
            exit(1)

    def executar(self):
        while self.pc < len(self.instrucoes):
            if self.pc >= len(self.instrucoes):
                break
            instrucao = self.instrucoes[self.pc]
            self.decifrar_e_executar(instrucao)
            self.pc += 1
        
        self.exibir_estado()

    def decifrar_e_executar(self, instrucao):
        opcode = instrucao[-7:]
        if opcode == '0110011':
            self.executar_tipo_R(instrucao)
        elif opcode == '0010011':
            self.executar_tipo_I(instrucao)
        elif opcode == '1100011':
            self.executar_tipo_B(instrucao)
        elif opcode == '1101111':
            self.executar_tipo_J(instrucao)
        elif opcode == '0000011':
            self.executar_load(instrucao)
        elif opcode == '0100011':
            self.executar_store(instrucao)
        else:
            print(f"Operação desconhecida: {opcode}")

    def executar_tipo_R(self, instrucao):
        funct3 = instrucao[12:15]
        funct7 = instrucao[0:7]
        rd = int(instrucao[20:25], 2)
        rs1 = int(instrucao[15:20], 2)
        rs2 = int(instrucao[25:32], 2)
        
        if funct3 == '000':
            if funct7 == '0000000':
                self.registradores[rd] = self.registradores[rs1] + self.registradores[rs2]
            elif funct7 == '0100000':
                self.registradores[rd] = self.registradores[rs1] - self.registradores[rs2]
        elif funct3 == '111':
            if funct7 == '0000000':
                self.registradores[rd] = self.registradores[rs1] & self.registradores[rs2]
        elif funct3 == '110':
            if funct7 == '0000000':
                self.registradores[rd] = self.registradores[rs1] | self.registradores[rs2]

    def executar_tipo_I(self, instrucao):
        funct3 = instrucao[12:15]
        rd = int(instrucao[20:25], 2)
        rs1 = int(instrucao[15:20], 2)
        imediato = int(instrucao[0:12], 2)
        
        if funct3 == '000':
            self.registradores[rd] = self.registradores[rs1] + imediato
        elif funct3 == '111':
            self.registradores[rd] = self.registradores[rs1] & imediato

    def executar_tipo_B(self, instrucao):
        funct3 = instrucao[12:15]
        rs1 = int(instrucao[15:20], 2)
        rs2 = int(instrucao[20:25], 2)
        deslocamento = int(instrucao[0:12], 2)
        
        if funct3 == '000':
            if self.registradores[rs1] == self.registradores[rs2]:
                self.pc += deslocamento - 1
        elif funct3 == '001':
            if self.registradores[rs1] != self.registradores[rs2]:
                self.pc += deslocamento - 1

    def executar_tipo_J(self, instrucao):
        rd = int(instrucao[20:25], 2)
        deslocamento = int(instrucao[0:20], 2)
        self.pc += deslocamento - 1

    def executar_load(self, instrucao):
        rd = int(instrucao[20:25], 2)
        rs1 = int(instrucao[15:20], 2)
        deslocamento = int(instrucao[0:12], 2)
        endereco = self.registradores[rs1] + deslocamento
        if endereco < len(self.memoria):
            self.registradores[rd] = self.memoria[endereco]
        else:
            print(f"Erro: Endereço {endereco} fora dos limites da memória.")

    def executar_store(self, instrucao):
        rs2 = int(instrucao[25:32], 2)
        rs1 = int(instrucao[15:20], 2)
        deslocamento = int(instrucao[0:12], 2)
        endereco = self.registradores[rs1] + deslocamento
        if endereco < len(self.memoria):
            self.memoria[endereco] = self.registradores[rs2]
        else:
            print(f"Erro: Endereço {endereco} fora dos limites da memória.")

    def exibir_estado(self):
        print("Estado Final dos Registradores:")
        for i, valor in enumerate(self.registradores):
            print(f"R{i}: {valor:08x}")

        print(f"PC: {self.pc:08x}")

def main():
    arquivo_binario = 'saida.txt'
    maquina = Maquina()
    maquina.carregar_instrucoes(arquivo_binario)
    maquina.executar()

if __name__ == '__main__':
    main()
