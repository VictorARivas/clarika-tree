from django.db import models

class Tree(models.Model):
    valor = models.CharField(max_length=30)
    state = models.CharField(max_length=8, default="active")

class SubTree(models.Model):
    tree_id = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name='children', default=1)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    valor = models.CharField(max_length=30)
    state = models.CharField(max_length=8, default="active")
    
