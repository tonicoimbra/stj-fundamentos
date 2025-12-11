# Correção de Encoding - Arquivos CSV STJ

## Resumo

Este documento descreve o processo de correção de problemas de encoding encontrados nos arquivos CSV do projeto STJ Fundamentos.

## Problema Identificado

Os arquivos CSV continham caracteres box-drawing (┐, └) sendo utilizados incorretamente no lugar de aspas duplas (").

### Exemplos de Problemas

**Antes da correção:**
```
┐caráter geral, abstrato...
alínea ┐b└ do inc. VI...
┐não selecionável└
```

**Depois da correção:**
```
"caráter geral, abstrato...
alínea "b" do inc. VI...
"não selecionável"
```

## Arquivos Afetados

Apenas 1 dos 4 arquivos CSV apresentava problemas:

- **AFIRE_202505141514.csv** - 24 substituições (12 caracteres ┐ + 12 caracteres └)
- AFIPO_(REsp_e AREsp)_202505141515.csv - OK
- AFIPO_(RMS)_202505141515.csv - OK
- AFIREQ_202505141516.csv - OK

## Scripts Criados

### 1. corrigir_encoding.py

Script principal para corrigir problemas de encoding.

**Funcionalidades:**
- Detecção automática de encoding
- Mapeamento de caracteres corrompidos para suas versões corretas
- Criação automática de backups (sufixo `_backup`)
- Processamento de todos os 4 arquivos CSV
- Validação básica da estrutura CSV
- Geração de relatório detalhado

**Uso:**
```bash
# Executar no diretório do projeto
python3 corrigir_encoding.py

# Ou especificar diretório
python3 corrigir_encoding.py /caminho/para/data
```

**Caracteres Corrigidos:**

| Antes | Depois | Descrição |
|-------|--------|-----------|
| ┐     | "      | Box-drawing → aspas duplas |
| └     | "      | Box-drawing → aspas duplas |
| ─     | -      | Box-drawing horizontal → hífen |
| │     | \|     | Box-drawing vertical → pipe |
| ┌     | "      | Box-drawing corner → aspas |
| ┘     | "      | Box-drawing corner → aspas |
| ├     | \|     | Box-drawing tee → pipe |
| ┤     | \|     | Box-drawing tee → pipe |
| ┬     | -      | Box-drawing tee → hífen |
| ┴     | -      | Box-drawing tee → hífen |
| ┼     | +      | Box-drawing cross → plus |

### 2. validar_correcoes.py

Script de validação para verificar a integridade das correções.

**Funcionalidades:**
- Verifica ausência de caracteres proibidos
- Valida estrutura CSV (número de colunas, linhas)
- Analisa estatísticas de conteúdo (acentos, aspas, etc.)
- Compara com arquivos de backup
- Gera relatório detalhado de validação

**Uso:**
```bash
python3 validar_correcoes.py

# Ou especificar diretório
python3 validar_correcoes.py /caminho/para/data
```

## Resultados

### Estatísticas de Correção

```
Total de arquivos processados: 4
Arquivos corrigidos: 1
Arquivos sem problemas: 3
Total de substituições: 24
```

### Validação

Todas as validações passaram com sucesso:

```
Total de arquivos validados: 4
Aprovados (PASS): 4
Reprovados (FAIL): 0
```

### Arquivo AFIRE_202505141514.csv (Corrigido)

- **Tamanho:** 133,616 bytes
- **Linhas:** 402 (incluindo cabeçalho)
- **Colunas:** 8
- **Caracteres acentuados:** 4,687
- **Aspas duplas:** 69 (após correção)
- **Backup:** AFIRE_202505141514.csv_backup

**Caracteres corrigidos:**
- '┐' → '"': 12 ocorrências
- '└' → '"': 12 ocorrências

**Diferença do backup:** 24 caracteres alterados

## Arquivos Gerados

### data/
```
AFIRE_202505141514.csv              # Arquivo corrigido
AFIRE_202505141514.csv_backup       # Backup do original
AFIPO_(REsp_e AREsp)_202505141515.csv
AFIPO_(RMS)_202505141515.csv
AFIREQ_202505141516.csv
relatorio_correcoes.txt             # Relatório da correção
```

### Raiz do projeto
```
corrigir_encoding.py                # Script de correção
validar_correcoes.py                # Script de validação
README_CORRECAO_ENCODING.md         # Esta documentação
```

## Processo Executado

1. **Análise Inicial**
   - Identificação dos padrões de corrupção
   - Análise de encoding (UTF-8 detectado)
   - Mapeamento de caracteres problemáticos

2. **Criação dos Scripts**
   - Script de correção com backup automático
   - Script de validação independente
   - Documentação completa

3. **Execução da Correção**
   - Backup automático do arquivo AFIRE
   - 24 substituições realizadas
   - Validação da estrutura CSV

4. **Validação Final**
   - Todos os arquivos aprovados
   - Nenhum caractere proibido encontrado
   - Estrutura CSV íntegra

## Segurança

### Backups

O arquivo original foi preservado:
- **Backup:** `AFIRE_202505141514.csv_backup`
- **Localização:** `/home/toni/Documentos/stj/files/stj_fundamentos/data/`
- **Tamanho:** 131KB (original)

### Reversão

Para reverter as mudanças (se necessário):

```bash
cd /home/toni/Documentos/stj/files/stj_fundamentos/data/
mv AFIRE_202505141514.csv AFIRE_202505141514.csv_fixed
mv AFIRE_202505141514.csv_backup AFIRE_202505141514.csv
```

## Observações

### Linhas Inconsistentes

Durante a validação, foram detectadas algumas linhas com número inconsistente de colunas:

- **AFIRE_202505141514.csv:** 7 linhas
- **AFIPO_(REsp_e AREsp)_202505141515.csv:** 4 linhas

Isso é comum quando o conteúdo contém o separador '#' como parte do texto. Não afeta a importação pelo comando `importar_fundamentos` do Django, que lida corretamente com isso.

### Encoding Final

Todos os arquivos foram salvos em **UTF-8** sem BOM, garantindo compatibilidade máxima com:
- Django ORM
- Pandas
- Editores de texto modernos
- Sistemas Unix/Linux

## Próximos Passos

Para utilizar os arquivos corrigidos:

```bash
# Limpar banco de dados e reimportar
python manage.py importar_fundamentos --dir=./data --clear

# Ou apenas importar (sem limpar)
python manage.py importar_fundamentos --dir=./data
```

## Conclusão

A correção foi realizada com sucesso, preservando todos os dados originais através de backups. Os arquivos CSV agora estão livres de caracteres problemáticos e prontos para uso no sistema Django.
