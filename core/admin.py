from django.contrib import admin
from .models import (
    Pet, Servico, Agendamento, Produto, 
    ConsumoServico, Profile, Cliente, Venda, ItemVenda
)

# --- INLINES (Tabelas dentro de tabelas) ---

class ConsumoInline(admin.TabularInline):
    """Permite adicionar produtos consumidos dentro do Agendamento"""
    model = ConsumoServico
    extra = 1

class ItemVendaInline(admin.TabularInline):
    """Permite ver os itens vendidos dentro da tela de Venda"""
    model = ItemVenda
    extra = 0
    readonly_fields = ('subtotal',)

class PetInline(admin.StackedInline):
    """Permite ver/editar os Pets dentro da tela do Cliente"""
    model = Pet
    extra = 0

# --- ADMIN CLASSES ---

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'data_cadastro')
    search_fields = ('nome', 'telefone', 'email')
    inlines = [PetInline] # Mostra os pets deste cliente logo abaixo

class PetAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'raca', 'dono')
    list_filter = ('especie',)
    search_fields = ('nome', 'dono__nome') # Permite buscar pelo nome do dono

class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('pet', 'servico', 'data_inicio', 'status', 'funcionario')
    list_filter = ('status', 'data_inicio', 'funcionario')
    search_fields = ('pet__nome', 'pet__dono__nome') # Busca por pet ou dono
    inlines = [ConsumoInline]
    date_hierarchy = 'data_inicio' # Cria uma navegação por datas no topo

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade', 'preco_venda')
    list_filter = ('quantidade',)
    search_fields = ('nome',)

class VendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'funcionario', 'valor_total', 'data')
    list_filter = ('data', 'funcionario')
    search_fields = ('cliente__nome', 'funcionario__username')
    inlines = [ItemVendaInline]
    date_hierarchy = 'data'

# --- REGISTROS ---
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Pet, PetAdmin)
admin.site.register(Servico)
admin.site.register(Profile)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Agendamento, AgendamentoAdmin)
admin.site.register(Venda, VendaAdmin)