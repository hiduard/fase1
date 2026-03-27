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