import sqlite3
import pandas as pd
from datetime import datetime
import os

print("="*70)
print("📋 RELATÓRIO EXECUTIVO DE AUDITORIA - BRF JUNDIAÍ")
print("="*70)

# ✅ CORREÇÃO: Criar pasta resultados se não existir
os.makedirs('../resultados', exist_ok=True)

conn = sqlite3.connect('../database/auditoria.db')

# Gerar todas as consultas e exportar para Excel

# Query principal - dados completos
query_completo = '''
    SELECT 
        p.codigo_pagamento,
        p.data,
        f.nome AS fornecedor,
        f.categoria AS categoria_fornecedor,
        d.nome AS departamento,
        d.gestor,
        p.valor,
        p.tipo_pagamento,
        p.status,
        p.aprovador
    FROM pagamentos p
    INNER JOIN fornecedores f ON p.fornecedor_id = f.id
    INNER JOIN departamentos d ON p.departamento_id = d.id
    ORDER BY p.data DESC
'''

df_completo = pd.read_sql_query(query_completo, conn)

# Duplicatas
query_dup = '''
    SELECT 
        p1.codigo_pagamento,
        p1.data,
        f.nome AS fornecedor,
        p1.valor,
        COUNT(*) AS ocorrencias
    FROM pagamentos p1
    INNER JOIN fornecedores f ON p1.fornecedor_id = f.id
    GROUP BY p1.data, p1.fornecedor_id, p1.valor
    HAVING COUNT(*) > 1
'''

df_duplicatas = pd.read_sql_query(query_dup, conn)

# Alto valor
query_alto = '''
    SELECT 
        p.codigo_pagamento,
        p.data,
        f.nome AS fornecedor,
        d.nome AS departamento,
        p.valor,
        p.aprovador
    FROM pagamentos p
    INNER JOIN fornecedores f ON p.fornecedor_id = f.id
    INNER JOIN departamentos d ON p.departamento_id = d.id
    WHERE p.valor > 150000
    ORDER BY p.valor DESC
'''

df_alto_valor = pd.read_sql_query(query_alto, conn)

# Por fornecedor
query_forn = '''
    SELECT 
        f.nome AS fornecedor,
        COUNT(p.id) AS qtd_pagamentos,
        SUM(p.valor) AS total_pago,
        AVG(p.valor) AS ticket_medio
    FROM pagamentos p
    INNER JOIN fornecedores f ON p.fornecedor_id = f.id
    GROUP BY f.id
    ORDER BY total_pago DESC
'''

df_fornecedores = pd.read_sql_query(query_forn, conn)

# Por departamento
query_dept = '''
    SELECT 
        d.nome AS departamento,
        d.orcamento_mensal,
        COUNT(p.id) AS qtd_pagamentos,
        SUM(p.valor) AS total_gasto,
        ROUND((SUM(p.valor) / d.orcamento_mensal * 100), 2) AS perc_orcamento
    FROM pagamentos p
    INNER JOIN departamentos d ON p.departamento_id = d.id
    GROUP BY d.id
    ORDER BY total_gasto DESC
'''

df_departamentos = pd.read_sql_query(query_dept, conn)

# Gerar resumo executivo
total_pagamentos = len(df_completo)
total_valor = df_completo['valor'].sum()
ticket_medio = df_completo['valor'].mean()
total_duplicatas = len(df_duplicatas)
total_alto_valor = len(df_alto_valor)

resumo = pd.DataFrame({
    'Indicador': [
        'Total de Pagamentos',
        'Valor Total (R$)',
        'Ticket Médio (R$)',
        'Pagamentos Duplicados',
        'Pagamentos Alto Valor',
        'Fornecedores Ativos',
        'Departamentos'
    ],
    'Valor': [
        total_pagamentos,
        f'{total_valor:,.2f}',
        f'{ticket_medio:,.2f}',
        total_duplicatas,
        total_alto_valor,
        df_fornecedores.shape[0],
        df_departamentos.shape[0]
    ]
})

# Exportar para Excel
arquivo_saida = f'../resultados/relatorio_auditoria_sql_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
    resumo.to_excel(writer, sheet_name='Resumo_Executivo', index=False)
    df_completo.to_excel(writer, sheet_name='Dados_Completos', index=False)
    df_duplicatas.to_excel(writer, sheet_name='Duplicatas', index=False)
    df_alto_valor.to_excel(writer, sheet_name='Alto_Valor', index=False)
    df_fornecedores.to_excel(writer, sheet_name='Por_Fornecedor', index=False)
    df_departamentos.to_excel(writer, sheet_name='Por_Departamento', index=False)

print("\n📊 RESUMO EXECUTIVO")
print("="*70)
print(resumo.to_string(index=False))

print(f"\n✅ Relatório gerado: {arquivo_saida}")

conn.close()

print("\n🎉 Processo de auditoria concluído!")
print("="*70)
