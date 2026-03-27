# ============================================================
# Analisador Léxico e Gerador de Código Assembly ARMv7
# Projeto de Compiladores - Fase 1
#
# Integrantes do grupo:
#   Eduardo Hideo Itinoseke Ogassawara
#   Gabriel Barbosa Fernandes de Oliveira
#
# Grupo 17
#
# ============================================================
import sys

TOKEN_NUMBER   = "NUMBER"
TOKEN_OPERATOR = "OPERATOR"
TOKEN_LPAREN   = "LPAREN"
TOKEN_RPAREN   = "RPAREN"
TOKEN_KEYWORD  = "KEYWORD"
TOKEN_ERROR    = "ERROR"


def estadoInicial(linha, pos, tokens):
#classifica e passa o caractere para o estado apro
    while pos < len(linha):
        c = linha[pos]

        if c == ' ' or c == '\t' or c == '\n' or c == '\r':
            pos = pos + 1

        elif c == '(':
            tokens.append((TOKEN_LPAREN, "("))
            pos = pos + 1

        elif c == ')':
            tokens.append((TOKEN_RPAREN, ")"))
            pos = pos + 1

        elif c == '+' or c == '-' or c == '*' or c == '^' or c == '%':
            pos = estadoOperador(linha, pos, tokens)

        elif c == '/':
            pos = estadoDivisao(linha, pos, tokens)

        elif c >= '0' and c <= '9':
            pos = estadoNumero(linha, pos, tokens)

        elif c >= 'A' and c <= 'Z':
            pos = estadoPalavraChave(linha, pos, tokens)

        elif c == ',':
            erro = c
            pos = pos + 1
            while pos < len(linha) and linha[pos] != ' ' and linha[pos] != ')' and linha[pos] != '(':
                erro = erro + linha[pos]
                pos = pos + 1
            tokens.append((TOKEN_ERROR, erro))

        else:
            tokens.append((TOKEN_ERROR, str(c)))
            pos = pos + 1

    return pos


def estadoNumero(linha, pos, tokens):
    
    # Reconhecimento de numeros reais.
    # Aceita: inteiros (42) e reais com ponto (3.14).
    # Rejeita: multiplos pontos (3.14.5), virgulas (3,45).
    
    numero = ""

    while pos < len(linha) and linha[pos] >= '0' and linha[pos] <= '9':
        numero = numero + linha[pos]
        pos = pos + 1

    if pos < len(linha) and linha[pos] == '.':
        numero = numero + '.'
        pos = pos + 1

        if pos < len(linha) and linha[pos] >= '0' and linha[pos] <= '9':
            while pos < len(linha) and linha[pos] >= '0' and linha[pos] <= '9':
                numero = numero + linha[pos]
                pos = pos + 1

            if pos < len(linha) and linha[pos] == '.':
                while pos < len(linha) and linha[pos] != ' ' and linha[pos] != ')' and linha[pos] != '(':
                    numero = numero + linha[pos]
                    pos = pos + 1
                tokens.append((TOKEN_ERROR, numero))
                return pos
        else:
            tokens.append((TOKEN_ERROR, numero))
            return pos

    if pos < len(linha) and linha[pos] == ',':
        while pos < len(linha) and linha[pos] != ' ' and linha[pos] != ')' and linha[pos] != '(':
            numero = numero + linha[pos]
            pos = pos + 1
        tokens.append((TOKEN_ERROR, numero))
        return pos

    tokens.append((TOKEN_NUMBER, numero))
    return pos


def estadoOperador(linha, pos, tokens):
    # Estado do AFD para operadores simples: + - * ^ %
    tokens.append((TOKEN_OPERATOR, linha[pos]))
    pos = pos + 1
    return pos


def estadoDivisao(linha, pos, tokens):
    pos = pos + 1
    if pos < len(linha) and linha[pos] == '/':
        tokens.append((TOKEN_OPERATOR, "//"))
        pos = pos + 1
    else:
        tokens.append((TOKEN_OPERATOR, "/"))
    return pos


