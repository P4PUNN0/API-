#!/usr/bin/env python3
"""
Script utilitario para generar el hash SHA-256 de una contraseña o texto.
Útil para preparar pruebas en Postman, cURL o pruebas automatizadas.
"""
import hashlib
import sys


def compute_sha256(text: str) -> str:
    """Calcula y devuelve el hash SHA-256 en formato hexadecimal."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "lola123"
    result = compute_sha256(target)
    
    print("-" * 65)
    print(f"Texto original: {target}")
    print(f"Hash SHA-256:   {result}")
    print("-" * 65)
