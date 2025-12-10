#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para inspecionar os bytes problemáticos.
"""

from pathlib import Path

data_dir = Path(__file__).parent / 'data'
txt_file = data_dir / 'texto_fundamentos.txt'

with open(txt_file, 'rb') as f:
    content = f.read()

# Procura por "REGI" nos bytes
search_bytes = b'REGI'
pos = content.find(search_bytes)

if pos != -1:
    # Mostra 30 bytes ao redor da primeira ocorrência
    start = max(0, pos - 10)
    end = min(len(content), pos + 30)
    chunk = content[start:end]

    print("Bytes encontrados:")
    print(f"Posição: {pos}")
    print(f"Hex: {chunk.hex(' ')}")
    print(f"ASCII: {chunk}")
    print(f"\nString UTF-8 decoded:")
    try:
        print(chunk.decode('utf-8', errors='replace'))
    except:
        print("(erro ao decodificar)")

    # Procura especificamente por "REGIÃ"
    for i in range(len(content) - 10):
        if content[i:i+4] == b'REGI':
            # Mostra os próximos bytes
            sample = content[i:i+15]
            try:
                text = sample.decode('utf-8', errors='replace')
                if 'REGI' in text and 'O' in text:
                    print(f"\nEncontrado em {i}: {sample.hex(' ')}")
                    print(f"  Texto: {text}")
                    if i > 100:  # Limita a 100 ocorrências
                        break
            except:
                pass
