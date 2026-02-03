# 📊 Projeto 2: Sistema de Auditoria com SQL

## 🎯 Objetivo
Sistema completo de auditoria utilizando banco de dados SQL com múltiplas tabelas relacionadas.

## 🛠️ Tecnologias
- Python 3.x
- SQLite3
- Pandas
- SQL (queries complexas com JOINs)

## 📋 Funcionalidades
- ✅ Banco de dados relacional com 4 tabelas
- ✅ Detecção de pagamentos duplicados via SQL
- ✅ Identificação de valores atípicos
- ✅ Análise por fornecedor e departamento
- ✅ Cruzamento de dados com JOINs
- ✅ Relatórios executivos automatizados

## 🗂️ Estrutura das Tabelas
- **fornecedores**: Cadastro de fornecedores
- **departamentos**: Departamentos da empresa
- **pagamentos**: Transações financeiras
- **auditoria_log**: Log de achados de auditoria

## 🚀 Como Executar
1. Instale as dependências: `pip install -r requirements.txt`
2. Execute os scripts na ordem:
```bash
   python scripts/1_criar_banco.py
   python scripts/2_popular_dados.py
   python scripts/3_consultas_auditoria.py
   python scripts/4_relatorio_executivo.py
```

## 📈 Resultados
O sistema gera automaticamente:
- Relatórios de duplicatas
- Análise de gastos por departamento vs orçamento
- Identificação de pagamentos de alto valor
- Análise temporal de pagamentos
- Relatório executivo consolidado em Excel

## 👨‍💻 Autor
Larissa Lima - Unidade 2: SQL e Bancos de Dados para Auditoria
