# SupersetPyClient

Simple Python client to manage roles in Apache Superset via its REST API.

## Usage

```Python
from supersetpyclient.client import SupersetClient

client = SupersetClient(
    host="http://localhost:8088",
    username="admin",
    password="admin"
)

# List of all users and roles
users = client.get_users()
roles = client.get_roles()

# Add or remove a user from a role
client.add_user_to_role("user@email.com", "custom_role")
client.remove_user_from_role("user@email.com", "custom_role")
```
