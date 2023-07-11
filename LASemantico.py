from LAParser import LAParser
from LAVisitor import LAVisitor
from Estruturas import TabelaDeSimbolos, Escopo
from Analisador import Analisador


class LASemantico(LAVisitor):
    escopos = Escopo()

    def visitPrograma(self, contexto):
        return super().visitPrograma(contexto)

    def visitCmdAtribuicao(self, contexto):
        tipoExpressao = Analisador.verificar_tipo_expressao(
            LASemantico.escopos, contexto.expressao()
        )
        error = False
        nome_var = contexto.identificador().getText()
        if tipoExpressao != TabelaDeSimbolos.TipoLA.INVALIDO:
            for escopo in LASemantico.escopos.obter_pilha():
                if escopo.contem(nome_var):
                    tipoVar = Analisador.verificar_tipo_nome_var(
                        LASemantico.escopos, nome_var=nome_var
                    )
                    varNumeric = (
                        tipoVar == TabelaDeSimbolos.TipoLA.INTEIRO
                        or tipoVar == TabelaDeSimbolos.TipoLA.REAL
                    )
                    expNumeric = (
                        tipoExpressao == TabelaDeSimbolos.TipoLA.INTEIRO
                        or tipoExpressao == TabelaDeSimbolos.TipoLA.REAL
                    )
                    if (
                        not (varNumeric and expNumeric)
                        and tipoVar != tipoExpressao
                        and tipoExpressao != TabelaDeSimbolos.TipoLA.INVALIDO
                    ):
                        error = True
        else:
            error = True

        if error:
            Analisador.adicionar_erro_semantico(
                contexto.identificador().start,
                f"atribuicao nao compativel para {nome_var}",
            )

        return super().visitCmdAtribuicao(contexto)

    def visitIdentificador(self, contexto):
        for escopo in LASemantico.escopos.obter_pilha():
            if not escopo.contem(contexto.IDENT(0).getText()):
                Analisador.adicionar_erro_semantico(
                    contexto.start,
                    f"identificador {contexto.IDENT(0).getText()} nao declarado",
                )
                break
        return super().visitIdentificador(contexto)

    def visitDeclaracao_tipo(self, contexto):
        escopo_atual = LASemantico.escopos.obter_escopo_atual()

        if escopo_atual.contem(contexto.IDENT().getText()):
            Analisador.adicionar_erro_semantico(
                contexto.start,
                f"tipo {contexto.IDENT().getText()} ja declarado duas vezes no mesmo escopo",
            )
        else:
            escopo_atual.adicionar(
                contexto.IDENT().getText(), TabelaDeSimbolos.TipoLA.TIPO
            )

        return super().visitDeclaracao_tipo(contexto)

    def visitDeclaracao_variavel(self, contexto):
        escopo_atual = LASemantico.escopos.obter_escopo_atual()

        for identificador in contexto.variavel().identificador():
            if escopo_atual.contem(identificador.getText()):
                Analisador.adicionar_erro_semantico(
                    identificador.start,
                    f"identificador {identificador.getText()} ja declarado anteriormente",
                )
            else:
                tipo = TabelaDeSimbolos.TipoLA.INTEIRO
                if contexto.variavel().tipo().getText() == "literal":
                    tipo = TabelaDeSimbolos.TipoLA.LITERAL
                elif contexto.variavel().tipo().getText() == "real":
                    tipo = TabelaDeSimbolos.TipoLA.REAL
                elif contexto.variavel().tipo().getText() == "logico":
                    tipo = TabelaDeSimbolos.TipoLA.LOGICO

                escopo_atual.adicionar(identificador.getText(), tipo)

        return super().visitDeclaracao_variavel(contexto)

    def visitDeclaracao_global(self, contexto):
        escopo_atual = LASemantico.escopos.obter_escopo_atual()

        if escopo_atual.contem(contexto.IDENT().getText()):
            Analisador.adicionar_erro_semantico(
                contexto.start,
                f"{contexto.IDENT().getText()} ja declarado anteriormente",
            )
        else:
            escopo_atual.adicionar(
                contexto.IDENT().getText(), TabelaDeSimbolos.TipoLA.TIPO
            )

        return super().visitDeclaracao_global(contexto)

    def visitTipo_basico_ident(self, contexto):
        if contexto.IDENT() is not None:
            for escopo in LASemantico.escopos.obter_pilha():
                if not escopo.contem(contexto.IDENT().getText()):
                    Analisador.adicionar_erro_semantico(
                        contexto.start,
                        f"tipo {contexto.IDENT().getText()} nao declarado",
                    )
                    break

        return super().visitTipo_basico_ident(contexto)

    def visitDeclaracao_constante(self, contexto: LAParser.Declaracao_constanteContext):
        escopo_atual = LASemantico.escopos.obter_escopo_atual()

        if escopo_atual.contem(contexto.IDENT().getText()):
            Analisador.adicionar_erro_semantico(
                contexto.start,
                f"constante {contexto.IDENT().getText()} ja declarada anteriormente",
            )
        else:
            tipo = TabelaDeSimbolos.TipoLA.INTEIRO
            if contexto.tipo_basico().getText() == "literal":
                tipo = TabelaDeSimbolos.TipoLA.LITERAL
            elif contexto.tipo_basico().getText() == "real":
                tipo = TabelaDeSimbolos.TipoLA.REAL
            elif contexto.tipo_basico().getText() == "logico":
                tipo = TabelaDeSimbolos.TipoLA.LOGICO

            escopo_atual.adicionar(contexto.IDENT().getText(), tipo)

        return super().visitDeclaracao_constante(contexto)
