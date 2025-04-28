from supersetpyclient.client import SupersetClient

client = SupersetClient(
    host="http://localhost:8088",
    username="admin",
    password="admin",
)

roles = client.add_user_to_role("test@canonical.com", "custom_role")

print(roles)
