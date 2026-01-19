from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_funcionario = models.BooleanField(default=False, verbose_name="É Funcionário?")

    def __str__(self):
        return f"Perfil de {self.user.username}"

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    endereco = models.TextField(blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.telefone})"

class Pet(models.Model):
    ESPECIES = [('Cão', 'Cão'), ('Gato', 'Gato'), ('Outro', 'Outro')]
    
    dono = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pets')
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=ESPECIES)
    raca = models.CharField(max_length=50, blank=True)
    alertas = models.TextField(blank=True, help_text="Alergias, agressividade, etc.")

    def __str__(self):
        return f"{self.nome} - Dono: {self.dono.nome}"

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    duracao_estimada = models.IntegerField(default=60, help_text="Em minutos")
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField(default=0)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('Marcado', 'Marcado'),
        ('Em Serviço', 'Em Serviço'),
        ('Concluido', 'Aguardando Pagamento'), # Mudou de nome/função
        ('Finalizado', 'Finalizado (Pago)'),   # Status final definitivo
        ('Cancelado', 'Cancelado'),            # Novo status
    ]
    
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    funcionario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Marcado')
    
    observacoes_internas = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.data_inicio and self.servico:
            self.data_fim = self.data_inicio + timedelta(minutes=self.servico.duracao_estimada)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pet.nome} - {self.servico.nome}"

class ConsumoServico(models.Model):
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, related_name='consumos')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return f"Consumo: {self.produto.nome} ({self.quantidade})"

class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    funcionario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venda #{self.id}"

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()