import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, AlertTriangle, Download, Printer } from 'lucide-react';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import GovBrHeader from '../components/GovBrHeader';
import { darfService } from '../services/api';

const Darf = () => {
  const navigate = useNavigate();
  const [darfData, setDarfData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDarf = async () => {
      try {
        const userData = JSON.parse(localStorage.getItem('userData'));
        if (!userData) {
          navigate('/');
          return;
        }

        const result = await darfService.obter(userData.protocol);
        if (result.success) {
          // Mescla dados da API com dados do usuário
          setDarfData({
            ...result.data,
            contribuinte: userData.name,
            cpf: userData.cpf
          });
        }
      } catch (error) {
        console.error('Erro ao buscar DARF:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDarf();
  }, [navigate]);

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const handleGerarDarf = () => {
    navigate('/loading-pix');
  };

  if (loading || !darfData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100 to-blue-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100 to-blue-50">
      <GovBrHeader />

      {/* Banner Azul */}
      <div className="bg-blue-600 text-white py-4 px-4 text-center font-bold text-lg flex items-center justify-center space-x-2">
        <FileText className="w-6 h-6" />
        <span>DARF - Documento de Arrecadação de Receitas Federais</span>
      </div>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Card Principal do DARF */}
        <Card className="shadow-xl bg-white mb-6">
          <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 rounded-t-lg">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-2xl font-bold mb-1">DARF</h2>
                <p className="text-blue-100 text-sm">Documento de Arrecadação de Receitas Federais</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-blue-100">Protocolo</p>
                <p className="text-xl font-bold">{darfData.protocolo}</p>
              </div>
            </div>
          </div>

          <div className="p-6">
            {/* Informações do Contribuinte */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <p className="text-sm text-gray-600 mb-1">Nome do Contribuinte</p>
                <p className="text-lg font-semibold text-gray-800">{darfData.contribuinte}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Período de Apuração</p>
                <p className="text-lg font-semibold text-gray-800">{darfData.periodoApuracao}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">CPF/CNPJ</p>
                <p className="text-lg font-semibold text-gray-800">{darfData.cpf}</p>
              </div>
              <div className="bg-red-50 p-3 rounded-lg border border-red-200">
                <p className="text-sm text-red-600 mb-1">Data de Vencimento</p>
                <p className="text-lg font-bold text-red-600">{darfData.dataVencimento}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Código da Receita</p>
                <p className="text-lg font-semibold text-gray-800">{darfData.codigoReceita}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Número de Referência</p>
                <p className="text-lg font-semibold text-gray-800">{darfData.numeroReferencia}</p>
              </div>
            </div>

            {/* Discriminação dos Valores */}
            <div className="border-t pt-6">
              <div className="flex items-center space-x-2 mb-4">
                <FileText className="w-5 h-5 text-blue-600" />
                <h3 className="text-lg font-bold text-gray-800">Discriminação dos Valores</h3>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between items-center py-3 border-b">
                  <span className="text-gray-700">Valor Principal</span>
                  <span className="text-lg font-semibold text-gray-800">{formatCurrency(darfData.valorPrincipal)}</span>
                </div>
                <div className="flex justify-between items-center py-3 border-b bg-red-50 px-3 rounded">
                  <span className="text-red-700 font-medium">Multa</span>
                  <span className="text-lg font-bold text-red-600">{formatCurrency(darfData.multa)}</span>
                </div>
                <div className="flex justify-between items-center py-3 border-b bg-red-50 px-3 rounded">
                  <span className="text-red-700 font-medium">Juros</span>
                  <span className="text-lg font-bold text-red-600">{formatCurrency(darfData.juros)}</span>
                </div>
                <div className="flex justify-between items-center py-4 bg-green-50 px-4 rounded-lg border-2 border-green-300">
                  <span className="text-xl font-bold text-gray-800">VALOR A PAGAR</span>
                  <span className="text-2xl font-bold text-blue-700">{formatCurrency(darfData.valorTotal)}</span>
                </div>
              </div>
            </div>

            {/* Aviso de Acréscimo */}
            <div className="mt-6 bg-yellow-50 border border-yellow-300 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <AlertTriangle className="w-6 h-6 text-yellow-600 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-bold text-yellow-900 mb-2">
                    Atenção: O não pagamento até a data de vencimento resultará em:
                  </p>
                  <ul className="space-y-1 text-sm text-yellow-800">
                    <li>• Acréscimo de multa de <span className="font-bold">20%</span> sobre o valor total</li>
                    <li>• Juros de mora calculados com base na taxa SELIC</li>
                    <li>• Inscrição em Dívida Ativa da União</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Código de Autenticação */}
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600 mb-2">Documento gerado eletronicamente</p>
              <div className="inline-flex items-center space-x-2 bg-gray-100 px-4 py-2 rounded">
                <FileText className="w-4 h-4 text-gray-600" />
                <span className="text-xs font-mono text-gray-700">Código de Autenticação: XZn4QCWvuI</span>
              </div>
            </div>
          </div>
        </Card>

        {/* Botões de Ação */}
        <div className="grid grid-cols-1 gap-4">
          <Button
            onClick={handleGerarDarf}
            className="w-full h-16 text-xl font-bold rounded-xl shadow-lg bg-gradient-to-r from-green-600 via-green-500 to-blue-500 hover:from-green-700 hover:via-green-600 hover:to-blue-600 text-white transition-all duration-300 transform hover:scale-105"
          >
            <FileText className="w-6 h-6 mr-3" />
            GERAR DARF DE PAGAMENTO
          </Button>

          <div className="grid grid-cols-2 gap-4">
            <Button
              variant="outline"
              className="h-12 border-2 border-blue-600 text-blue-600 hover:bg-blue-50 font-semibold"
            >
              <Download className="w-5 h-5 mr-2" />
              Baixar PDF
            </Button>
            <Button
              variant="outline"
              className="h-12 border-2 border-blue-600 text-blue-600 hover:bg-blue-50 font-semibold"
            >
              <Printer className="w-5 h-5 mr-2" />
              Imprimir
            </Button>
          </div>
        </div>

        <p className="text-center text-sm text-gray-600 mt-6">
          Mantenha este documento para seus registros. Ele pode ser usado para pagamento em qualquer agência bancária ou internet banking.
        </p>
      </main>
    </div>
  );
};

export default Darf;