# Contratos de API e Plano de Integração Backend

## Visão Geral do Sistema
Sistema de regularização de CPF e declaração do Imposto de Renda com geração de DARF e pagamento via PIX.

## Fluxo de Páginas
1. **Login** (`/`) - Entrada de CPF
2. **Loading** (`/loading`) - Validação CPF (6s)
3. **Resultado** (`/resultado`) - Status do CPF e irregularidades
4. **DARF** (`/darf`) - Documento de arrecadação
5. **Loading PIX** (`/loading-pix`) - Geração do PIX (6s)
6. **Pagamento PIX** (`/pagamento-pix`) - QR Code e código PIX

---

## 1. API Endpoints Necessários

### 1.1 POST `/api/cpf/consultar`
**Descrição**: Consulta status do CPF na base de dados

**Request:**
```json
{
  "cpf": "012.302.462-58"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "name": "Natanael Sales Pantoja",
    "cpf": "012.302.462-58",
    "birthDate": "24/09/1975",
    "status": "IRREGULAR",
    "declaration2023": "NÃO ENTREGUE",
    "protocol": "CTP9513859",
    "deadline": "20/12/2025",
    "statusType": "CRÍTICO"
  }
}
```

### 1.2 GET `/api/darf/:protocol`
**Descrição**: Gera DARF com base no protocolo

**Response:**
```json
{
  "success": true,
  "data": {
    "protocolo": "CTP9513859",
    "contribuinte": "Natanael Sales Pantoja",
    "cpf": "012.302.462-58",
    "periodoApuracao": "18/11/2024",
    "dataVencimento": "20/12/2025",
    "codigoReceita": "8045",
    "numeroReferencia": "CTP9513859",
    "valorPrincipal": 98.44,
    "multa": 35.28,
    "juros": 17.70,
    "valorTotal": 149.42
  }
}
```

### 1.3 POST `/api/pix/gerar`
**Descrição**: Gera código PIX para pagamento

**Request:**
```json
{
  "protocol": "CTP9513859",
  "value": 149.42,
  "cpf": "012.302.462-58"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "pixCode": "00020101021226940014br.gov.bcb.pix...",
    "qrCodeUrl": "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=...",
    "expiresAt": "2025-12-21T15:00:00Z"
  }
}
```

### 1.4 GET `/api/pix/verificar/:protocol`
**Descrição**: Verifica se o pagamento PIX foi confirmado

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "PENDENTE" | "PAGO" | "EXPIRADO",
    "paidAt": "2025-12-20T14:30:00Z" // se pago
  }
}
```

---

## 2. Dados Mockados no Frontend

### Arquivo: `/app/frontend/src/mock.js` (NÃO EXISTE AINDA)
Atualmente os dados estão hardcoded nas páginas. Precisa criar:

```javascript
export const mockUserData = {
  name: 'Natanael Sales Pantoja',
  cpf: '012.302.462-58',
  birthDate: '24/09/1975',
  status: 'IRREGULAR',
  declaration2023: 'NÃO ENTREGUE',
  protocol: 'CTP9513859',
  deadline: '20/12/2025',
  statusType: 'CRÍTICO'
};

