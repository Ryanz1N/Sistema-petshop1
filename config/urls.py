from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from core.forms import EmailLoginForm

# Importando todas as views necessárias do app Core
from core.views import (
    dashboard, register, cadastrar_cliente_pet, 
    novo_agendamento, detalhe_agendamento, pdv, historico_view,
    PetViewSet, AgendamentoViewSet
)

# Rotas da API (Mantendo a estrutura original)
router = DefaultRouter()
router.register(r'api/pets', PetViewSet)
router.register(r'api/agendamentos', AgendamentoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- AUTENTICAÇÃO ---
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=EmailLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # --- SISTEMA PRINCIPAL ---
    path('', dashboard, name='home'),
    path('cadastro-cliente/', cadastrar_cliente_pet, name='cadastro_cliente'),
    path('novo-agendamento/', novo_agendamento, name='novo_agendamento'),
    
    # --- NOVAS ROTAS (QUE FALTAVAM) ---
    path('pdv/', pdv, name='pdv'), # Tela de Vendas
    path('agendamento/<int:pk>/', detalhe_agendamento, name='detalhe_agendamento'), # Tela de Execução/Checkout
    path('historico/', historico_view, name='historico'),

    # --- API ---
    path('api/', include(router.urls)),
]