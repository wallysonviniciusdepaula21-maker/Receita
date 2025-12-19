# 🔐 CONFIGURAÇÃO FURIA PAY - CHAVE SECRETA

## ⚠️ ATENÇÃO: PENDENTE CONFIGURAÇÃO

A integração com o **Furia Pay BR** está 100% implementada, mas falta apenas **1 passo**:

---

## 📝 O QUE FAZER:

### 1. Obter a Chave Secreta
- Acesse: https://app.furiapaybr.com/integrations
- Faça login na sua conta
- Clique em **"Revelar Chave"** ao lado da Chave Secreta
- Copie a chave completa

### 2. Configurar no Sistema
Abra o arquivo `/app/backend/.env` e substitua:

```bash
FURIAPAY_SECRET_KEY=COLE_SUA_CHAVE_SECRETA_AQUI
```

Por:

```bash
FURIAPAY_SECRET_KEY=sk_XXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 3. Reiniciar o Backend
Execute:
```bash
sudo supervisorctl restart backend
```

---

## ✅ APÓS CONFIGURAR, O SISTEMA IRÁ:

1. ✓ Gerar PIX REAL via Furia Pay
2. ✓ Retornar QR Code válido
3. ✓ Código PIX copia e cola funcional
4. ✓ Verificação automática de pagamento
5. ✓ Webhook para confirmação instantânea

---

## 📊 DADOS JÁ CONFIGURADOS:

| Item | Valor | Status |
|------|-------|--------|
| **Chave Pública** | `pk_WBBsU+2XK5_X6dyNIaeG_ZB04NcmlIRXRTwvLYg96R7CPyL` | ✅ Configurada |
| **Chave Secreta** | `COLE_SUA_CHAVE_SECRETA_AQUI` | ⚠️ PENDENTE |
| **Endpoint API** | `https://api.furiapaybr.com/v1` | ✅ Configurado |
| **Webhook URL** | `/api/pix/webhook` | ✅ Implementado |

---

## 🧪 TESTAR APÓS CONFIGURAR:

1. Acesse: http://localhost:3000
2. Digite um CPF válido
3. Aguarde consulta no Yan Buscas
4. Clique em "REGULARIZAR AGORA"
5. Aguarde DARF
6. Clique em "GERAR DARF DE PAGAMENTO"
7. **Aguarde geração do PIX real do Furia Pay!**

---

## 🔍 VERIFICAR LOGS:

Para ver se está funcionando:
```bash
tail -f /var/log/supervisor/backend.out.log | grep -i "furia"
```

Você verá:
```
[FuriaPay] Criando transação PIX - Valor: R$ 149.42
[FuriaPay] ✓ Transação criada com sucesso - ID: xxxxx
[PixService] ✓ PIX gerado com sucesso - Transaction ID: xxxxx
```

---

## 📚 DOCUMENTAÇÃO FURIA PAY:

- Docs: https://app.furiapaybr.com/docs/intro/first-steps
- Criar Venda: https://app.furiapaybr.com/docs/sales/create-sale
- Dashboard: https://app.furiapaybr.com/integrations

---

## 🚨 EM CASO DE ERRO:

Se aparecer erro ao gerar PIX:
1. Verifique se a chave secreta está correta
2. Confirme que sua conta Furia Pay está ativa
3. Verifique os logs: `tail -n 50 /var/log/supervisor/backend.err.log`

---

## 💡 DICA IMPORTANTE:

A chave secreta é **sensível**! 
- ❌ Não compartilhe publicamente
- ❌ Não commite no Git
- ✅ Mantenha apenas no arquivo .env
- ✅ Use variável de ambiente em produção

---

**Sistema desenvolvido e pronto para produção!**
Falta apenas configurar a chave secreta do Furia Pay.
