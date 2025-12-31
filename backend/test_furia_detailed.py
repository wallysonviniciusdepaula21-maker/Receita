#!/usr/bin/env python3
"""Teste detalhado da API Furia Pay com logs completos"""
import requests
import base64
import json
import time

# Chaves
public_key = "pk_KynpL7l3H-Qf-AsQw0FzSx1OR1kEoLYfvj_XBfwra6AUd0Ox"
secret_key = "sk_SWWj5eNt9JGj_Dv67Y_JDcgCDJZI-Sq5yT-her0gqNeFykZl"

# Base64 encode
credentials = f"{public_key}:{secret_key}"
auth_b64 = base64.b64encode(credentials.encode()).decode()

print("="*60)
print("TESTE DETALHADO FURIA PAY API")
print("="*60)

# Teste 1: Listar transações existentes
print("\n[1] Tentando listar transações existentes...")
headers = {
    'Authorization': f'Basic {auth_b64}',
    'Accept': 'application/json'
}

try:
    response = requests.get(
        "https://api.furiapaybr.com/v1/transactions",
        headers=headers,
        timeout=10
    )
    print(f"    Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"    Total de transações: {len(data.get('data', []))}")
        if data.get('data'):
            print(f"    Primeira transação: {json.dumps(data['data'][0], indent=2)}")
    else:
        print(f"    Response: {response.text[:200]}")
except Exception as e:
    print(f"    Erro: {e}")

# Teste 2: Tentar criar com valores mínimos
print("\n[2] Criando transação com payload mínimo...")
payload_minimo = {
    "amount": 100,  # R$ 1,00
    "paymentMethod": "pix",
    "items": [{
        "title": "Teste",
        "unitPrice": 100,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TESTE",
        "documentNumber": "00000000000",
        "email": "teste@teste.com",
        "phoneNumber": "11999999999"
    }
}

headers_post = {
    'Authorization': f'Basic {auth_b64}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

try:
    response = requests.post(
        "https://api.furiapaybr.com/v1/transactions",
        json=payload_minimo,
        headers=headers_post,
        timeout=30
    )
    print(f"    Status: {response.status_code}")
    print(f"    Response completa: {response.text}")
    print(f"    Headers: {dict(response.headers)}")
except Exception as e:
    print(f"    Erro: {e}")

# Teste 3: Verificar se tem alguma configuração de PIX
print("\n[3] Verificando dados da empresa...")
try:
    response = requests.get(
        "https://api.furiapaybr.com/v1/company",
        headers=headers,
        timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        print(f"    Empresa: {data.get('commercialName')}")
        print(f"    Status: {data.get('status')}")
        print(f"    Blocked: {data.get('blocked')}")
        print(f"    Produtos tangíveis: {data.get('tangibleProducts')}")
        
        # Verificar se tem informações sobre métodos de pagamento
        if 'paymentMethods' in data:
            print(f"    Métodos de pagamento: {data['paymentMethods']}")
        
        # Mostrar campos relacionados a configuração
        campos_config = ['acquirer', 'gateway', 'pixKey', 'paymentConfig', 'settings']
        for campo in campos_config:
            if campo in data:
                print(f"    {campo}: {data[campo]}")
except Exception as e:
    print(f"    Erro: {e}")

# Teste 4: Tentar criar com CPF válido
print("\n[4] Criando com CPF válido (10362198950)...")
payload_cpf_valido = {
    "amount": 14942,
    "paymentMethod": "pix",
    "pix": {
        "expiresInMinutes": 1440
    },
    "items": [{
        "title": "Regularização DARF",
        "unitPrice": 14942,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TIAGO CARVALHO LOURENCINI",
        "documentNumber": "10362198950",
        "email": "tiago@email.com",
        "phoneNumber": "11987654321"
    },
    "externalRef": f"TEST_{int(time.time())}"
}

try:
    response = requests.post(
        "https://api.furiapaybr.com/v1/transactions",
        json=payload_cpf_valido,
        headers=headers_post,
        timeout=30
    )
    print(f"    Status: {response.status_code}")
    print(f"    Response: {response.text}")
    
    # Se tiver mais detalhes no header
    if 'x-error-detail' in response.headers:
        print(f"    Erro detalhe: {response.headers['x-error-detail']}")
    
    # Tentar pegar resposta JSON
    try:
        error_json = response.json()
        print(f"    JSON completo:")
        print(json.dumps(error_json, indent=2))
    except:
        pass
        
except Exception as e:
    print(f"    Erro: {e}")

print("\n" + "="*60)
print("FIM DOS TESTES")
print("="*60)
