class HRISCVSimulator:
    def __init__(self):
        self.registers = [0] * 8  # Registradores r0 a r7
        self.pc = 0  # Program Counter
        self.memory = [0] * 128  # Memória com 128 endereços
        self.instructions = []

    def load_instructions(self, binary_file):
        with open(binary_file, 'r') as file:
            self.instructions = [line.strip() for line in file.readlines()]

    def fetch(self):
        if self.pc < len(self.instructions):
            return self.instructions[self.pc]
        return None

    def decode_and_execute(self, instruction):
        opcode = instruction[25:32]
        rd = int(instruction[20:25], 2)
        func3 = instruction[17:20]
        rs1 = int(instruction[12:17], 2)
        rs2 = int(instruction[7:12], 2)
        func7 = instruction[:7]

        imm_bin = instruction[:12]
        imm = int(imm_bin, 2) if imm_bin[0] == '0' else int(imm_bin, 2) - (1 << 12)

        print(f"📥 Imediato lido: {imm} (binário: {imm_bin})")

        # Verificação de registradores
        if not (0 <= rd < len(self.registers)) or not (0 <= rs1 < len(self.registers)) or (opcode == '0110011' and not (0 <= rs2 < len(self.registers))):
            print(f"⚠️ Erro: registrador inválido (rd={rd}, rs1={rs1}, rs2={rs2})")
            return False

        # Decodificação e execução das instruções
        if opcode == '0110011':  # R-Type (add, sub, mul)
            if func3 == '000':
                if func7 == '0000000':  # 'add'
                    self.registers[rd] = self.registers[rs1] + self.registers[rs2]
                    print(f"➕ Executando ADD: rd={rd}, rs1={rs1}, rs2={rs2}, resultado={self.registers[rd]}")
                elif func7 == '0100000':  # 'sub'
                    self.registers[rd] = self.registers[rs1] - self.registers[rs2]
                    print(f"➖ Executando SUB: rd={rd}, rs1={rs1}, rs2={rs2}, resultado={self.registers[rd]}")
                elif func7 == '0000001':  # 'mul'
                    self.registers[rd] = self.registers[rs1] * self.registers[rs2]
                    print(f"✖️ Executando MUL: rd={rd}, rs1={rs1}, rs2={rs2}, resultado={self.registers[rd]}")
        elif opcode == '0010011':  # I-Type ('addi')
            if func3 == '000':
                self.registers[rd] = self.registers[rs1] + imm
                print(f"🧮 Executando ADDI: rd={rd}, rs1={rs1}, imm={imm}, resultado={self.registers[rd]}")
        elif opcode == '1100011':  # B-Type ('beq')
            if func3 == '000':  # 'beq'
                if self.registers[rs1] == self.registers[rs2]:
                    print(f"🔀 BEQ: registradores iguais (rs1={rs1}, rs2={rs2}), desvio para PC={self.pc + imm}")
                    self.pc += imm  # Ajusta o PC para o rótulo
                    return True  # Salto ocorreu, não incrementar o PC automaticamente
        elif opcode == '1101111':  # J-Type ('jal')
            imm = int(instruction[:20], 2)  # Extraindo o imediato para JAL
            imm = imm if imm < (1 << 19) else imm - (1 << 20)  # Tratar o imediato como sinalizado
            print(f"🏃 Executando JAL: salto para PC={self.pc + imm}")
            self.pc += imm  # Ajusta o PC para o rótulo do loop
            return True  # Salto ocorreu, não incrementar o PC automaticamente

        # Garantir que r0 seja sempre 0
        self.registers[0] = 0
        return False


    def execute(self):
        print("💻 Iniciando a simulação RISC-V 💻\n")
        print("═════════════════════════════════════════════════════════════════\n")

        while self.pc < len(self.instructions):
            print(f"📝 Executando instrução na posição PC={self.pc}")
            instruction = self.fetch()
            if not instruction:
                break
            if not self.decode_and_execute(instruction):
                self.pc += 1  # Incrementar o PC apenas se não houver salto

        print("\n═════════════════════════════════════════════════════════════════")
        print("🌟 Estado final dos registradores 🌟")
        for i in range(8):
            print(f"r{i}: {self.registers[i]:>3}", end="  ")
            if (i + 1) % 4 == 0:
                print()
        print(f"\n\n📝 PC: {self.pc}")
        print(f"🧠 Memória (primeiros 10 valores): {self.memory[:10]}")
        print("\n═════════════════════════════════════════════════════════════════")
        print("👾 Simulação concluída 👾\n")


# Exemplo de uso
simulator = HRISCVSimulator()
simulator.load_instructions('input-g1.txt')
simulator.execute()
