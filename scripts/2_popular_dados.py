import sqlite3
import random
from datetime import datetime, timedelta

print("="*70)
print("📥 POPULANDO BANCO DE DADOS COM DADOS DE TESTE")
print("="*70)

conn = sqlite3.connect('../database/auditoria.db')
cursor = conn.cursor()

# ============================================================
# 1. INSERIR FORNECEDORES
# ============================================================
print("\n1️⃣ Inserindo fornecedores...")

fornecedores = [
    ('Alimentos Integrados S.A.', '12.345.678/0001-90', 'Matéria-Prima', 1, '2020-01-15'),
    ('Tech Solutions Ltda', '98.765.432/0001-10', 'TI', 1, '2021-03-20'),
    ('Logística Express', '11.222.333/0001-44', 'Transporte', 1, '2019-07-10'),
    ('Manutenção Industrial', '55.666.777/0001-88', 'Serviços', 1, '2020-11-05'),
    ('Embalagens Premium', '33.444.555/0001-99', 'Embalagens', 1, '2021-02-28'),
    ('Consultoria Empresarial', '77.888.999/0001-22', 'Consultoria', 0, '2018-05-12'),
]

cursor.executemany('''
    INSERT OR IGNORE INTO fornecedores (nome, cnpj, categoria, ativo, data_cadastro)
    VALUES (?, ?, ?, ?, ?)
''', fornecedores)

print(f"   ✅ {cursor.rowcount} fornecedores inseridos")

# ============================================================
# 2. INSERIR DEPARTAMENTOS
# ============================================================
print("\n2️⃣ Inserindo departamentos...")

departamentos = [
    ('Compras', 'Maria Silva', 500000.00, 'CC-001'),
    ('TI', 'João Santos', 300000.00, 'CC-002'),
    ('Operações', 'Carlos Oliveira', 800000.00, 'CC-003'),
    ('Manutenção', 'Ana Costa', 200000.00, 'CC-004'),
    ('Marketing', 'Paulo Ferreira', 150000.00, 'CC-005'),
]

cursor.executemany('''
    INSERT OR IGNORE INTO departamentos (nome, gestor, orcamento_mensal, centro_custo)
    VALUES (?, ?, ?, ?)
''', departamentos)

print(f"   ✅ {cursor.rowcount} departamentos inseridos")

# ============================================================
# 3. INSERIR PAGAMENTOS
# ============================================================
print("\n3️⃣ Inserindo pagamentos...")

random.seed(42)
data_inicial = datetime(2024, 1, 1)

pagamentos = []
for i in range(300):
    codigo = f'PAG-2024-{i+1:04d}'
    data = data_inicial + timedelta(days=random.randint(0, 365))
    fornecedor_id = random.randint(1, 6)
    departamento_id = random.randint(1, 5)
    valor = round(random.uniform(1000, 100000), 2)
    tipo_pag = random.choice(['Boleto', 'TED', 'PIX', 'Cheque'])
    status = random.choice(['Aprovado', 'Pendente', 'Pago'])
    aprovador = random.choice(['Gestor A', 'Gestor B', 'Gestor C', 'Diretor'])
    
    pagamentos.append((
        codigo, data.strftime('%Y-%m-%d'), fornecedor_id, departamento_id,
        valor, tipo_pag, status, aprovador, None
    ))

# Adicionar alguns pagamentos duplicados (para auditoria detectar)
for i in range(15):
    pagamentos.append(pagamentos[i])

# Adicionar pagamentos suspeitos (valores muito altos)
for i in range(10):
    codigo = f'PAG-2024-SUSP-{i+1:02d}'
    data = data_inicial + timedelta(days=random.randint(0, 365))
    valor = round(random.uniform(200000, 500000), 2)  # Valores altíssimos
    
    pagamentos.append((
        codigo, data.strftime('%Y-%m-%d'), random.randint(1, 6),
        random.randint(1, 5), valor, 'TED', 'Aprovado', 'Diretor',
        'Pagamento de alto valor'
    ))

cursor.executemany('''
    INSERT OR IGNORE INTO pagamentos 
    (codigo_pagamento, data, fornecedor_id, departamento_id, valor, 
     tipo_pagamento, status, aprovador, observacoes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', pagamentos)

print(f"   ✅ {cursor.rowcount} pagamentos inseridos")

# Salvar tudo
conn.commit()

# ============================================================
# 4. ESTATÍSTICAS
# ============================================================
print("\n" + "="*70)
print("📊 ESTATÍSTICAS DO BANCO DE DADOS")
print("="*70)

cursor.execute("SELECT COUNT(*) FROM fornecedores")
print(f"\n👥 Fornecedores cadastrados: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM departamentos")
print(f"🏢 Departamentos: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM pagamentos")
print(f"💰 Pagamentos registrados: {cursor.fetchone()[0]}")

cursor.execute("SELECT SUM(valor) FROM pagamentos")
total = cursor.fetchone()[0]
print(f"💵 Valor total: R$ {total:,.2f}")

cursor.execute("SELECT AVG(valor) FROM pagamentos")
media = cursor.fetchone()[0]
print(f"📊 Ticket médio: R$ {media:,.2f}")

conn.close()

print("\n✅ Dados inseridos com sucesso!")
print("="*70)
