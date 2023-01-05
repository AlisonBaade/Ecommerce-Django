from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify

class Produto(models.Model):

    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to='produto_imagens/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(default=0)
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variavel'),
            ('S', 'Simples'),
        )
    )
    
    def get_preco_formatado(self):
        return f'R$ {self.preco_marketing:.2f}'.replace('.',',')
    get_preco_formatado.short_description = 'Preço'
    
    def get_preco_promo_formatado(self):
        return f'R$ {self.preco_marketing_promocional:.2f}'.replace('.',',')
    get_preco_promo_formatado.short_description = 'Preço Promo'

    @staticmethod  # DEFININDO COMO MÉTODO ESTÁTICO ############
    def resize_image(img, new_width=800):  # Trabalhndo com as imagens #################
        # caminho completo da imagem
        img_full_patch = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_patch)
        original_width, original_heigth = img_pil.size  # tamanho total da imagem

        if original_width <= new_width:
            # print('Largura original menor que nova largura')
            img_pil.close()
            return

        new_heigth = round((new_width * original_heigth) / original_width)

        # LANCZOS calculo para fazer alteração de pixels para qualidade de imagem
        new_img = img_pil.resize((new_width, new_heigth), Image.LANCZOS)
        new_img.save(
            img_full_patch,
            optimize=True,
            quality=50
        )
        # print('A imagem foi redimensionada')

    def save(self, *args, **kwargs):
        
        if not self.slug: # tratamento de urls automática
            slug = f'{slugify(self.nome)}'
            self.slug = slug
            
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):  # FUNÇÃO PARA QUE APAREÇA O NOME DOS PRODUTOS E NÃO PRODUCTS OBJECTS ##########
        return self.nome
    


class Variacao(models.Model):
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1) # definindo que a variação começe com 1
    
    def __str__(self):
        return self.nome or self.produto.nome
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'