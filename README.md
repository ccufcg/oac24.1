# Implementação de um Simulador RISC-V em Python


**Objetivo**: Desenvolver um simulador RISC-V em Python capaz de converter um arquivo `.asm` com instruções em assembly para sua representação binária e, posteriormente, simular a execução dessas instruções em uma máquina com arquitetura simplificada (HRISC-V).


**Equipes** : Se dividam em grupos de até 4 participantes. 
- Preencher a planilha com os integrantes da equipe na [planilha](https://docs.google.com/spreadsheets/d/15_Yb_xL4qPqkxcHhxIdVfZ0OMNeevCCndfeNu1Rovok/edit?usp=sharing)

### **ToC**
1. Descrição da Atividade
   1. [Instruções](#instruções-suportadas)
   2. [Visão Geral](#descrição-do-simulador)
      1. [Conversor de instruções](#conversão-de-instruções-assembly-para-binário)
      2. [Simulador](#simulador-hrisc-v)
   3. [Entradas Exemplo](#entradas)
2. [Critérios de Avaliação](#entregáveis--avaliação)


## Instruções Suportadas

Por se tratar de um versão simplificada o RISC-V o nosso simulador tera que suportar as sequintes instruções:

**add, addi, and, andi, beq, bne, jal, ld, nop, or, sd, sub**


> Por se tratar de um conjunto simplificado de instruções. Considere as syntaxe simplificadas das instrções **ld** e **sd**.
> 
> | sala de aula | simulador |
> | ------------ | --------- |
> | addi x1, x0, 1024 <br> ld x2, 0(x1) <br> sd x11, 0(x1) | addi x1, x0, 1024 <br> ld x2, x1 <br> sd x11, x1  |
> 
> Repare que no nosso simulador em python **não utilizaremo** `0(x1)`. 
> - O nosso simulador fara referência direta ao registrado **`x1`**




<!-- R-type: add, and, or, rem, sub,
I-type: addi, andi, ld
S-type: sd
SB-type: beq, bge, blt, bne
UJ-type: jal
No-type: nop -->

##  Descrição do Simulador

O simulador será composto por duas partes:

> 1. [Conversor](#conversão-de-instruções-assembly-para-binário): converte a linguagem de montagem em máquina
> 2. [Simulador](#simulador-hrisc-v): executa as instruções em linguagem de máquina
> 3. [Exemplo de entrada](#entradas): Exemplo para teste

Ambos descritos abaixo. 

### Conversão de Instruções Assembly para Binário

**Descrição:**
Os alunos deverão implementar um programa em Python que receba como entrada um arquivo `.asm` contendo instruções em assembly do conjunto de instruções RISC-V. O programa deve:

> 1. **Ler o arquivo `.asm`:** As instruções estarão no formato assembly, e os comentários começarão com `#`.
> 2. **Converter as instruções:** Para cada linha de código assembly, o programa deve gerar a correspondente instrução em formato binário (32 bits) de acordo com o manual RISC-V,
>       - [Site Oficial do RISC](https://riscv.org/wp-content/uploads/2017/05/riscv-spec-v2.2.pdf])
>       - Livro _Digital Design and Computer Architecture - Harris&Harris_.
> 3. **Gerar um arquivo `.txt`:** O programa deve escrever as instruções convertidas em um arquivo `.txt`.

**Exemplo de Execução:**
```bash
python compilador.py input-g1.asm
```

**Saída Esperada:**
- Um arquivo `.txt` com as representações das instruções binárias
  - por exemplo, a primeira instrução foi convertida para o valor binário `0b00000001100100010000000110110011`
  - Em cada linha da saída deve ter uma string de **32 caracteres**, composta de `0` e `1`, representando o binário de cada instrução, na ordem de leitura.
    - `00000001100100010000000110110011`
- O arquivo de saida deve ter o mesmo nome da entrada por exemplo de execução acima a `.txt` de saíde deve ter o nome `input-g1.txt`.
  - Esse nome será gerado aleatorio durante a avaliação.  

**DICA:**

Cuidado com os rótulos. Eles serão utilizados para identificar a posição dos saltos.

Para facilitar o processamento, é recomendável realizar a leitura do arquivo `.asm` em dois momentos. Primeiro, identifique a posição dos rótulos (linhas) para que, no processamento das instruções, a posição correta possa ser repassada ao contador de programa (PC). O fluxo a seguir ilustra um possível procedimento de processamento.

<!-- Para converter o `.asm` no `.txt` um fluxo possivel é ler o arquivo `.asm` identificar a posição da -->

![](dica_c.png)

---


### Simulador HRISC-V

**Descrição:**
Na segunda etapa, os alunos deverão construir um simulador que executará as instruções geradas na etapa anterior (`.txt`) em uma arquitetura simplificada chamada HRISC-V.

**Especificações do HRISC-V:**

A arquitetura que será implementada deve considerar a arquitetura descrita na imagem a abaixo:

![](arq.png)

- **Memória de Instruções:** Armazena as instruções binárias geradas na primeira etapa. Capacidade de 128 endereços.
  - _inst_mem[128] = 0_
- **Memória de Dados:** Armazena variáveis que serão carregadas e lidas durante a execução. Capacidade de 16 endereços.
  - todos iniciam zerado
  - _data_mem[128] = 0_
- **Registradores:** O simulador terá 8 registradores (r0 a r7), mais o PC (Program Counter). 
  - O `PC` sempre busca a a instrução no endereço 0
  - O registrador `r0` sempre terá o valor 0.
  - ```python
    class hsrisc():
        def __init__():
            self.pc = 0
            self.r0 = 0
            self.r1 = 0
            ...
            self.r7 = 0
    ```
- **Decodificação e Execução:** O simulador deve ser capaz de decodificar cada instrução binária e realizar as operações correspondentes.
  - Ao final o simulador deve imprimir a saida com todos os valores dos registradores no formato abaixo:
    - pc=1,r0=0,r1=1,r2=1,r3=4,r5=1,r6=1,r7=7
    - Caso o simulador encontra um instrução invalida (`0b00000000000000000000000000000000`) ele deve encerrar a execução e exebir o status dos registradores.



**DICA:**

Para construir o simulador, vocês podem utilizar como base o [HPC1 e HPC2](https://github.com/ccufcg/oac/) e **considerar os seguintes passos**:



1. **Carregar as Instruções:** Ler o arquivo `.txt` gerado na Etapa 1 e carregar as instruções na memória de instruções.
2. **Simulação da Execução:** Implementar o ciclo de busca, decodificação e execução para simular o comportamento do HRISC-V.
3. **Exibir Estado Final:** Ao final da execução, o simulador deve exibir o estado de todos os registradores, incluindo o PC.

**Exemplo de Execução:**
```bash
python simulador.py output.txt
```

### Entradas

Ambas as partes (Simulador e Conversor) podem considerar o arquivo [exemplo 01](https://github.com/ccufcg/oac/blob/95a4d9d6d01466b5a8bc61dd67dbd8b65766f3a8/exemplo_1.asm)) para testar o sistema.


## Entregáveis & Avaliação


1. Descrição das instruções (29/08/2024):
    >  a. Considerando as instruções suportados na [seção 1](#instruções-suportadas) cada grupo deve entregar um os documentos indicando qual os typos das instruções:
    > ![](../imagens/na11/todasinst.svg)
    > - Exemplo No-type: nop
    >
    > b. Especificar e explicar o tipo de endereçamento das instruções
    > - imediato
    > - direto
    > - registrador
    > - indireto de registrador
    > - indexado
2. Código Python (10/09/2024)
   - compilador (`compilador.py`).
   - simulador (`simulador.py`).
   - obs: Não utilizar bibliotecas, apenas o core do python estara disponivel 
2. Apresentação explicando o funcionamento do código (17/09/2024)


<!-- 
R-type: add, and, or, rem, sub,
I-type: addi, andi, ld
S-type: sd
SB-type: beq, bge, blt, bne
UJ-type: jal
No-type: nop -->

### Avaliação

A avaliação se dará por meio da corretude do entregável 1   ($e_1$) e qualidade das explicações do entregável 3 ($e_3$). O código (entregável 2 - $e_2$) será avaliado com base na corretude, aderência às especificações do RISC-V, e a capacidade de simular a execução de instruções corretamente. 

Desse modo a nota do trabalho sera

$$ NT = \frac{e_1}{3} + \frac{e_2 + e_3}{2}$$

Sobre a correção do $e_2$, utilizerei um metodo similar ao utilizada em olimpiadas de programação, onde um juiz avaliara os artefatos utilizando códigos `.asm` - de complexidade similar ou inferio ao [exemplo 01](https://github.com/ccufcg/oac/blob/95a4d9d6d01466b5a8bc61dd67dbd8b65766f3a8/exemplo_1.asm) para ser avaliada. 


Importante: Avaliarei o `simulador.py` repassando saída (`.txt`) de um grupo para o outro. Por exemplo, a saída do conversor do G1 (`g1.txt`) sera executada pelo simulador do G3 e G4.


### Dúvidas

Caso tenham dúvidas, podem enviar um e-mail ou marcar um horário de atendimento. No entanto, não há garantia de resposta caso as dúvidas sejam enviadas com menos de 48 horas antes da data de entrega.

<!-- **Bônus:** Implementar suporte para mais tipos de instruções ou otimizações no simulador. -->
