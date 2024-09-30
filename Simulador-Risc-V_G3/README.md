# Simulador Risc-V

Este projeto faz parte de uma disciplina de Organização e Arquitetura de Computadores (OAC), com o objetivo de construir um simulador baseado na arquitetura RISC-V, utilizando um subconjunto de instruções. O simulador é capaz de interpretar e executar instruções add, addi, and, andi, beq, bne, jal, ld, nop, or, sd, sub.
Pelos Alunos:

    Carlos Artur
    Débora Sabrina
    Nicolas Paz
    João Pedro

### Especificações de Implementação das Instruções

     Registradores: add, and, sub, or | Entradas rd, rs1, rs2
     Imediato: addi, andi             | Entradas rd, rs1, imd
     Salto Condicional: beq, bne      | Entradas rs1, rs2, rotulo/linha
     Salto:  jal                      | Entradas rd, rotulo/linha
     Memória Amazenar: sd             | Entradas rs1, rs2/memoria
     Memória Carregar: ld             | Entradas rd, rs1/memoria
     Pseudo Instrução: nop            |Internamente addi x0, x0, x0

Mais detalhes sobre o projeto podem ser encontrados na primeira parte da documentação, disponível em Parte 1 do Projeto.

### Compilador

O compilador deste projeto recebe um arquivo de entrada em formato .asm (com as instruções em Assembly RISC-V) e gera um arquivo de saída .txt, com o mesmo nome, contendo o código binário correspondente.
Como Usar

    Execução: Para rodar o compilador, execute o seguinte comando no terminal:

    bash

python montador.py <arquivo_de_entrada>

O arquivo de entrada <arquivo_de_entrada> deve conter as instruções em Assembly, e a saída será gerada automaticamente com o mesmo nome, mas com a extensão .txt.

Exemplo: Se você tiver um arquivo de entrada chamado programa.asm, o comando seria:

bash

    python montador.py programa.asm

    Isso gerará um arquivo de saída chamado programa.txt com o código binário correspondente.

Funcionalidades

    Instruções Suportadas:
        Aritméticas: add, addi, sub
        Lógicas: and, andi, or
        Controle de fluxo: beq, bne, jal
        Memória: ld, sd
        Outras: nop

    Rotulagem: O compilador identifica rótulos no código e os traduz para endereços de memória apropriados, permitindo saltos condicionais e incondicionais.

    Comentários: Linhas ou trechos de linhas iniciados com # são ignorados pelo compilador.

Estrutura do Código

    main(): Função principal que gerencia a leitura do arquivo de entrada, a remoção de comentários e a tradução das instruções.
    compilador(): Converte as instruções para seu formato binário adequado, chamando funções específicas para cada tipo de instrução.
    typeR(), typeI(), typeS(), typeB(), typeJ(): Geram o código binário para os diferentes formatos de instrução suportados pela arquitetura RISC-V.
    filtra_registradores(): Processa os operandos das instruções, convertendo-os em valores binários.

### Simulador

O simulador é responsável por interpretar e executar o código binário gerado pelo compilador, processando as instruções RISC-V.

Como Funciona?

O simulador lê um arquivo de entrada contendo as instruções em binário e executa cada uma delas, atualizando o valor dos registradores e a memória conforme necessário. O simulador também imprime o valor do program counter (PC), o opcode da instrução atual e o valor do registrador modificado, durante a execução de cada instrução.
Instruções Suportadas

    Aritméticas: add, addi, sub
    Lógicas: and, andi, or
    Controle de fluxo: beq, bne, jal
    Memória: ld, sd
    Outras: nop

    Instruções de Memória são tratadas diretamente pelo valor no registrador pois não foi implementado 0 ofsset utilizado em 0(r1) ou 2000(r0).

Como Usar

    Execução: Para rodar o simulador, execute o seguinte comando no terminal:

    bash

python simulador.py <arquivo_binario>

O arquivo <arquivo_binario> deve conter as instruções em código binário, e o simulador as processará e exibirá o resultado.

Exemplo: Se você tiver um arquivo de entrada chamado programa_binario.txt, o comando seria:

bash

    python simulador.py programa_binario.txt

    Isso executará as instruções do arquivo e mostrará o resultado no terminal.

Funcionalidades

    Registradores e Memória: O simulador possui 8 registradores e uma memória de 128 posições.

    Controle de Fluxo: O PC (Program Counter) é atualizado a cada instrução. Instruções de salto condicional e incondicional são executadas adequadamente.

    Mensagens de Erro: Se um opcode não for reconhecido, o simulador exibe uma mensagem de erro e encerra a simulação.

    Exemplo de Saída: Durante a execução, o simulador imprime o valor do PC, o opcode executado e o valor do registrador modificado:


    pc = 0, opCode = 0110011, Register r1 = 10
    pc = 1, opCode = 1101111, Register r5 = 5
    Opcode não reconhecido, finalizando simulação.

Estrutura do Código

    simulador(): Função principal que executa o ciclo de instruções, atualizando o PC e os registradores.
    executa(): Decodifica e executa cada instrução, modificando registradores e memória.
    lista(): Organiza o arquivo binário em uma lista de instruções.
    cleaner(): Remove caracteres indesejados da linha binária.
    organizaInstrucao(): Decodifica cada instrução binária em seus componentes, como opcode, registradores, e offsets.


Link do Repositorio 

    https://github.com/CarlosArturr/Simulador-Risc-V.git

Referências

    Guia Prático RISC-V 1.0.0
    Especificação RISC-V v2.2
    Arquitetura e Organização de Computadores (William Stallings)
    Digital Design and Computer Architecture (David Harris, Sarah Harris)

    Links:
      http://riscvbook.com/portuguese/guia-pratico-risc-v-1.0.0.pdf
      https://riscv.org/wp-content/uploads/2017/05/riscv-spec-v2.2.pdf
      https://archive.org/details/stallings-arquitetura-e-organizacao-de-computadores-10a/page/n31/mode/2up?view=theater 

