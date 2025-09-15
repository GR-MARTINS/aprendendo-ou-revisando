class ErroDeConexao(Exception):
    """exceção personalida para erros de conexão"""

    pass


class ErroAoCriarTabelaCliente(Exception):
    """exceção personalida para erros na criação da tabela cliente"""

    pass


class ErroAoInserirCliente(Exception):
    """exceção personalida para erros ao salvar na tabela clientes"""

    pass


class ErroAoAtualizarCliente(Exception):
    """exceção personalida para erros ao atualizar registros na tabela clientes"""

    pass


class ErroAoExcluirCliente(Exception):
    """exceção personalida para erros ao excluir registos da tabela clientes"""

    pass


class ErroAoInserirClientes(Exception):
    """exceção personalida para erros ao inserir registros em lote na tabela clientes."""

    pass


class ErroAoBuscarCliente(Exception):
    """exceção personalida para erros ao buscar um cliente no banco."""

    pass


class ErroAoBuscarClientes(Exception):
    """exceção personalida para erros ao buscar clientes no banco."""

    pass


class ErroAoListarClientesOrdenadosPorNome(Exception):
    """exceção personalida para erros ao listar clientes ordenados por nome no banco."""

    pass


class ErroAoListarPorEmail(Exception):
    """Exceção personalizada para erros ao buscar clientes por email."""

    pass
