#!/usr/bin/env python3
"""Testes completos da API Furia Pay - Descobrir formato exato"""
import requests
import base64
import json
import time

public_key = "pk_KynpL7l3H-Qf-AsQw0FzSx1OR1kEoLYfvj_XBfwra6AUd0Ox"
secret_key = "sk_SWWj5eNt9JGj_Dv67Y_JDcgCDJZI-Sq5yT-her0gqNeFykZl"

credentials = f"{public_key}:{secret_key}"
auth_b64 = base64.b64encode(credentials.encode()).decode()

headers = {
    'Authorization': f'Basic {auth_b64}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def testar_payload(nome_teste, payload):
    print(f"\n{'='*60}")
    print(f"TESTE: {nome_teste}")
    print(f"{'='*60}")
    print("Payload:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(
            "https://api.furiapaybr.com/v1/transactions",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"\n✓ Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ SUCESSO! Transaction ID: {data.get('id')}")
            print(f"✓ QR Code: {data['pix']['qrcode'][:50]}...")
            print(f"✓ Expira em: {data['pix']['expirationDate']}")
            return True
        else:
            print(f"✗ FALHOU!")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ ERRO: {e}")
        return False

# TESTE 1: Payload mínimo absoluto
print("\n" + "="*60)
print("INICIANDO TESTES DE FORMATO FURIA PAY")
print("="*60)

# TESTE 1: Apenas campos obrigatórios
testar_payload("1. Apenas campos obrigatórios", {
    "amount": 100,
    "paymentMethod": "pix",
    "items": [{
        "title": "Teste",
        "unitPrice": 100,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TESTE",
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    }
})

# TESTE 2: Com email (sem phone)
testar_payload("2. Com email (sem phone)", {
    "amount": 100,
    "paymentMethod": "pix",
    "items": [{
        "title": "Teste",
        "unitPrice": 100,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TESTE",
        "email": "teste@email.com",
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    }
})

# TESTE 3: Com phone (sem email)
testar_payload("3. Com phone (sem email)", {
    "amount": 100,
    "paymentMethod": "pix",
    "items": [{
        "title": "Teste",
        "unitPrice": 100,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TESTE",
        "phone": "11987654321",
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    }
})

# TESTE 4: Com email e phone
testar_payload("4. Com email E phone", {
    "amount": 100,
    "paymentMethod": "pix",
    "items": [{
        "title": "Teste",
        "unitPrice": 100,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TESTE",
        "email": "teste@email.com",
        "phone": "11987654321",
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    }
})

# TESTE 5: Phone null explícito
testar_payload("5. Phone null explícito", {
    "amount": 100,
    "paymentMethod": "pix",
    "items": [{
        "title": "Teste",
        "unitPrice": 100,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TESTE",
        "email": "teste@email.com",
        "phone": None,
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    }
})

# TESTE 6: Email temporário
testar_payload("6. Email temporário", {
    "amount": 100,
    "paymentMethod": "pix",
    "items": [{
        "title": "Teste",
        "unitPrice": 100,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TESTE",
        "email": "10362198950@temp.com",
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    }
})

# TESTE 7: Com externalRef
testar_payload("7. Com externalRef", {
    "amount": 100,
    "paymentMethod": "pix",
    "items": [{
        "title": "Teste",
        "unitPrice": 100,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TESTE",
        "email": "teste@email.com",
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    },
    "externalRef": f"TEST_{int(time.time())}"
})

# TESTE 8: CPF com máscara (formatado)
testar_payload("8. CPF formatado (com pontos e traço)", {
    "amount": 100,
    "paymentMethod": "pix",
    "items": [{
        "title": "Teste",
        "unitPrice": 100,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TESTE",
        "email": "teste@email.com",
        "document": {
            "type": "cpf",
            "number": "103.621.989-50"  # Com formatação
        }
    }
})

# TESTE 9: Múltiplos items
testar_payload("9. Múltiplos items", {
    "amount": 200,
    "paymentMethod": "pix",
    "items": [
        {
            "title": "Item 1",
            "unitPrice": 100,
            "quantity": 1,
            "tangible": False
        },
        {
            "title": "Item 2",
            "unitPrice": 100,
            "quantity": 1,
            "tangible": False
        }
    ],
    "customer": {
        "name": "TESTE",
        "email": "teste@email.com",
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    }
})

# TESTE 10: Valor alto (R$ 149,42)
testar_payload("10. Valor real do sistema (R$ 149,42)", {
    "amount": 14942,
    "paymentMethod": "pix",
    "items": [{
        "title": "Regularização DARF - Imposto de Renda",
        "unitPrice": 14942,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TIAGO CARVALHO LOURENCINI",
        "email": "tiago.carvalho@gmail.com",
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    },
    "externalRef": f"DARF_{int(time.time())}"
})

# TESTE 11: Com metadata
testar_payload("11. Com metadata", {
    "amount": 100,
    "paymentMethod": "pix",
    "items": [{
        "title": "Teste",
        "unitPrice": 100,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TESTE",
        "email": "teste@email.com",
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    },
    "metadata": "Dados extras do pedido"
})

# TESTE 12: Com externalRef no item
testar_payload("12. Com externalRef no item", {
    "amount": 100,
    "paymentMethod": "pix",
    "items": [{
        "title": "Teste",
        "unitPrice": 100,
        "quantity": 1,
        "tangible": False,
        "externalRef": "ITEM_001"
    }],
    "customer": {
        "name": "TESTE",
        "email": "teste@email.com",
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    }
})

# TESTE 13: Nome com caracteres especiais
testar_payload("13. Nome com acentos e caracteres especiais", {
    "amount": 100,
    "paymentMethod": "pix",
    "items": [{
        "title": "Teste",
        "unitPrice": 100,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "JOSÉ DA SILVA JÚNIOR",
        "email": "jose@email.com",
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    }
})

# TESTE 14: Email inválido
testar_payload("14. Email sem domínio", {
    "amount": 100,
    "paymentMethod": "pix",
    "items": [{
        "title": "Teste",
        "unitPrice": 100,
        "quantity": 1,
        "tangible": False
    }],
    "customer": {
        "name": "TESTE",
        "email": "teste",  # Email inválido
        "document": {
            "type": "cpf",
            "number": "10362198950"
        }
    }
})

print("\n" + "="*60)
print("RESUMO DOS TESTES")
print("="*60)
print("\nAgora vou montar o payload PERFEITO baseado nos resultados...")
