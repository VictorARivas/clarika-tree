from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Tree, SubTree
from .serializers import TreeSerializer

class TestTreeViews(APITestCase):
    def setUp(self):
        # Create a Tree instance with pk=1 for testing
        Tree.objects.create(pk=1, valor="Root Node", state="active")
        self.subtree_data = {'valor': 'SubTree 1', 'state': 'active'}
        self.url = reverse('sub_tree_list')  # Assuming you've named the URL pattern

    def test_trees_list_GET(self):
        # Initialize the Django test client
        client = APIClient()

        # Send a GET request to the trees_list endpoint
        url = reverse('node_list')
        response = client.get(url)

        # Check the response status code and data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        trees = Tree.objects.all()
        serializer = TreeSerializer(trees, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_trees_list_POST(self):
        # Initialize the Django test client
        client = APIClient()

        # Send a POST request to the trees_list endpoint with valid data
        url = reverse('node_list')
        data = {'valor': 'New Node', 'state': 'active'}
        response = client.post(url, data)

        # Check the response status code and data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'message': 'Node created Successfully.'})

    def test_trees_list_POST_missing_valor(self):
        # Initialize the Django test client
        client = APIClient()

        # Send a POST request to the trees_list endpoint with missing 'valor' field
        url = reverse('node_list')
        data = {}
        response = client.post(url, data)

        # Check the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': "'valor' field is required."})

    def test_node_detail_GET(self):
        # Ensure we can retrieve a specific node using the GET request
        client = APIClient()  # Initialize the Django test client
        node_id = 1  # The ID of the node to retrieve
        url = reverse('node_detail', kwargs={'pk': node_id})
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        node = Tree.objects.get(pk=node_id)
        serializer = TreeSerializer(node)
        self.assertEqual(response.data, serializer.data)

    def test_node_detail_PATCH(self):
        # Ensure we can update the 'valor' field of a specific node using the PATCH request
        client = APIClient()  # Initialize the Django test client
        node_id = 1  # The ID of the node to update
        url = reverse('node_detail', kwargs={'pk': node_id})
        new_valor = 'Updated Node'  # The new value for the 'valor' field
        data = {'valor': new_valor}
        response = client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        node = Tree.objects.get(pk=node_id)
        self.assertEqual(node.valor, new_valor)

    def test_node_state_PATCH(self):
        # Ensure we can update the state of a Tree record and its related SubTree records
        client = APIClient()  # Initialize the Django test client

        # Create a Tree record and a related SubTree record for testing
        tree = Tree.objects.create(valor="Test Tree", state="active")
        subtree = SubTree.objects.create(tree_id=tree, valor="Test SubTree", state="active")

        # Send a PATCH request to the node_state endpoint to change the state to 'borrado'
        url = reverse('node_state', args=[tree.pk])
        data = {'state': 'borrado'}
        response = client.patch(url, data)

        # Check the response status code and updated Tree record data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 'borrado')

        # Check that the related SubTree record state is also updated to 'borrado'
        updated_subtree = SubTree.objects.get(pk=subtree.pk)
        self.assertEqual(updated_subtree.state, 'borrado')

        # Check that changing back the state to 'active' updates both Tree and SubTree states
        data = {'state': 'active'}
        response = client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 'active')

        # Check that the related SubTree record state is also updated back to 'active'
        updated_subtree = SubTree.objects.get(pk=subtree.pk)
        self.assertEqual(updated_subtree.state, 'active')       
    
    def test_create_sub_tree(self):
        # Ensure we can create a new SubTree object
        client = APIClient()  # Initialize the Django test client
        response = client.post(self.url, self.subtree_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SubTree.objects.count(), 1)
        self.assertEqual(SubTree.objects.get().valor, 'SubTree 1')
        self.assertEqual(SubTree.objects.get().state, 'active')

    def test_get_all_sub_trees(self):
        # Ensure we can get a list of all subtrees
        client = APIClient()  # Initialize the Django test client
        SubTree.objects.create(valor='SubTree 1', state='active')
        SubTree.objects.create(valor='SubTree 2', state='inactive')

        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['valor'], 'SubTree 1')
        self.assertEqual(response.data[1]['valor'], 'SubTree 2')
