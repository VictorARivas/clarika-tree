from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tree, SubTree
from .serializers import TreeSerializer, SubTreeSerializer
from django.shortcuts import get_object_or_404

class NodeListAPIView(APIView):
    def get(self, request):
        nodes = Tree.objects.all()
        serializer = TreeSerializer(nodes, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Check if there is a record with pk=1, if not, create one
        try:
            Tree.objects.get(pk=1)
        except Tree.DoesNotExist:
            Tree.objects.create(pk=1, valor="Default Node", state="active")

        # Proceed with the rest of the logic for the POST request
        if Tree.objects.count() >= 10:
            return Response({"error": "Cannot add more than 10 nodes to this tree, please delete one node"}, status=status.HTTP_400_BAD_REQUEST)

        valor = request.data.get('valor')
        state = request.data.get('state', 'active')
        if valor:
            node = Tree.objects.create(valor=valor, state=state)
            return Response({"message": "Node created Successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "'valor' field is required."}, status=status.HTTP_400_BAD_REQUEST)

class NodeDetailAPIView(RetrieveUpdateAPIView):
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    lookup_field = 'pk'

    def get(self, request, pk):
        # Get a detailed node 
        node = get_object_or_404(Tree, pk=pk)
        serializer = TreeSerializer(node)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        valor = request.data.get('valor')
        if valor:
            # Update the valor of the Tree record
            instance.valor = valor
            instance.save()
            return Response({"message": "Node updated Successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "'valor' field is required."}, status=status.HTTP_400_BAD_REQUEST) 

class SubTreeListAPIView(APIView):
    def get(self, request):
        # Get all subtrees
        subtrees = SubTree.objects.all()
        serializer = SubTreeSerializer(subtrees, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a new subtree
        serializer = SubTreeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NodeStateAPIView(RetrieveUpdateAPIView):
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer

    def partial_update(self, request, *args, **kwargs):
        tree = self.get_object()

        new_state = request.data.get('state')
        if new_state not in ['active', 'borrado']:
            return Response({"error": "Invalid value for 'state' field. It should be either 'active' or 'borrado'."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the state of the Tree record
        tree.state = new_state
        tree.save()

        # Update the state of related SubTree records if they exist
        related_subtrees = SubTree.objects.filter(tree_id=tree.pk)
        if related_subtrees.exists():
            for subtree in related_subtrees:
                subtree.state = new_state
                subtree.save()

        serializer = self.get_serializer(tree)
        return Response(serializer.data)
