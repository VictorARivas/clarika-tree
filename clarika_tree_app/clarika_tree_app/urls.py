from django.contrib import admin
from django.urls import path

from tree import views

urlpatterns = [
    path('node-list/', views.NodeListAPIView.as_view(), name='node_list'),    
    path('node-detail/<int:pk>/', views.NodeDetailAPIView.as_view(), name='node_detail'),
    path('node-state/<int:pk>/', views.NodeStateAPIView.as_view(), name='node_state'),
    path('sub-tree-list/', views.SubTreeListAPIView.as_view(), name='sub_tree_list'),
]