def estadoPalavraChave(linha, pos, tokens):
    palavra = ""

    while pos < len(linha) and linha[pos] >= 'A' and linha[pos] <= 'Z':
        palavra = palavra + linha[pos]
        pos = pos + 1

    if pos < len(linha) and ((linha[pos] >= 'a' and linha[pos] <= 'z') or
                              (linha[pos] >= '0' and linha[pos] <= '9')):
        while pos < len(linha) and linha[pos] != ' ' and linha[pos] != ')' and linha[pos] != '(':
            palavra = palavra + linha[pos]
            pos = pos + 1
        tokens.append((TOKEN_ERROR, palavra))
        return pos

    tokens.append((TOKEN_KEYWORD, palavra))
    return pos

def estadoParenteses(linha, pos, tokens):
    if linha[pos] == '(':
        tokens.append((TOKEN_LPAREN, "("))
    elif linha[pos] == ')':
        tokens.append((TOKEN_RPAREN, ")"))
    pos = pos + 1
    return pos


def parseExpressao(linha, _tokens_):
    #Analisa uma linha de expressao RPN e extrai os tokens.
    estadoInicial(linha.strip(), 0, _tokens_)

    for token in _tokens_:
        if token[0] == TOKEN_ERROR:
            print("ERRO LEXICO: token invalido '" + token[1] + "' na linha: " + linha.strip())
            return False

    nivel = 0
    for token in _tokens_:
        if token[0] == TOKEN_LPAREN:
            nivel = nivel + 1
        elif token[0] == TOKEN_RPAREN:
            nivel = nivel - 1
        if nivel < 0:
            print("ERRO: parentese de fechamento sem abertura na linha: " + linha.strip())
            return False
    if nivel != 0:
        print("ERRO: parenteses desbalanceados na linha: " + linha.strip())
        return False

    return True


def _potencia_inteira(base, expoente):
    resultado = 1.0
    exp = int(expoente)
    i = 0
    while i < exp:
        resultado = resultado * base
        i = i + 1
    return resultado


def _truncar(valor):
    return float(int(valor))


def executarExpressao(tokens, resultados, memoria):

    #Parametros:
        #tokens     
        #resultados 
        #memoria    

    #Retorna:
        #float com o resultado, ou None em caso de erro.
    pilha_contextos = []
    contexto_atual = []

    i = 0
    while i < len(tokens):
        tipo, valor = tokens[i]

        if tipo == TOKEN_LPAREN:
            pilha_contextos.append(contexto_atual)
            contexto_atual = []
            i = i + 1

        elif tipo == TOKEN_RPAREN:
            resultado_sub = _avaliar_subexpressao(contexto_atual, resultados, memoria)
            if resultado_sub is None:
                return None

            if len(pilha_contextos) > 0:
                contexto_pai = pilha_contextos.pop()
                contexto_pai.append(("VAL", resultado_sub))
                contexto_atual = contexto_pai
            else:
                contexto_atual.append(("VAL", resultado_sub))
            i = i + 1

        elif tipo == TOKEN_NUMBER:
            contexto_atual.append(("NUM", valor))
            i = i + 1

        elif tipo == TOKEN_OPERATOR:
            contexto_atual.append(("OP", valor))
            i = i + 1

        elif tipo == TOKEN_KEYWORD:
            contexto_atual.append(("KW", valor))
            i = i + 1

        else:
            print("ERRO: token inesperado: " + str(tokens[i]))
            return None

    resultado_final = None
    for item in contexto_atual:
        if item[0] == "VAL":
            resultado_final = item[1]

    if resultado_final is not None:
        resultados.append(resultado_final)
    else:
        resultados.append(0.0)

    return resultado_final


def _avaliar_subexpressao(contexto, resultados, memoria):
    """Avalia o conteudo de uma subexpressao (dentro de parenteses)."""

    # (MEM) - leitura de memoria
    if len(contexto) == 1 and contexto[0][0] == "KW" and contexto[0][1] != "RES":
        nome_mem = contexto[0][1]
        if nome_mem in memoria:
            return memoria[nome_mem]
        else:
            return 0.0

    # (N RES) - resultado anterior
    if len(contexto) == 2 and contexto[1][0] == "KW" and contexto[1][1] == "RES":
        n = 0
        if contexto[0][0] == "NUM":
            n = int(float(contexto[0][1]))
        elif contexto[0][0] == "VAL":
            n = int(contexto[0][1])

        indice = len(resultados) - n
        if indice >= 0 and indice < len(resultados):
            return resultados[indice]
        else:
            print("ERRO: RES(" + str(n) + ") - indice fora do intervalo")
            return 0.0

    # (V MEM) - armazenar em memoria
    if len(contexto) == 2 and contexto[1][0] == "KW" and contexto[1][1] != "RES":
        nome_mem = contexto[1][1]
        valor = 0.0
        if contexto[0][0] == "NUM":
            valor = float(contexto[0][1])
        elif contexto[0][0] == "VAL":
            valor = contexto[0][1]
        memoria[nome_mem] = valor
        return valor

    # (A B op) - operacao aritmetica
    if len(contexto) >= 3 and contexto[-1][0] == "OP":
        operador = contexto[-1][1]

        # Operando A
        a = 0.0
        if contexto[0][0] == "NUM":
            a = float(contexto[0][1])
        elif contexto[0][0] == "VAL":
            a = contexto[0][1]
        elif contexto[0][0] == "KW":
            nome = contexto[0][1]
            a = memoria[nome] if nome in memoria else 0.0

        # Operando B
        b = 0.0
        if contexto[1][0] == "NUM":
            b = float(contexto[1][1])
        elif contexto[1][0] == "VAL":
            b = contexto[1][1]
        elif contexto[1][0] == "KW":
            nome = contexto[1][1]
            b = memoria[nome] if nome in memoria else 0.0

        # Executar operacao
        if operador == "+":
            return a + b
        elif operador == "-":
            return a - b
        elif operador == "*":
            return a * b
        elif operador == "/":
            if b == 0.0:
                print("ERRO: divisao por zero")
                return 0.0
            return a / b
        elif operador == "//":
            if b == 0.0:
                print("ERRO: divisao por zero")
                return 0.0
            return _truncar(a / b)
        elif operador == "%":
            if b == 0.0:
                print("ERRO: divisao por zero")
                return 0.0
            quociente = _truncar(a / b)
            return a - quociente * b
        elif operador == "^":
            return _potencia_inteira(a, b)
        else:
            print("ERRO: operador desconhecido '" + operador + "'")
            return None

    print("ERRO: subexpressao nao reconhecida: " + str(contexto))
    return None

# REPRESENTACAO INTERMEDIARIA PARA ASSEMBLY
OP_PUSH_CONST  = "PUSH_CONST"
OP_PUSH_RES    = "PUSH_RES"
OP_PUSH_MEM    = "PUSH_MEM"
OP_STORE_MEM   = "STORE_MEM"
OP_ADD         = "ADD"
OP_SUB         = "SUB"
OP_MUL         = "MUL"
OP_DIV         = "DIV"
OP_IDIV        = "IDIV"
OP_MOD         = "MOD"
OP_POW         = "POW"


def _gerar_operacoes_intermediarias(tokens, resultados_hist, memoria_nomes):
    """Gera lista de operacoes intermediarias para traducao em Assembly."""
    operacoes = []
    pilha_contextos = []
    contexto_atual = []

    i = 0
    while i < len(tokens):
        tipo, valor = tokens[i]

        if tipo == TOKEN_LPAREN:
            pilha_contextos.append(contexto_atual)
            contexto_atual = []
            i = i + 1
        elif tipo == TOKEN_RPAREN:
            ops = _processar_subexpr_asm(contexto_atual, resultados_hist, memoria_nomes)
            if ops is None:
                ops = []
            if len(pilha_contextos) > 0:
                contexto_pai = pilha_contextos.pop()
                contexto_pai.append(("SUBEXPR", ops))
                contexto_atual = contexto_pai
            else:
                contexto_atual.append(("SUBEXPR", ops))
            i = i + 1
        elif tipo == TOKEN_NUMBER:
            contexto_atual.append(("NUM", valor))
            i = i + 1
        elif tipo == TOKEN_OPERATOR:
            contexto_atual.append(("OP", valor))
            i = i + 1
        elif tipo == TOKEN_KEYWORD:
            contexto_atual.append(("KW", valor))
            i = i + 1
        else:
            i = i + 1

    for item in contexto_atual:
        if item[0] == "SUBEXPR":
            operacoes.extend(item[1])

    resultados_hist.append(len(resultados_hist))
    return operacoes


