import React from 'react';
import { Download, FileText, Database, CheckCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import GovBrHeader from '../components/GovBrHeader';

const Dashboard = () => {
  const API_URL = process.env.REACT_APP_BACKEND_URL;

  const handleDownload = (endpoint, filename) => {
    window.open(`${API_URL}/api/download/${endpoint}`, '_blank');
  };

  const files = [
    {
      title: 'Mensagens WhatsApp (3.000) - PRONTO',
      description: '3.000 mensagens com link cpfregularize.online incluído',
      icon: FileText,
      endpoint: 'mensagens-3000',
      filename: 'mensagens_whatsapp_3000_PRONTO.xlsx',
      size: '3.000 registros',
      color: 'bg-blue-500',
      iconColor: 'text-blue-500'
    },
    {
      title: 'Mensagens WhatsApp (Completo)',
      description: '97.377 mensagens da base completa',
      icon: Database,
      endpoint: 'mensagens-completo',
      filename: 'mensagens_whatsapp_completo.xlsx',
      size: '97.377 registros',
      color: 'bg-green-500',
      iconColor: 'text-green-500'
    },
    {
      title: 'CPF + Telefone Consolidado',
      description: 'Lista consolidada de CPF e telefones',
      icon: CheckCircle,
      endpoint: 'cpf-telefone',
      filename: 'cpf_telefone_consolidado.txt',
      size: '3.427 registros',
      color: 'bg-purple-500',
      iconColor: 'text-purple-500'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100 to-blue-50">
      <GovBrHeader />

      <main className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-800 mb-4">
              Dashboard de Downloads
            </h1>
            <p className="text-gray-600">
              Baixe os arquivos de mensagens e dados consolidados
            </p>
          </div>

          {/* Info Card */}
          <Card className="mb-8 bg-blue-50 border-blue-200">
            <CardContent className="p-6">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                    <FileText className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-800 mb-2">
                    ℹ️ Informações Importantes
                  </h3>
                  <ul className="text-sm text-gray-700 space-y-1">
                    <li>📅 <strong>Data de Detecção:</strong> 31/12/2025 (Hoje)</li>
                    <li>🗓️ <strong>Prazo Final:</strong> 31/12/2025 (Hoje)</li>
                    <li>✅ <strong>Link incluído:</strong> https://cpfregularize.online</li>
                    <li>📱 Formato: Excel (.xlsx) - Pronto para disparar!</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Download Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {files.map((file, index) => {
              const Icon = file.icon;
              return (
                <Card key={index} className="hover:shadow-xl transition-shadow duration-300">
                  <CardHeader>
                    <div className="flex items-center justify-between mb-4">
                      <div className={`w-16 h-16 ${file.color} bg-opacity-10 rounded-lg flex items-center justify-center`}>
                        <Icon className={`w-8 h-8 ${file.iconColor}`} />
                      </div>
                    </div>
                    <CardTitle className="text-xl">{file.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 mb-4 text-sm">
                      {file.description}
                    </p>
                    <div className="mb-4">
                      <span className="inline-block bg-gray-100 text-gray-700 text-xs px-3 py-1 rounded-full">
                        {file.size}
                      </span>
                    </div>
                    <Button
                      onClick={() => handleDownload(file.endpoint, file.filename)}
                      className={`w-full ${file.color} hover:opacity-90 text-white`}
                    >
                      <Download className="w-4 h-4 mr-2" />
                      Baixar Arquivo
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* Instructions */}
          <Card className="mt-8 bg-yellow-50 border-yellow-200">
            <CardContent className="p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                ⚠️ Instruções de Uso
              </h3>
              <ol className="text-sm text-gray-700 space-y-2 ml-4">
                <li><strong>1.</strong> Baixe o arquivo desejado clicando no botão acima</li>
                <li><strong>2.</strong> Abra o arquivo CSV em um editor de texto ou Excel</li>
                <li><strong>3.</strong> Substitua <code className="bg-yellow-100 px-2 py-1 rounded">https://SEU_SITE_AQUI.com</code> pelo link real do seu site</li>
                <li><strong>4.</strong> Salve o arquivo modificado</li>
                <li><strong>5.</strong> Importe na sua ferramenta de disparo WhatsApp</li>
                <li><strong>6.</strong> Configure: coluna "telefone" + coluna "mensagem"</li>
              </ol>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
