# Projeto: Simulador RISC-V e Compilador

- Fábio
- Laysa
- Emanuel
- João Pedro

Este projeto consiste em um simulador de um conjunto simplificado de instruções da arquitetura RISC-V, e um compilador que converte código assembly para binário.

## Arquivos

### 1. `compilador.py`

Este script é responsável por converter um código em linguagem assembly (arquivo `.asm`) em uma representação binária. Essa conversão é necessária para que o simulador possa executar as instruções.

#### Funcionamento

1. **Primeira Passagem (Coletar Rótulos):**

   - O compilador percorre o arquivo `.asm` para identificar os rótulos (nomes que marcam posições no código, usados em instruções de salto como `beq` e `jal`).
   - Armazena as posições dos rótulos em um dicionário para serem utilizados na segunda passagem.

2. **Segunda Passagem (Conversão para Binário):**

   - O compilador processa cada linha de instrução no código assembly.
   - Converte as instruções para seus opcodes binários usando um dicionário de opcodes.
   - Extrai registradores e valores imediatos das instruções, convertendo-os para binário.
   - Para instruções de salto (`beq`, `bne`, `jal`), calcula os deslocamentos para os rótulos e os converte em binário.

3. **Geração do Arquivo Binário:**
   - O resultado é uma lista de instruções em binário, que são salvas em um arquivo `.txt`.
   - Esse arquivo é utilizado pelo `simulador.py` para executar as instruções.

### 2. `simulador.py`

Este script simula a execução das instruções binárias geradas pelo compilador. Ele emula uma arquitetura simplificada do RISC-V, executando as operações descritas nas instruções.

#### Funcionamento

1. **Carregar Instruções:**

   - O simulador lê o arquivo binário gerado pelo `compilador.py` e armazena as instruções em uma lista para execução.

2. **Simular a Execução:**

   - O simulador executa um ciclo de "buscar-decodificar-executar":
     - **Busca:** Obtém a próxima instrução usando o `Program Counter` (PC).
     - **Decodifica:** Extrai o opcode, registradores, e valores imediatos da instrução binária.
     - **Executa:** Realiza operações como `add`, `sub`, `ld`, `sd`, e controle de fluxo (`beq`, `bne`, `jal`).
     - Inclui validações para endereços de memória válidos e acessos a registradores.

3. **Atualiza Estado:**

   - O simulador atualiza os registradores e a memória conforme as instruções são executadas. Garante que o registrador `r0` sempre tenha o valor 0 (convenção da arquitetura RISC-V).

4. **Exibe Resultados:**
   - Ao final da execução, o simulador exibe o estado final dos registradores e parte da memória, permitindo verificar o resultado da simulação.

## Uso

1. **Compilar o Arquivo `.asm`:**

   ```bash
   python3 compilador.py input-g1.asm
   - Isso gerará um arquivo binário .txt que pode ser usado pelo simulador.

   ```

2. **Executar o Simulador:**
   ```bash
   python3 simulador.py
   ```

## Análise do Arquivo `input-g1.asm` e Resultados da Simulação

Vamos explicar os resultados apresentados pelo simulador com base no código assembly fornecido no arquivo `input-g1.asm`:

### Código Assembly (`input-g1.asm`)

#### Carregar valores em registradores:

##### Exemplo de código assembly para calcular potenciação: x^y

- `addi x1, x0, 3` – Carrega o valor 3 no registrador `x1`.
- `addi x2, x0, 4` – Carregar expoente y = 4 em `x2`.
- `addi x3, x0, 1` - Inicializar resultado (x^0 = 1) em `x3`.
- `add x4, x0, x2` - Inicializar contador em `x4`.

##### Loop para calcular x^y:

- `loop:`
- `mul x3, x3, x1` - Multiplica resultado por x (x3 = x3 \* x1)
- `jal x0, loop` - Realiza um salto incondicional para o início do loop, repetindo as multiplicações até atingir o expoente.
- `beq x2, x4, end` - Verifica se o contador atingiu o valor do expoente `(x4) == expoente (x2)`. Se sim, o loop é finalizado.

##### Rótulo de término do loop:

- `end:`
- `nop` # O loop termina quando o contador (`x4`) atinge o valor do expoente (`x2`), e o valor final da potenciação é armazenado no registrador `x3`.

**Resultado no simulador:**

- `x1 = 5`
- `x2 = 10`

#### Operações aritméticas:

- `add x3, x1, x2` – Soma os valores de `x1` e `x2` (5 + 10) e armazena o resultado em `x3`.
- `sub x4, x2, x1` – Subtrai o valor de `x1` do valor de `x2` (10 - 5) e armazena o resultado em `x4`.

##### Resultado esperado:

- O código calcula `3^4`. O valor final será armazenado em `x3`, e o resultado esperado é `81, pois 3^4 = 81.`

### Saída esperada do Simulador

O estado final dos registradores é:
`r0: 0, r1: 3, r2: 4, r3: 81`
`r4: 4, r5: 0, r6: 0, r7: 0`

### Conclusão

O simulador executa corretamente as operações definidas no arquivo assembly. Os resultados nos registradores refletem as operações aritméticas e de memória especificadas. No caso específico do código fornecido:

- Este código assembly realiza o cálculo de potenciação utilizando um loop simples. O simulador executará as instruções e exibirá o resultado final, que, para este exemplo, será `81 (o valor de 3^4)`.

O simulador garante que as instruções sejam interpretadas e executadas corretamente conforme as definições do arquivo assembly, demonstrando uma implementação funcional do conjunto de instruções RISC-V.