export const mockDarfData = {
  protocolo: 'CTP9513859',
  contribuinte: 'Natanael Sales Pantoja',
  cpf: '012.302.462-58',
  periodoApuracao: '18/11/2024',
  dataVencimento: '20/12/2025',
  codigoReceita: '8045',
  numeroReferencia: 'CTP9513859',
  valorPrincipal: 98.44,
  multa: 35.28,
  juros: 17.70,
  valorTotal: 149.42
};
```

---

## 3. Models do MongoDB

### 3.1 CPF Model
```python
class CPF(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cpf: str
    name: str
    birth_date: str
    status: str  # REGULAR, IRREGULAR
    declaration_2023: str  # ENTREGUE, NÃO ENTREGUE
    protocol: str
    deadline: str
    status_type: str  # NORMAL, CRÍTICO
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 3.2 DARF Model
```python
class DARF(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    protocol: str
    contribuinte: str
    cpf: str
    periodo_apuracao: str
    data_vencimento: str
    codigo_receita: str
    numero_referencia: str
    valor_principal: float
    multa: float
    juros: float
    valor_total: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 3.3 PIX Payment Model
```python
class PixPayment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    protocol: str
    cpf: str
    value: float
    pix_code: str
    qr_code_url: str
    status: str  # PENDENTE, PAGO, EXPIRADO
    expires_at: datetime
    paid_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## 4. Integração Frontend → Backend

### Arquivos a modificar:

#### 4.1 `/app/frontend/src/components/LoginCard.jsx`
```javascript
// ANTES (mock)
const handleSubmit = (e) => {
  e.preventDefault();
  navigate('/loading');
};

// DEPOIS (API)
const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await axios.post(`${API}/cpf/consultar`, {
      cpf: cpf.replace(/\D/g, '')
    });
    // Salvar dados no localStorage ou context
    localStorage.setItem('userData', JSON.stringify(response.data.data));
    navigate('/loading');
  } catch (error) {
    toast({ title: "Erro", description: "CPF não encontrado" });
  }
};
```

#### 4.2 `/app/frontend/src/pages/Loading.jsx`
```javascript
// Após 6 segundos, verificar se dados foram salvos
useEffect(() => {
  const userData = localStorage.getItem('userData');
  if (userData) {
    setTimeout(() => navigate('/resultado'), 6000);
  } else {
    navigate('/');
  }
}, []);
```

#### 4.3 `/app/frontend/src/pages/Resultado.jsx`
```javascript
// ANTES (mock)
const userData = { ... hardcoded ... };

// DEPOIS (API)
const [userData, setUserData] = useState(null);

useEffect(() => {
  const data = JSON.parse(localStorage.getItem('userData'));
  setUserData(data);
}, []);
```

#### 4.4 `/app/frontend/src/pages/Darf.jsx`
```javascript
// Buscar DARF da API ao carregar página
useEffect(() => {
  const fetchDarf = async () => {
    const userData = JSON.parse(localStorage.getItem('userData'));
    const response = await axios.get(`${API}/darf/${userData.protocol}`);
    setDarfData(response.data.data);
  };
  fetchDarf();
}, []);
```

#### 4.5 `/app/frontend/src/pages/PagamentoPix.jsx`
```javascript
// Gerar PIX ao carregar página
useEffect(() => {
  const generatePix = async () => {
    const userData = JSON.parse(localStorage.getItem('userData'));
    const response = await axios.post(`${API}/pix/gerar`, {
      protocol: userData.protocol,
      value: 149.42,
      cpf: userData.cpf
    });
    setPixData(response.data.data);
  };
  generatePix();
}, []);

// Verificar pagamento a cada 30s
useEffect(() => {
  const interval = setInterval(async () => {
    const userData = JSON.parse(localStorage.getItem('userData'));
    const response = await axios.get(`${API}/pix/verificar/${userData.protocol}`);
    if (response.data.data.status === 'PAGO') {
      toast({ title: "Pagamento confirmado!" });
      // Redirecionar para página de sucesso
    }
  }, 30000);
  return () => clearInterval(interval);
}, []);
```

---

## 5. Implementação Backend

### Estrutura de arquivos:
```
/app/backend/
├── server.py (já existe)
├── models/
│   ├── cpf.py
│   ├── darf.py
│   └── pix.py
├── routes/
│   ├── cpf_routes.py
│   ├── darf_routes.py
│   └── pix_routes.py
└── services/
    ├── cpf_service.py
    ├── darf_service.py
    └── pix_service.py
```

---

## 6. Próximos Passos

1. ✅ Frontend completo com mock data
2. ⏳ Criar models do MongoDB
3. ⏳ Implementar endpoints da API
4. ⏳ Integrar frontend com backend
5. ⏳ Testar fluxo completo end-to-end
6. ⏳ Implementar webhook de pagamento PIX (simulado)

---

## 7. Observações Importantes

- **Todos os dados são mockados** no frontend atualmente
- CPF usado para testes: `012.302.462-58` ou qualquer outro
- Valores do DARF: R$ 98,44 + R$ 35,28 + R$ 17,70 = R$ 149,42
- Timer de contagem regressiva é apenas visual
- Código PIX é simulado
- QR Code é gerado via API pública (qrserver.com)
