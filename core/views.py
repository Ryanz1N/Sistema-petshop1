from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db import transaction
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta, datetime

from rest_framework import viewsets
from .serializers import PetSerializer, AgendamentoSerializer

from .models import Agendamento, Cliente, Pet, Produto, ItemVenda, Venda, ConsumoServico
from .forms import ClienteForm, PetForm, AgendamentoForm, VendaForm, FuncionarioRegistroForm

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = FuncionarioRegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            if hasattr(user, 'profile'):
                user.profile.is_funcionario = True
                user.profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = FuncionarioRegistroForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    hoje = timezone.now().date()
    
    # 1. Lógica de Navegação de Data (Para a coluna 'Marcado')
    data_get = request.GET.get('data')
    if data_get:
        try:
            data_filtro = datetime.strptime(data_get, '%Y-%m-%d').date()
        except ValueError:
            data_filtro = hoje
    else:
        data_filtro = hoje

    # Calcula dia anterior e próximo para os links
    data_anterior = data_filtro - timedelta(days=1)
    data_proxima = data_filtro + timedelta(days=1)

    # 2. Automação (mantida)
    Agendamento.objects.filter(status='Em Serviço', data_fim__lte=timezone.now()).update(status='Concluido')
    
    # 3. Queries
    # Coluna Marcado: Filtra pela data selecionada nas setinhas
    marcado = Agendamento.objects.filter(status='Marcado', data_inicio__date=data_filtro).order_by('data_inicio')
    
    # Outras colunas: Mostra tudo que está ativo independente da data (para não perder nada de vista)
    em_servico = Agendamento.objects.filter(status='Em Serviço').order_by('data_inicio')
    pronto = Agendamento.objects.filter(status='Concluido').order_by('data_inicio')

    context = {
        'coluna_marcado': marcado,
        'coluna_servico': em_servico,
        'coluna_pronto': pronto,
        'data_filtro': data_filtro,
        'data_anterior': data_anterior,
        'data_proxima': data_proxima,
        'hoje': hoje,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def historico_view(request):
    # Pega os últimos 50 registros de cada para não pesar
    vendas = Venda.objects.all().order_by('-data')[:50]
    servicos = Agendamento.objects.filter(status='Finalizado').order_by('-data_inicio')[:50]
    
    return render(request, 'core/historico.html', {
        'vendas': vendas,
        'servicos': servicos
    })

@login_required
def cadastrar_cliente_pet(request):
    if request.method == 'POST':
        c_form = ClienteForm(request.POST, prefix='cliente')
        p_form = PetForm(request.POST, prefix='pet')
        
        if c_form.is_valid() and p_form.is_valid():
            cliente = c_form.save()
            pet = p_form.save(commit=False)
            pet.dono = cliente
            pet.save()
            messages.success(request, "Cliente e Pet cadastrados!")
            return redirect('novo_agendamento') 
    else:
        c_form = ClienteForm(prefix='cliente')
        p_form = PetForm(prefix='pet')

    return render(request, 'core/cadastro_cliente.html', {
        'c_form': c_form, 
        'p_form': p_form
    })

@login_required
def novo_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agenda = form.save(commit=False)
            agenda.funcionario = request.user
            agenda.save()
            messages.success(request, "Agendamento criado!")
            return redirect('home')
    else:
        form = AgendamentoForm()
    
    return render(request, 'core/form_agendamento.html', {'form': form})

@login_required
def detalhe_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    produtos = Produto.objects.filter(quantidade__gt=0)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                
                # AÇÃO: INICIAR ATENDIMENTO
                if 'iniciar_servico' in request.POST:
                    if agendamento.status == 'Marcado':
                        agendamento.status = 'Em Serviço'
                        agendamento.save()
                        messages.success(request, "Serviço iniciado! O tempo está contando.")
                
                # AÇÃO: CANCELAR AGENDAMENTO
                elif 'cancelar_servico' in request.POST:
                    if agendamento.status in ['Marcado', 'Em Serviço']:
                        agendamento.status = 'Cancelado'
                        agendamento.save()
                        messages.warning(request, "Agendamento cancelado.")
                        return redirect('home')

                # AÇÃO: FINALIZAR SERVIÇO MANUALMENTE (Para Concluido)
                elif 'concluir_manual' in request.POST:
                    agendamento.status = 'Concluido'
                    agendamento.save()
                    messages.success(request, "Serviço marcado como concluído. Aguardando pagamento.")

                # AÇÃO: ADICIONAR PRODUTO (Só se não estiver finalizado/cancelado)
                elif 'add_produto' in request.POST:
                    if agendamento.status not in ['Finalizado', 'Cancelado']:
                        prod_id = request.POST.get('produto_id')
                        prod_qtd = int(request.POST.get('produto_qtd', 0))
                        
                        if prod_id and prod_qtd > 0:
                            produto = Produto.objects.get(id=prod_id)
                            if produto.quantidade >= prod_qtd:
                                produto.quantidade -= prod_qtd
                                produto.save()
                                ConsumoServico.objects.create(agendamento=agendamento, produto=produto, quantidade=prod_qtd)
                                messages.success(request, "Produto adicionado.")
                            else:
                                messages.error(request, "Estoque insuficiente.")

                # AÇÃO: PAGAR E FINALIZAR (Definitivo)
                elif 'realizar_pagamento' in request.POST:
                    if agendamento.status == 'Concluido':
                        pagamento = request.POST.get('pagamento')
                        checklist = request.POST.get('checklist')
                        notas = request.POST.get('notas')
                        
                        if not pagamento:
                            messages.error(request, "Selecione a forma de pagamento.")
                        else:
                            agendamento.metodo_pagamento = pagamento
                            agendamento.checklist = checklist
                            agendamento.observacoes_internas = notas
                            agendamento.status = 'Finalizado' # Trava o sistema
                            agendamento.valor_final = agendamento.servico.preco # + produtos se quiser
                            agendamento.save()
                            messages.success(request, "Pagamento recebido e serviço encerrado!")
                            return redirect('home')

        except Exception as e:
            messages.error(request, f"Erro: {e}")
            
    return render(request, 'core/agendamento_detail.html', {
        'agendamento': agendamento,
        'produtos': produtos
    })

@login_required
def pdv(request):
    produtos = Produto.objects.filter(quantidade__gt=0)
    
    if request.method == 'POST':
        form = VendaForm(request.POST)
        p_ids = request.POST.getlist('produto_id')
        p_qtds = request.POST.getlist('produto_qtd')
        
        itens_validos = []
        for pid, qtd in zip(p_ids, p_qtds):
            if pid and qtd and int(qtd) > 0:
                itens_validos.append((pid, int(qtd)))

        if form.is_valid() and itens_validos:
            try:
                with transaction.atomic():
                    venda = form.save(commit=False)
                    venda.funcionario = request.user
                    venda.save()

                    total = 0
                    for pid, qtd in itens_validos:
                        prod = Produto.objects.select_for_update().get(id=pid)
                        if prod.quantidade >= qtd:
                            prod.quantidade -= qtd
                            prod.save()
                            subtotal = (prod.preco_venda or 0) * qtd
                            ItemVenda.objects.create(venda=venda, produto=prod, quantidade=qtd, subtotal=subtotal)
                            total += subtotal
                        else:
                            raise Exception(f"Sem estoque: {prod.nome}")

                    venda.valor_total = total
                    venda.save()
                    messages.success(request, f"Venda realizada: R$ {total}")
                    return redirect('home')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = VendaForm()

    return render(request, 'core/nova_venda.html', {'form': form, 'produtos': produtos})

