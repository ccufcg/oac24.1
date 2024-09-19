def convert_asm_to_binary(asm_file):
    binary_instructions = []
    labels = {}

    instruction_set = {
        'add': '0110011',
        'sub': '0110011',
        'mul': '0110011',  
        'addi': '0010011',
        'and': '0110011',
        'andi': '0010011',
        'or': '0110011',
        'ld': '0000011',
        'sd': '0100011',
        'beq': '1100011',
        'bne': '1100011',
        'jal': '1101111',
        'nop': '0000001'
    }

    func3_set = {
        'add': '000',
        'sub': '000',
        'mul': '000',  
        'addi': '000',
        'and': '111',
        'andi': '111',
        'or': '110',
        'ld': '010',
        'sd': '010',
        'beq': '000',
        'bne': '001',
        'jal': '000'
    }

    func7_set = {
        'add': '0000000',
        'sub': '0100000',
        'mul': '0000001'  
    }

    registers = {
        'x0': '00000',
        'x1': '00001',
        'x2': '00010',
        'x3': '00011',
        'x4': '00100',
        'x5': '00101',
        'x6': '00110',
        'x7': '00111'
    }

    # Primeira passagem: encontrar rótulos
    with open(asm_file, 'r') as file:
        current_line = 0
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if ':' in line:
                label = line.split(':')[0].strip()
                labels[label] = current_line
            else:
                current_line += 1

    # Segunda passagem: converter instruções para binário
    with open(asm_file, 'r') as file:
        for line in file:
            line = line.strip()

            # Ignorar comentários e linhas vazias
            if not line or line.startswith('#'):
                continue

            # Remover comentários embutidos na linha
            if '#' in line:
                line = line.split('#')[0].strip()

            if ':' in line:
                continue  # Ignorar rótulos na segunda passagem

            parts = line.split()
            instruction = parts[0]

            if instruction not in instruction_set:
                raise ValueError(f"Instrução desconhecida: {instruction}")

            opcode = instruction_set[instruction]
            func3 = func3_set.get(instruction, '000')  

            # Instruções do tipo R (e.g., add, sub, mul)
            if instruction in ['add', 'sub', 'mul', 'or']:
                rd = registers.get(parts[1].replace(',', ''), '00000')
                rs1 = registers.get(parts[2].replace(',', ''), '00000')
                rs2 = registers.get(parts[3], '00000')
                func7 = func7_set.get(instruction, '0000000')
                binary_instruction = func7 + rs2 + rs1 + func3 + rd + opcode

            # Instruções do tipo I (e.g., addi, andi, ld)
            elif instruction in ['addi', 'andi', 'ld']:
                rd = registers.get(parts[1].replace(',', ''), '00000')
                rs1 = registers.get(parts[2].replace(',', ''), '00000')
                imm_value = int(parts[3])
                imm = format((1 << 12) + imm_value, '012b') if imm_value < 0 else format(imm_value, '012b')
                binary_instruction = imm + rs1 + func3 + rd + opcode

            elif instruction in ['sd']:  # Instrução de armazenamento (S-Type)
                rs2 = registers.get(parts[1].replace(',', ''), '00000')
                offset_and_rs1 = parts[2].replace(')', '').split('(')
                offset, rs1 = offset_and_rs1
                rs1 = registers.get(rs1, '00000')
                imm_value = int(offset)
                imm = format((1 << 12) + imm_value, '012b') if imm_value < 0 else format(imm_value, '012b')
                imm_high = imm[:7]  # Os 7 bits superiores do imediato
                imm_low = imm[7:]  # Os 5 bits inferiores do imediato
                binary_instruction = imm_high + rs2 + rs1 + func3 + imm_low + opcode

            # Garantir que a instrução tenha 32 bits
            binary_instruction = binary_instruction.ljust(32, '0')
            binary_instructions.append(binary_instruction)

    output_file = asm_file.replace('.asm', '.txt')
    with open(output_file, 'w') as file:
        for binary_instruction in binary_instructions:
            file.write(binary_instruction + '\n')

    print(f'Conversão completa. Saída em {output_file}')

# Exemplo de uso
convert_asm_to_binary('input-g1.asm')