def _processar_subexpr_asm(contexto, resultados_hist, memoria_nomes):
    """Gera operacoes intermediarias para uma subexpressao."""
    operacoes = []

    if len(contexto) == 1 and contexto[0][0] == "KW" and contexto[0][1] != "RES":
        memoria_nomes[contexto[0][1]] = True
        operacoes.append((OP_PUSH_MEM, contexto[0][1]))
        return operacoes

    if len(contexto) == 2 and contexto[1][0] == "KW" and contexto[1][1] == "RES":
        if contexto[0][0] == "NUM":
            operacoes.append((OP_PUSH_RES, contexto[0][1]))
            return operacoes
        elif contexto[0][0] == "SUBEXPR":
            operacoes.extend(contexto[0][1])
            operacoes.append((OP_PUSH_RES, "stack"))
            return operacoes

    if len(contexto) == 2 and contexto[1][0] == "KW" and contexto[1][1] != "RES":
        nome_mem = contexto[1][1]
        memoria_nomes[nome_mem] = True
        if contexto[0][0] == "NUM":
            operacoes.append((OP_PUSH_CONST, contexto[0][1]))
        elif contexto[0][0] == "SUBEXPR":
            operacoes.extend(contexto[0][1])
        operacoes.append((OP_STORE_MEM, nome_mem))
        return operacoes

    if len(contexto) >= 3 and contexto[-1][0] == "OP":
        operador = contexto[-1][1]
        if contexto[0][0] == "NUM":
            operacoes.append((OP_PUSH_CONST, contexto[0][1]))
        elif contexto[0][0] == "SUBEXPR":
            operacoes.extend(contexto[0][1])
        elif contexto[0][0] == "KW":
            memoria_nomes[contexto[0][1]] = True
            operacoes.append((OP_PUSH_MEM, contexto[0][1]))

        if contexto[1][0] == "NUM":
            operacoes.append((OP_PUSH_CONST, contexto[1][1]))
        elif contexto[1][0] == "SUBEXPR":
            operacoes.extend(contexto[1][1])
        elif contexto[1][0] == "KW":
            memoria_nomes[contexto[1][1]] = True
            operacoes.append((OP_PUSH_MEM, contexto[1][1]))

        mapa = {"+": OP_ADD, "-": OP_SUB, "*": OP_MUL, "/": OP_DIV,
                "//": OP_IDIV, "%": OP_MOD, "^": OP_POW}
        if operador in mapa:
            operacoes.append((mapa[operador], None))
        return operacoes

    return operacoes


