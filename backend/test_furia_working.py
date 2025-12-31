import requests
import base64
import json
import time

public_key = "pk_KynpL7l3H-Qf-AsQw0FzSx1OR1kEoLYfvj_XBfwra6AUd0Ox"
secret_key = "sk_SWWj5eNt9JGj_Dv67Y_JDcgCDJZI-Sq5yT-her0gqNeFykZl"

credentials = f"{public_key}:{secret_key}"
auth_b64 = base64.b64encode(credentials.encode()).decode()

# Payload que deve funcionar (baseado na transação existente)
payload = {
    "amount": 14942,
    "paymentMethod": "pix",
    "items": [{
        "title": "Regularização DARF - Imposto de Renda",
        "quantity": 1,
        "tangible": False,
        "unitPrice": 14942,
        "externalRef": ""
    }],
    "customer": {
        "name": "TIAGO CARVALHO LOURENCINI",
        "email": "tiago.carvalho@gmail.com",
        "phone": None,
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    },
    "externalRef": f"DARF_{int(time.time())}"
}

headers = {
    'Authorization': f'Basic {auth_b64}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

print("Criando transação PIX com estrutura correta...")
print(json.dumps(payload, indent=2))

response = requests.post(
    "https://api.furiapaybr.com/v1/transactions",
    json=payload,
    headers=headers,
    timeout=30
)

print(f"\n✓ Status: {response.status_code}")
print(f"✓ Response:")
print(json.dumps(response.json(), indent=2))
