class ErroDeConexao(Exception):
    """Excessão personalida para erros de conexão"""

    pass


class ErroAoCriarTabelaCliente(Exception):
    """Excessão personalida para erros na criação da tabela cliente"""

    pass


class ErroAoInserirCliente(Exception):
    """Excessão personalida para erros ao salvar na tabela clientes"""

    pass


class ErroAoAtualizarCliente(Exception):
    """Excessão personalida para erros ao atualizar registros na tabela clientes"""

    pass

class ErroAoExcluirCliente(Exception):
    """excessão personalida para erros ao excluir registos da tabela clientes"""