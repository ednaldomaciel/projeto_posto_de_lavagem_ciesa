#!/usr/bin/env python
"""
Utilitário de linha de comando do Django para a raiz do projeto.
Permite executar comandos como:
    python manage.py runserver
    python manage.py test lavajato
    python manage.py migrate
diretamente da raiz sem a necessidade de dar 'cd backend'.
"""
import os
import sys
from pathlib import Path


def main():
    """Executa tarefas administrativas direcionando para o backend."""
    base_dir = Path(__file__).resolve().parent
    backend_dir = base_dir / 'backend'

    # Adiciona a pasta backend no início do sys.path para carregar config e lavajato
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django. Verifique se o ambiente virtual (venv) "
            "está ativado e se as dependências estão instaladas."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
