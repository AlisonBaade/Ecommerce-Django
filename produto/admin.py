from django.contrib import admin
from . import models


# FAZENDO COM QUE OS CAMPOS DE ALTERAÇÃO 
# APAREÇAM NA PAGINA DE CADASTRO DO PRODUTO NA AREA DA ADMIN

class VariacaoInLine(admin.TabularInline):
    model = models.Variacao
    extra = 1
    
    
    
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome',
                    'descricao_curta',
                    'get_preco_formatado',
                    'get_preco_promo_formatado']
    inlines = [
        VariacaoInLine
    ]
    
#########################################

# REGISTRANDO AS MODELS
admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao)