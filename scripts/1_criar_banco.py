import sqlite3
import os

print("="*70)
print("🏗️  CRIANDO BANCO DE DADOS DE AUDITORIA")
print("="*70)

# Garantir que a pasta database existe
os.makedirs('../database', exist_ok=True)

# Conectar ao banco (cria se não existir)
conn = sqlite3.connect('../database/auditoria.db')
cursor = conn.cursor()

print("\n📊 Criando tabelas...")

# ============================================================
# TABELA 1: FORNECEDORES
# ============================================================
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fornecedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cnpj TEXT UNIQUE NOT NULL,
        categoria TEXT,
        ativo INTEGER DEFAULT 1,
        data_cadastro TEXT
    )
''')
print("✅ Tabela 'fornecedores' criada")

# ============================================================
# TABELA 2: DEPARTAMENTOS
# ============================================================
cursor.execute('''
    CREATE TABLE IF NOT EXISTS departamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        gestor TEXT,
        orcamento_mensal REAL,
        centro_custo TEXT
    )
''')
print("✅ Tabela 'departamentos' criada")

# ============================================================
# TABELA 3: PAGAMENTOS
# ============================================================
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pagamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_pagamento TEXT UNIQUE NOT NULL,
        data TEXT NOT NULL,
        fornecedor_id INTEGER NOT NULL,
        departamento_id INTEGER NOT NULL,
        valor REAL NOT NULL,
        tipo_pagamento TEXT,
        status TEXT DEFAULT 'Pendente',
        aprovador TEXT,
        observacoes TEXT,
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id),
        FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
    )
''')
print("✅ Tabela 'pagamentos' criada")

# ============================================================
# TABELA 4: AUDITORIA_LOG (para rastreamento)
# ============================================================
cursor.execute('''
    CREATE TABLE IF NOT EXISTS auditoria_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_auditoria TEXT NOT NULL,
        tipo_achado TEXT,
        descricao TEXT,
        pagamento_id INTEGER,
        severidade TEXT,
        FOREIGN KEY (pagamento_id) REFERENCES pagamentos(id)
    )
''')
print("✅ Tabela 'auditoria_log' criada")

# Salvar alterações
conn.commit()

# Verificar tabelas criadas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tabelas = cursor.fetchall()

print("\n📋 Tabelas no banco de dados:")
for tabela in tabelas:
    print(f"   • {tabela[0]}")

# Fechar conexão
conn.close()

print("\n✅ Banco de dados criado com sucesso!")
print(f"📁 Local: database/auditoria.db")
print("="*70)
