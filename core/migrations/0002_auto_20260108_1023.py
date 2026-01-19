from django.db import migrations

def criar_dados_iniciais(apps, schema_editor):
    # Obtém os modelos históricos (segurança contra mudanças futuras)
    Servico = apps.get_model('core', 'Servico')
    Produto = apps.get_model('core', 'Produto')

    # --- 1. CRIAR SERVIÇOS ---
    lista_servicos = [
        {"nome": "Banho (Pequeno Porte)", "duracao": 45, "preco": 45.00},
        {"nome": "Banho (Grande Porte)", "duracao": 90, "preco": 80.00},
        {"nome": "Tosa Higiênica", "duracao": 30, "preco": 30.00},
        {"nome": "Tosa Completa (Máquina)", "duracao": 60, "preco": 70.00},
        {"nome": "Tosa na Tesoura", "duracao": 120, "preco": 120.00},
        {"nome": "Corte de Unhas", "duracao": 15, "preco": 15.00},
        {"nome": "Consulta Veterinária", "duracao": 40, "preco": 150.00},
        {"nome": "Vacinação (Aplicação)", "duracao": 20, "preco": 50.00},
    ]

    for item in lista_servicos:
        Servico.objects.get_or_create(
            nome=item["nome"],
            defaults={
                "duracao_estimada": item["duracao"], 
                "preco": item["preco"]
            }
        )

    # --- 2. CRIAR PRODUTOS (ESTOQUE INICIAL) ---
    lista_produtos = [
        {"nome": "Shampoo Neutro (Galão)", "qtd": 10, "venda": 0.00},
        {"nome": "Laço/Gravata (Unidade)", "qtd": 200, "venda": 2.50},
        {"nome": "Perfume Pet", "qtd": 20, "venda": 0.00},
        {"nome": "Ração Premium 1kg", "qtd": 15, "venda": 45.00},
        {"nome": "Petisco Bifinho", "qtd": 50, "venda": 5.00},
        {"nome": "Pipeta Anti-Pulgas", "qtd": 30, "venda": 85.00},
    ]

    for item in lista_produtos:
        Produto.objects.get_or_create(
            nome=item["nome"],
            defaults={
                "quantidade": item["qtd"], 
                "preco_venda": item["venda"]
            }
        )

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'), # Garante que roda DEPOIS de criar as tabelas
    ]

    operations = [
        migrations.RunPython(criar_dados_iniciais),
    ]