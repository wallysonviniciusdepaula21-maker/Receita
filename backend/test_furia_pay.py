#!/usr/bin/env python3
"""Teste direto da API Furia Pay"""
import requests
import base64
import json

# Chaves
public_key = "pk_KynpL7l3H-Qf-AsQw0FzSx1OR1kEoLYfvj_XBfwra6AUd0Ox"
secret_key = "sk_SWWj5eNt9JGj_Dv67Y_JDcgCDJZI-Sq5yT-her0gqNeFykZl"

# Base64 encode
credentials = f"{public_key}:{secret_key}"
auth_b64 = base64.b64encode(credentials.encode()).decode()

print(f"Chaves configuradas:")
print(f"  Public: {public_key}")
print(f"  Secret: {secret_key[:20]}...")
print(f"\nAuth Basic: {auth_b64[:50]}...")

# Payload mínimo
payload = {
    "amount": 14942,
    "paymentMethod": "pix",
    "pix": {"expiresInMinutes": 1440},
    "items": [{
        "title": "Teste PIX",
        "unitPrice": 14942,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TESTE USUARIO",
        "documentNumber": "10362198950",
        "email": "teste@teste.com",
        "phoneNumber": "11999999999"
    },
    "externalRef": "TEST_" + str(int(time.time())),
    "metadata": "Teste integração"
}

headers = {
    'Authorization': f'Basic {auth_b64}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

print(f"\nPayload:")
print(json.dumps(payload, indent=2))

print(f"\nHeaders:")
for k, v in headers.items():
    if k == 'Authorization':
        print(f"  {k}: Basic {v.split()[1][:30]}...")
    else:
        print(f"  {k}: {v}")

print(f"\n📡 Fazendo requisição para: https://api.furiapaybr.com/v1/transactions")

try:
    response = requests.post(
        "https://api.furiapaybr.com/v1/transactions",
        json=payload,
        headers=headers,
        timeout=30
    )
    
    print(f"\n✓ Status Code: {response.status_code}")
    print(f"✓ Response Headers:")
    for k, v in response.headers.items():
        print(f"  {k}: {v}")
    
    print(f"\n✓ Response Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
        
except Exception as e:
    print(f"\n✗ Erro: {e}")

import time