def gerarAssembly(tokens, codigoAssembly):
    #Gera codigo Assembly ARMv7 para todas as expressoes.
    todas_operacoes = []
    todas_constantes = []
    variaveis_mem = {}
    resultados_hist = []

    for idx in range(len(_tokens_)):
        ops = _gerar_operacoes_intermediarias(_tokens_[idx], resultados_hist, variaveis_mem)
        todas_operacoes.append(ops)
        for op, val in ops:
            if op == OP_PUSH_CONST and val is not None:
                if val not in todas_constantes:
                    todas_constantes.append(val)

    asm = []
    asm.append("@ ============================================================")
    asm.append("@ Codigo Assembly ARMv7 - Gerado automaticamente")
    asm.append("@ Compativel com CPUlator ARMv7 DEC1-SOC(v16.1)")
    asm.append("@ ============================================================")
    asm.append("")
    asm.append(".text")
    asm.append(".global _start")
    asm.append("")
    asm.append("_start:")
    asm.append("    LDR R4, =fp_stack       @ Base da pilha FP")
    asm.append("    MOV R5, #0              @ Offset da pilha FP")
    asm.append("    LDR R7, =resultados     @ Base do vetor de resultados")
    asm.append("    MOV R8, #0              @ Indice do resultado atual")
    asm.append("")

    for idx_expr in range(len(todas_operacoes)):
        ops = todas_operacoes[idx_expr]
        asm.append("    @ === Expressao " + str(idx_expr + 1) + " ===")
        asm.append("    MOV R5, #0")
        asm.append("")

        for op, val in ops:
            if op == OP_PUSH_CONST:
                idx_c = todas_constantes.index(val)
                asm.append("    @ Push " + str(val))
                asm.append("    LDR R0, =const_" + str(idx_c))
                asm.append("    VLDR D0, [R0]")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VSTR D0, [R1]")
                asm.append("    ADD R5, R5, #8")
                asm.append("")

            elif op == OP_PUSH_RES:
                asm.append("    @ Push RES " + str(val))
                asm.append("    LDR R0, =resultados")
                asm.append("    MOV R2, R8")
                asm.append("    MOV R3, #" + str(val))
                asm.append("    MOV R6, #8")
                asm.append("    MUL R3, R3, R6")
                asm.append("    SUB R2, R2, R3")
                asm.append("    ADD R0, R0, R2")
                asm.append("    VLDR D0, [R0]")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VSTR D0, [R1]")
                asm.append("    ADD R5, R5, #8")
                asm.append("")

            elif op == OP_PUSH_MEM:
                asm.append("    @ Push mem " + str(val))
                asm.append("    LDR R0, =mem_" + str(val))
                asm.append("    VLDR D0, [R0]")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VSTR D0, [R1]")
                asm.append("    ADD R5, R5, #8")
                asm.append("")

            elif op == OP_STORE_MEM:
                asm.append("    @ Store mem " + str(val))
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D0, [R1]")
                asm.append("    LDR R0, =mem_" + str(val))
                asm.append("    VSTR D0, [R0]")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VSTR D0, [R1]")
                asm.append("    ADD R5, R5, #8")
                asm.append("")

            elif op == OP_ADD:
                asm.append("    @ ADD")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D1, [R1]")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D0, [R1]")
                asm.append("    VADD.F64 D2, D0, D1")
                asm.append("    VSTR D2, [R1]")
                asm.append("    ADD R5, R5, #8")
                asm.append("")

            elif op == OP_SUB:
                asm.append("    @ SUB")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D1, [R1]")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D0, [R1]")
                asm.append("    VSUB.F64 D2, D0, D1")
                asm.append("    VSTR D2, [R1]")
                asm.append("    ADD R5, R5, #8")
                asm.append("")

            elif op == OP_MUL:
                asm.append("    @ MUL")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D1, [R1]")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D0, [R1]")
                asm.append("    VMUL.F64 D2, D0, D1")
                asm.append("    VSTR D2, [R1]")
                asm.append("    ADD R5, R5, #8")
                asm.append("")

            elif op == OP_DIV:
                asm.append("    @ DIV")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D1, [R1]")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D0, [R1]")
                asm.append("    VDIV.F64 D2, D0, D1")
                asm.append("    VSTR D2, [R1]")
                asm.append("    ADD R5, R5, #8")
                asm.append("")

            elif op == OP_IDIV:
                asm.append("    @ IDIV")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D1, [R1]")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D0, [R1]")
                asm.append("    VDIV.F64 D2, D0, D1")
                asm.append("    VCVT.S32.F64 S4, D2")
                asm.append("    VCVT.F64.S32 D2, S4")
                asm.append("    VSTR D2, [R1]")
                asm.append("    ADD R5, R5, #8")
                asm.append("")

            elif op == OP_MOD:
                asm.append("    @ MOD")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D1, [R1]           @ B")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D0, [R1]           @ A")
                asm.append("    VDIV.F64 D2, D0, D1")
                asm.append("    VCVT.S32.F64 S4, D2")
                asm.append("    VCVT.F64.S32 D2, S4")
                asm.append("    VMUL.F64 D3, D2, D1")
                asm.append("    VSUB.F64 D2, D0, D3")
                asm.append("    VSTR D2, [R1]")
                asm.append("    ADD R5, R5, #8")
                asm.append("")

            elif op == OP_POW:
                lbl = "pow_e" + str(idx_expr) + "_" + str(len(asm))
                asm.append("    @ POW")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D1, [R1]           @ expoente")
                asm.append("    SUB R5, R5, #8")
                asm.append("    ADD R1, R4, R5")
                asm.append("    VLDR D0, [R1]           @ base")
                asm.append("    VCVT.S32.F64 S4, D1")
                asm.append("    VMOV R2, S4")
                asm.append("    LDR R0, =const_um")
                asm.append("    VLDR D2, [R0]           @ resultado = 1.0")
                asm.append("    CMP R2, #0")
                asm.append("    BLE " + lbl + "_end")
                asm.append(lbl + "_loop:")
                asm.append("    VMUL.F64 D2, D2, D0")
                asm.append("    SUB R2, R2, #1")
                asm.append("    CMP R2, #0")
                asm.append("    BGT " + lbl + "_loop")
                asm.append(lbl + "_end:")
                asm.append("    VSTR D2, [R1]")
                asm.append("    ADD R5, R5, #8")
                asm.append("")

        # armazena resultado
        asm.append("    @ Resultado expr " + str(idx_expr + 1))
        asm.append("    SUB R5, R5, #8")
        asm.append("    ADD R1, R4, R5")
        asm.append("    VLDR D0, [R1]")
        asm.append("    ADD R1, R7, R8")
        asm.append("    VSTR D0, [R1]")
        asm.append("    ADD R8, R8, #8")
        asm.append("")
        asm.append("    VCVT.S32.F64 S0, D0")
        asm.append("    VMOV R0, S0")
        asm.append("    BL exibir_hex")
        asm.append("    BL imprimir_resultado")
        asm.append("")

    asm.append("_end:")
    asm.append("    B _end")
    asm.append("")

    # subrotinas
    asm.append("exibir_hex:")
    asm.append("    PUSH {R0-R3, LR}")
    asm.append("    LDR R1, =0xFF200020")
    asm.append("    LDR R2, =tabela_hex")
    asm.append("    CMP R0, #0")
    asm.append("    RSBLT R0, R0, #0")
    asm.append("    MOV R3, #0")
    asm.append("    BL mod10")
    asm.append("    LDRB R6, [R2, R6]")
    asm.append("    ORR R3, R3, R6")
    asm.append("    BL div10")
    asm.append("    BL mod10")
    asm.append("    LDRB R6, [R2, R6]")
    asm.append("    ORR R3, R3, R6, LSL #8")
    asm.append("    BL div10")
    asm.append("    BL mod10")
    asm.append("    LDRB R6, [R2, R6]")
    asm.append("    ORR R3, R3, R6, LSL #16")
    asm.append("    BL div10")
    asm.append("    BL mod10")
    asm.append("    LDRB R6, [R2, R6]")
    asm.append("    ORR R3, R3, R6, LSL #24")
    asm.append("    STR R3, [R1]")
    asm.append("    POP {R0-R3, PC}")
    asm.append("")
    asm.append("mod10:")
    asm.append("    PUSH {LR}")
    asm.append("    MOV R6, R0")
    asm.append("mod10_lp:")
    asm.append("    CMP R6, #10")
    asm.append("    SUBGE R6, R6, #10")
    asm.append("    BGE mod10_lp")
    asm.append("    POP {PC}")
    asm.append("")
    asm.append("div10:")
    asm.append("    PUSH {R1-R3, LR}")
    asm.append("    MOV R1, #0")
    asm.append("div10_lp:")
    asm.append("    CMP R0, #10")
    asm.append("    BLT div10_dn")
    asm.append("    SUB R0, R0, #10")
    asm.append("    ADD R1, R1, #1")
    asm.append("    B div10_lp")
    asm.append("div10_dn:")
    asm.append("    MOV R0, R1")
    asm.append("    POP {R1-R3, PC}")
    asm.append("")
    asm.append("imprimir_resultado:")
    asm.append("    PUSH {R0-R6, LR}")
    asm.append("    LDR R3, =0xFF201000")
    asm.append("    VMOV R0, R1, D0")
    asm.append("    CMP R1, #0")
    asm.append("    BGE pr_pos")
    asm.append("    MOV R2, #45")
    asm.append("    STR R2, [R3]")
    asm.append("    VNEG.F64 D0, D0")
    asm.append("pr_pos:")
    asm.append("    VCVT.S32.F64 S0, D0")
    asm.append("    VMOV R0, S0")
    asm.append("    BL print_int")
    asm.append("    MOV R2, #46")
    asm.append("    STR R2, [R3]")
    asm.append("    VCVT.S32.F64 S0, D0")
    asm.append("    VCVT.F64.S32 D1, S0")
    asm.append("    VSUB.F64 D2, D0, D1")
    asm.append("    LDR R0, =const_dez")
    asm.append("    VLDR D3, [R0]")
    asm.append("    VMUL.F64 D2, D2, D3")
    asm.append("    VCVT.S32.F64 S0, D2")
    asm.append("    VMOV R0, S0")
    asm.append("    CMP R0, #0")
    asm.append("    RSBLT R0, R0, #0")
    asm.append("    ADD R2, R0, #48")
    asm.append("    STR R2, [R3]")
    asm.append("    MOV R2, #10")
    asm.append("    STR R2, [R3]")
    asm.append("    POP {R0-R6, PC}")
    asm.append("")
    asm.append("print_int:")
    asm.append("    PUSH {R0-R6, LR}")
    asm.append("    MOV R4, #0")
    asm.append("    LDR R5, =print_buf")
    asm.append("    CMP R0, #0")
    asm.append("    BNE pi_loop")
    asm.append("    MOV R2, #48")
    asm.append("    STR R2, [R3]")
    asm.append("    B pi_end")
    asm.append("pi_loop:")
    asm.append("    CMP R0, #0")
    asm.append("    BEQ pi_rev")
    asm.append("    MOV R6, R0")
    asm.append("    MOV R1, #0")
    asm.append("pi_ml:")
    asm.append("    CMP R6, #10")
    asm.append("    BLT pi_md")
    asm.append("    SUB R6, R6, #10")
    asm.append("    ADD R1, R1, #1")
    asm.append("    B pi_ml")
    asm.append("pi_md:")
    asm.append("    STRB R6, [R5, R4]")
    asm.append("    ADD R4, R4, #1")
    asm.append("    MOV R0, R1")
    asm.append("    B pi_loop")
    asm.append("pi_rev:")
    asm.append("    SUB R4, R4, #1")
    asm.append("    LDRB R2, [R5, R4]")
    asm.append("    ADD R2, R2, #48")
    asm.append("    STR R2, [R3]")
    asm.append("    CMP R4, #0")
    asm.append("    BGT pi_rev")
    asm.append("pi_end:")
    asm.append("    POP {R0-R6, PC}")
    asm.append("")

    # dados
    asm.append(".data")
    asm.append(".align 3")
    asm.append("")
    for i in range(len(todas_constantes)):
        asm.append("const_" + str(i) + ": .double " + str(todas_constantes[i]))
    asm.append("")
    asm.append("const_um:  .double 1.0")
    asm.append("const_dez: .double 10.0")
    asm.append("")
    for nome in variaveis_mem:
        asm.append("mem_" + nome + ": .double 0.0")
    asm.append("")
    asm.append("resultados: .space " + str(len(todas_operacoes) * 8))
    asm.append("fp_stack: .space 800")
    asm.append("tabela_hex: .byte 0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F")
    asm.append("print_buf: .space 20")
    asm.append("")

    codigoAssembly[0] = "\n".join(asm)


