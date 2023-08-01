# clarika-tree

Welcome to Clarika Tree, the code challenge.

## Usage
To run the development server, use the following command:
```bash
python3 manage.py runserver
```
## Endpoints
- GET /node-list/

  __Get a list of all tree nodes.__

- POST /node-list/

  __Create a new tree node.__

- GET /sub-tree-list/

  __Get a list of all subtree nodes.__

- POST /sub-tree-list/

  __Create a new subtree node.__

- GET /node-detail/{pk}/

  __Get details of a specific tree node.__

- PATCH /node-detail/{pk}/

  __Update the 'valor' field of a specific tree node.__

- PATCH /node-state/{pk}/

  __Toggle the 'state' field of a specific tree node between 'active' and 'borrado'. This will also update the 'state' field of related subtree nodes to 'borrado'.__

## Testing
According to the Challenge notes there is no need to implement a DB, so, in order to test this project please run following command inside the _**clarika_tree_app**_ directory

```bash
python3 manage.py test
```
