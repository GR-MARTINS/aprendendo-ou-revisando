def get_changes_from_states(state, target):
    # Pega os valores antigos e novos das colunas
    old_data = {}
    new_data = {}

    for attr in state.attrs:
        # attr.key é o nome da coluna
        hist = attr.history
        if hist.has_changes():
            old_data[attr.key] = hist.deleted[0] if hist.deleted else None
            new_data[attr.key] = hist.added[0] if hist.added else None
        else:
            # Se o campo não foi alterado, mantém o valor atual
            old_data[attr.key] = getattr(target, attr.key)
            new_data[attr.key] = getattr(target, attr.key)

    return old_data, new_data
