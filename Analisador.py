from LAParser import LAParser
from Estruturas import Escopo, TabelaDeSimbolos


class Analisador:
    erros = []

    def adicionar_erro_semantico(token, mensagem):
        Analisador.erros.append(f"Linha {token.line}: {mensagem}")

    def verificar_tipo_parcela_unario(escopos, contexto):
        if contexto.NUM_INT() is not None:
            return TabelaDeSimbolos.TipoLA.INTEIRO
        if contexto.NUM_REAL() is not None:
            return TabelaDeSimbolos.TipoLA.REAL
        if contexto.identificador() is not None:
            return Analisador.verificar_tipo_identificador(
                escopos, contexto.identificador()
            )
        if contexto.IDENT() is not None:
            resultado = Analisador.verificar_tipo_nome_var(
                escopos, contexto.IDENT().getText()
            )
            for expressaoContext in contexto.expressao():
                auxiliar = Analisador.verificar_tipo_expressao(
                    escopos, expressaoContext
                )
                if resultado is None:
                    resultado = auxiliar
                elif (
                    resultado != auxiliar
                    and auxiliar != TabelaDeSimbolos.TipoLA.INVALIDO
                ):
                    resultado = TabelaDeSimbolos.TipoLA.INVALIDO
            return resultado
        else:
            resultado = None
            for expressaoContext in contexto.expressao():
                auxiliar = Analisador.verificar_tipo_expressao(
                    escopos, expressaoContext
                )
                if resultado is None:
                    resultado = auxiliar
                elif (
                    resultado != auxiliar
                    and auxiliar != TabelaDeSimbolos.TipoLA.INVALIDO
                ):
                    resultado = TabelaDeSimbolos.TipoLA.INVALIDO
            return resultado

    def verificar_tipo_termo_logico(escopos, contexto):
        resultado = None
        for token in contexto.fator_logico():
            auxiliar = Analisador.verificar_tipo_fator_logico(escopos, token)
            if resultado is None:
                resultado = auxiliar
            elif resultado != auxiliar and auxiliar != TabelaDeSimbolos.TipoLA.INVALIDO:
                resultado = TabelaDeSimbolos.TipoLA.INVALIDO
        return resultado

    def verificar_tipo_fator_logico(escopos, contexto):
        return Analisador.verificar_tipo_parcela_logica(
            escopos, contexto.parcela_logica()
        )

    def verificar_tipo_parcela_logica(escopos, contexto):
        if contexto.exp_relacional() is not None:
            resultado = Analisador.verificar_tipo_exp_relacional(
                escopos, contexto.exp_relacional()
            )
        else:
            resultado = TabelaDeSimbolos.TipoLA.LOGICO
        return resultado

    def verificar_tipo_exp_relacional(escopos, contexto):
        resultado = None
        if contexto.op_relacional() is not None:
            for token in contexto.exp_aritmetica():
                auxiliar = Analisador.verificar_tipo_exp_aritmetica(escopos, token)
                auxiliar_numeric0 = (
                    auxiliar == TabelaDeSimbolos.TipoLA.INTEIRO
                    or auxiliar == TabelaDeSimbolos.TipoLA.REAL
                )
                resultado_numerico = (
                    resultado == TabelaDeSimbolos.TipoLA.INTEIRO
                    or resultado == TabelaDeSimbolos.TipoLA.REAL
                )
                if resultado is None:
                    resultado = auxiliar
                elif (
                    not (auxiliar_numeric0 and resultado_numerico)
                    and auxiliar != resultado
                ):
                    resultado = TabelaDeSimbolos.TipoLA.INVALIDO
            if resultado != TabelaDeSimbolos.TipoLA.INVALIDO:
                resultado = TabelaDeSimbolos.TipoLA.LOGICO
        else:
            resultado = Analisador.verificar_tipo_exp_aritmetica(
                escopos, contexto.exp_aritmetica(0)
            )
        return resultado

    def verificar_tipo_identificador(escopos, contexto):
        nome_var = ""
        resultado = TabelaDeSimbolos.TipoLA.INVALIDO
        for i in range(len(contexto.IDENT())):
            nome_var += contexto.IDENT(i).getText()
            if i != len(contexto.IDENT()) - 1:
                nome_var += "."
        for tabela in escopos.obter_pilha():
            if tabela.contem(nome_var):
                resultado = Analisador.verificar_tipo_nome_var(escopos, nome_var)
        return resultado

    def verificar_tipo_termo(escopos, contexto):
        resultado = None
        for token in contexto.fator():
            auxiliar = Analisador.verificar_tipo_fator(escopos, token)
            auxiliar_numeric0 = (
                auxiliar == TabelaDeSimbolos.TipoLA.INTEIRO
                or auxiliar == TabelaDeSimbolos.TipoLA.REAL
            )
            resultado_numerico = (
                resultado == TabelaDeSimbolos.TipoLA.INTEIRO
                or resultado == TabelaDeSimbolos.TipoLA.REAL
            )
            if resultado is None:
                resultado = auxiliar
            elif (
                not (auxiliar_numeric0 and resultado_numerico) and auxiliar != resultado
            ):
                resultado = TabelaDeSimbolos.TipoLA.INVALIDO
        return resultado

    def verificar_tipo_fator(escopos, contexto):
        resultado = None
        for token in contexto.parcela():
            auxiliar = Analisador.verificar_tipo_parcela(escopos, token)
            if resultado is None:
                resultado = auxiliar
            elif resultado != auxiliar and auxiliar != TabelaDeSimbolos.TipoLA.INVALIDO:
                resultado = TabelaDeSimbolos.TipoLA.INVALIDO
        return resultado

    def verificar_tipo_parcela(escopos, contexto):
        resultado = TabelaDeSimbolos.TipoLA.INVALIDO
        if contexto.parcela_nao_unario() is not None:
            resultado = Analisador.verificar_tipo_parcela_nao_unario(
                escopos, contexto.parcela_nao_unario()
            )
        else:
            resultado = Analisador.verificar_tipo_parcela_unario(
                escopos, contexto.parcela_unario()
            )
        return resultado

    def verificar_tipo_parcela_nao_unario(escopos, contexto):
        if contexto.identificador() is not None:
            return Analisador.verificar_tipo_identificador(
                escopos, contexto.identificador()
            )
        return TabelaDeSimbolos.TipoLA.LITERAL

    def verificar_tipo_nome_var(escopos, nome_var):
        tipo = None
        for tabela in escopos.obter_pilha():
            tipo = tabela.verificar(nome_var)
        return tipo

    def verificar_tipo_expressao(escopos, contexto):
        resultado = None
        for token in contexto.termo_logico():
            auxiliar = Analisador.verificar_tipo_termo_logico(escopos, token)
            if resultado is None:
                resultado = auxiliar
            elif resultado != auxiliar and auxiliar != TabelaDeSimbolos.TipoLA.INVALIDO:
                resultado = TabelaDeSimbolos.TipoLA.INVALIDO
        return resultado

    def verificar_tipo_exp_aritmetica(escopos, contexto):
        resultado = None
        for token in contexto.termo():
            auxiliar = Analisador.verificar_tipo_termo(escopos, token)
            if resultado is None:
                resultado = auxiliar
            elif resultado != auxiliar and auxiliar != TabelaDeSimbolos.TipoLA.INVALIDO:
                resultado = TabelaDeSimbolos.TipoLA.INVALIDO
        return resultado