def exibirResultados(resultados):
    
    print("============================================================")
    print(" RESULTADOS DAS EXPRESSOES")
    print("============================================================")
    print()

    for i in range(len(resultados)):
        valor = resultados[i]
        if valor is None:
            print("  Expressao " + str(i + 1) + ": ERRO")
        else:
            # Formatar o numero
            parte_int = int(valor)
            diferenca = valor - parte_int
            if diferenca < 0:
                diferenca = -diferenca

            if diferenca < 0.00001:
                texto = str(parte_int) + ".0"
            else:
                if valor < 0:
                    texto = "-"
                    valor_abs = -valor
                else:
                    texto = ""
                    valor_abs = valor

                p_int = int(valor_abs)
                p_frac = valor_abs - p_int
                texto = texto + str(p_int) + "."

                casas = 0
                while casas < 6:
                    p_frac = p_frac * 10
                    digito = int(p_frac)
                    texto = texto + str(digito)
                    p_frac = p_frac - digito
                    casas = casas + 1

                while len(texto) > 1 and texto[-1] == '0' and texto[-2] != '.':
                    texto = texto[:-1]

            print("  Expressao " + str(i + 1) + ": " + texto)

    print()
    print("============================================================")


def testeProgramaCompleto(nomeArquivo):
    
    #Testa o fluxo completo usando o arquivo de teste fornecido.
    #Para cada linha do arquivo, valida:
    #  1. Analise lexica (tokens gerados sem erros)
    #  2. Execucao da expressao (resultado calculado sem erros)
    #Exibe status detalhado de cada linha.

    print("=== Teste do Programa Completo: " + nomeArquivo + " ===")
    print()

    # le arquivo
    linhas = []
    if not lerArquivo(nomeArquivo, linhas):
        print("FALHOU - nao foi possivel ler o arquivo")
        return False

    todos_passaram = True
    total_linhas = len(linhas)
    linhas_ok = 0
    resultados = []
    memoria = {}

    for i in range(total_linhas):
        linha = linhas[i]
        print("Linha " + str(i + 1) + ": " + linha)

        # analise lexic
        tokens = []
        ok_parse = parseExpressao(linha, tokens)

        if not ok_parse:
            print("  Tokens: ERRO - entrada invalida")
            tem_erro = ""
            for t in tokens:
                if t[0] == TOKEN_ERROR:
                    tem_erro = t[1]
            if len(tem_erro) > 0:
                print("  Token invalido: " + tem_erro)
            print("  Status: FALHOU")
            print()
            todos_passaram = False
            resultados.append(None)
            continue

        # quantidade de tokens
        print("  Tokens: OK (" + str(len(tokens)) + " tokens)")

        #  execucao da expressao
        resultado = executarExpressao(tokens, resultados, memoria)

        if resultado is None:
            print("  Resultado: ERRO - nao foi possivel calcular")
            print("  Status: FALHOU")
            print()
            todos_passaram = False
            continue

        # Fformata
        parte_int = int(resultado)
        diferenca = resultado - parte_int
        if diferenca < 0:
            diferenca = -diferenca

        if diferenca < 0.00001:
            texto_res = str(parte_int) + ".0"
        else:
            if resultado < 0:
                texto_res = "-"
                valor_abs = -resultado
            else:
                texto_res = ""
                valor_abs = resultado
            p_int = int(valor_abs)
            p_frac = valor_abs - p_int
            texto_res = texto_res + str(p_int) + "."
            casas = 0
            while casas < 6:
                p_frac = p_frac * 10
                digito = int(p_frac)
                texto_res = texto_res + str(digito)
                p_frac = p_frac - digito
                casas = casas + 1
            while len(texto_res) > 1 and texto_res[-1] == '0' and texto_res[-2] != '.':
                texto_res = texto_res[:-1]

        print("  Resultado: " + texto_res)
        print("  Status: PASSOU")
        print()
        linhas_ok = linhas_ok + 1

    print("============================================================")
    print("Resumo: " + str(linhas_ok) + "/" + str(total_linhas) + " expressoes processadas com sucesso")
    if todos_passaram:
        print("Todos os testes PASSARAM!")
    else:
        print("Alguns testes FALHARAM.")
    print("============================================================")
    print()

    return todos_passaram


