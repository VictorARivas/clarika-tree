from django.contrib import admin
from django.urls import path

from tree import views

urlpatterns = [
    path('node-list/', views.node_list,name='node_list'),
    path('node-detail/<int:pk>/', views.node_detail, name='node_detail'),
    path('node-state/<int:pk>/', views.node_state, name='node_state'),
    path('sub-tree-list/', views.sub_tree_list, name='sub_tree_list'),
]   
