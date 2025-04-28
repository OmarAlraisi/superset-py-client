"""Superset Client."""
import requests
from typing import List, Optional
from supersetpyclient.models import User, Role


class SupersetClient:
    def __init__(self, host: str, username: str, password: str):
        self.base_url = f"{host}/api/v1"
        access_token = self.authenticate(username, password)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

    def authenticate(self, username: str, password: str):
        reponse = requests.post(
            f"{self.base_url}/security/login",
            headers={
                "Content-Type": "application/json",
            },
            json={
                "username": username,
                "password": password,
                "provider": "db",
            }
        )
        return reponse.json().get("access_token")

    def get_users(self):
        response = requests.get(
            f"{self.base_url}/security/users",
            headers=self.headers
        )

        users: List[User] = []
        raw_users = response.json().get("result")
        for raw_user in raw_users:
            user = User(username=raw_user.get(
                "username"), id=raw_user.get("id"))
            for r in raw_user.get("roles"):
                user.roles.append(r.get("id"))
            users.append(user)

        return users

    def get_roles(self):
        response = requests.get(
            f"{self.base_url}/security/roles/search",
            headers=self.headers,
        )

        roles: List[Role] = []
        for role in response.json().get("result"):
            roles.append(
                Role(
                    id=role.get("id"),
                    name=role.get("name"),
                    users=role.get("user_ids")
                )
            )
        return roles

    def _create_role_if_not_exist(self, role_name: str):
        roles = self.get_roles()
        role = next((r for r in roles if r.name == role_name), None)
        if role is not None:
            return role.id

        response = requests.post(
            f"{self.base_url}/security/roles",
            headers=self.headers,
            json={"name": role_name}
        )

        return response.json().get("id")

    def add_user_to_role(self, username: str, role_name: str):
        # create role if not exists
        role_id = self._create_role_if_not_exist(role_name)

        # add user to role
        users = self.get_users()
        user = next((u for u in users if u.username == username), None)
        if user is None:
            raise Exception("Failed to add user to role. User does not exist")

        role_exists = next((r for r in user.roles if r == role_id), None)
        if role_exists is not None:
            # user is already added to the role
            return

        user.roles.append(role_id)
        response = requests.put(
            f"{self.base_url}/security/users/{user.id}",
            headers=self.headers,
            json={
                "roles": user.roles,
            }
        )
        return response.json()