def lerArquivo(nomeArquivo, linhas):
    #Le arquivo de texto com expressoes RPN.
    try:
        arquivo = open(nomeArquivo, 'r', encoding='utf-8')
        for linha in arquivo:
            linha_limpa = linha.strip()
            if len(linha_limpa) > 0:
                linhas.append(linha_limpa)
        arquivo.close()
        return True
    except FileNotFoundError:
        print("ERRO: Arquivo '" + nomeArquivo + "' nao encontrado.")
        return False
    except PermissionError:
        print("ERRO: Sem permissao para ler '" + nomeArquivo + "'.")
        return False
    except Exception as e:
        print("ERRO ao ler arquivo: " + str(e))
        return False

def salvarTokens(tokens_por_linha, nomeArquivo):
    #tokens em .txt
    try:
        arquivo = open(nomeArquivo, 'w', encoding='utf-8')
        for i in range(len(tokens_por_linha)):
            arquivo.write("Expressao " + str(i + 1) + ":\n")
            for token in tokens_por_linha[i]:
                arquivo.write("  " + token[0] + ": " + token[1] + "\n")
            arquivo.write("\n")
        arquivo.close()
        return True
    except Exception as e:
        print("ERRO ao salvar tokens: " + str(e))
        return False

def main():
    pass

if _name_ == "_main_":
    main()