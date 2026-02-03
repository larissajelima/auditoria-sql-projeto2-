import sqlite3
import pandas as pd

print("="*70)
print("🔍 SISTEMA DE CONSULTAS DE AUDITORIA")
print("="*70)

conn = sqlite3.connect('../database/auditoria.db')

# ============================================================
# CONSULTA 1: Pagamentos por Fornecedor (com JOIN)
# ============================================================
print("\n" + "="*70)
print("📊 CONSULTA 1: Total de Pagamentos por Fornecedor")
print("="*70)

query1 = '''
    SELECT 
        f.nome AS fornecedor,
        f.categoria,
        COUNT(p.id) AS qtd_pagamentos,
        SUM(p.valor) AS total_pago,
        AVG(p.valor) AS ticket_medio,
        MAX(p.valor) AS maior_pagamento
    FROM pagamentos p
    INNER JOIN fornecedores f ON p.fornecedor_id = f.id
    GROUP BY f.id, f.nome, f.categoria
    ORDER BY total_pago DESC
'''

df1 = pd.read_sql_query(query1, conn)
print(df1.to_string(index=False))

# ============================================================
# CONSULTA 2: Pagamentos por Departamento
# ============================================================
print("\n" + "="*70)
print("🏢 CONSULTA 2: Gastos por Departamento vs Orçamento")
print("="*70)

query2 = '''
    SELECT 
        d.nome AS departamento,
        d.gestor,
        d.orcamento_mensal,
        COUNT(p.id) AS qtd_pagamentos,
        SUM(p.valor) AS total_gasto,
        ROUND((SUM(p.valor) / d.orcamento_mensal * 100), 2) AS perc_orcamento
    FROM pagamentos p
    INNER JOIN departamentos d ON p.departamento_id = d.id
    GROUP BY d.id, d.nome, d.gestor, d.orcamento_mensal
    ORDER BY perc_orcamento DESC
'''

df2 = pd.read_sql_query(query2, conn)
print(df2.to_string(index=False))

# ============================================================
# CONSULTA 3: Identificar Pagamentos Duplicados
# ============================================================
print("\n" + "="*70)
print("⚠️  CONSULTA 3: Detecção de Pagamentos Duplicados")
print("="*70)

query3 = '''
    SELECT 
        p1.codigo_pagamento,
        p1.data,
        f.nome AS fornecedor,
        d.nome AS departamento,
        p1.valor,
        COUNT(*) AS ocorrencias
    FROM pagamentos p1
    INNER JOIN fornecedores f ON p1.fornecedor_id = f.id
    INNER JOIN departamentos d ON p1.departamento_id = d.id
    GROUP BY p1.data, p1.fornecedor_id, p1.departamento_id, p1.valor
    HAVING COUNT(*) > 1
    ORDER BY ocorrencias DESC, valor DESC
'''

df3 = pd.read_sql_query(query3, conn)
print(f"\n🚨 Total de pagamentos duplicados encontrados: {len(df3)}")
if len(df3) > 0:
    print("\nPrimeiras duplicatas:")
    print(df3.head(10).to_string(index=False))

# ============================================================
# CONSULTA 4: Pagamentos Acima do Limite
# ============================================================
print("\n" + "="*70)
print("💰 CONSULTA 4: Pagamentos de Alto Valor (>R$ 150.000)")
print("="*70)

query4 = '''
    SELECT 
        p.codigo_pagamento,
        p.data,
        f.nome AS fornecedor,
        d.nome AS departamento,
        p.valor,
        p.aprovador,
        p.status
    FROM pagamentos p
    INNER JOIN fornecedores f ON p.fornecedor_id = f.id
    INNER JOIN departamentos d ON p.departamento_id = d.id
    WHERE p.valor > 150000
    ORDER BY p.valor DESC
'''

df4 = pd.read_sql_query(query4, conn)
print(f"\n💵 Total: {len(df4)} pagamentos acima de R$ 150.000")
print(df4.to_string(index=False))

# ============================================================
# CONSULTA 5: Fornecedores Inativos com Pagamentos
# ============================================================
print("\n" + "="*70)
print("🚫 CONSULTA 5: Pagamentos para Fornecedores Inativos")
print("="*70)

query5 = '''
    SELECT 
        f.nome AS fornecedor,
        f.cnpj,
        COUNT(p.id) AS qtd_pagamentos,
        SUM(p.valor) AS total_pago
    FROM pagamentos p
    INNER JOIN fornecedores f ON p.fornecedor_id = f.id
    WHERE f.ativo = 0
    GROUP BY f.id, f.nome, f.cnpj
'''

df5 = pd.read_sql_query(query5, conn)
if len(df5) > 0:
    print("⚠️  ATENÇÃO: Encontrados pagamentos para fornecedores inativos!")
    print(df5.to_string(index=False))
else:
    print("✅ Nenhum pagamento para fornecedor inativo")

# ============================================================
# CONSULTA 6: Análise Temporal (Pagamentos por Mês)
# ============================================================
print("\n" + "="*70)
print("📅 CONSULTA 6: Distribuição de Pagamentos por Mês")
print("="*70)

query6 = '''
    SELECT 
        strftime('%Y-%m', data) AS mes,
        COUNT(*) AS qtd_pagamentos,
        SUM(valor) AS total_mensal,
        AVG(valor) AS ticket_medio
    FROM pagamentos
    GROUP BY strftime('%Y-%m', data)
    ORDER BY mes
'''

df6 = pd.read_sql_query(query6, conn)
print(df6.to_string(index=False))

conn.close()

print("\n" + "="*70)
print("✅ Análise concluída!")
print("="*70)
