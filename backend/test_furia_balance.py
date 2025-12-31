import requests
import base64

public_key = "pk_KynpL7l3H-Qf-AsQw0FzSx1OR1kEoLYfvj_XBfwra6AUd0Ox"
secret_key = "sk_SWWj5eNt9JGj_Dv67Y_JDcgCDJZI-Sq5yT-her0gqNeFykZl"

credentials = f"{public_key}:{secret_key}"
auth_b64 = base64.b64encode(credentials.encode()).decode()

headers = {
    'Authorization': f'Basic {auth_b64}',
    'Accept': 'application/json'
}

print("Testando endpoint de saldo...")
response = requests.get(
    "https://api.furiapaybr.com/v1/balance",
    headers=headers,
    timeout=10
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
