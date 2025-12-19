import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Check, Loader2, CreditCard, Building, FileText } from 'lucide-react';
import { Card, CardContent } from '../components/ui/card';
import GovBrHeader from '../components/GovBrHeader';

const LoadingPagamento = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);

  useEffect(() => {
    // Progressão dos steps
    const timers = [
      setTimeout(() => setStep(1), 1500),
      setTimeout(() => setStep(2), 3000),
      setTimeout(() => setStep(3), 4500),
      setTimeout(() => navigate('/darf'), 6000)
    ];

    return () => timers.forEach(timer => clearTimeout(timer));
  }, [navigate]);

  const progressSteps = [
    {
      icon: CreditCard,
      title: 'Validando Pagamento',
      subtitle: 'Verificando informações do DARF',
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      progressColor: 'bg-green-500',
      completed: step >= 1
    },
    {
      icon: Building,
      title: 'Conectando com Banco',
      subtitle: 'Estabelecendo conexão segura',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      progressColor: 'bg-blue-500',
      completed: step >= 2
    },
    {
      icon: FileText,
      title: 'Gerando Guia de Pagamento',
      subtitle: 'Preparando forma de pagamento',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      progressColor: 'bg-purple-500',
      completed: step >= 3
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100 to-blue-50">
      <GovBrHeader />

      <main className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          {/* Título Principal */}
          <div className="text-center mb-8">
            <Loader2 className="w-16 h-16 text-blue-600 animate-spin mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-gray-800 mb-2">
              Carregando informações de pagamento...
            </h1>
            <p className="text-gray-600">Verificando dados bancários...</p>
            <p className="text-sm text-gray-500 mt-1">Processando DARF...</p>
          </div>

          {/* Badges de Status no Topo */}
          <div className="flex justify-center space-x-4 mb-8">
            <div className={`px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 ${
              step >= 1 ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-400'
            }`}>
              <Check className="inline w-4 h-4 mr-1" />
              Seguro
            </div>
            <div className={`px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 ${
              step >= 2 ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-400'
            }`}>
              <Check className="inline w-4 h-4 mr-1" />
              Criptografado
            </div>
            <div className={`px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 ${
              step >= 3 ? 'bg-purple-100 text-purple-700' : 'bg-gray-100 text-gray-400'
            }`}>
              <Check className="inline w-4 h-4 mr-1" />
              Verificado
            </div>
          </div>

          {/* Barra de Progresso Geral */}
          <div className="mb-10">
            <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-green-500 via-blue-500 to-purple-500 transition-all duration-1000 ease-out"
                style={{ width: `${(step / 3) * 100}%` }}
              />
            </div>
          </div>

          {/* Cards de Progresso */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {progressSteps.map((item, index) => {
              const Icon = item.icon;
              const isActive = step === index + 1;
              const isCompleted = item.completed;

              return (
                <Card
                  key={index}
                  className={`transition-all duration-500 transform ${
                    isActive ? 'scale-105 shadow-xl' : 'scale-100 shadow-lg'
                  } ${isCompleted ? item.bgColor : 'bg-white'}`}
                >
                  <CardContent className="p-6 text-center">
                    {/* Ícone */}
                    <div className={`w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center transition-all duration-500 ${
                      isCompleted ? item.bgColor : 'bg-gray-100'
                    }`}>
                      <Icon className={`w-10 h-10 transition-all duration-500 ${
                        isCompleted ? item.color : 'text-gray-400'
                      } ${isActive ? 'animate-pulse' : ''}`} />
                    </div>

                    {/* Título */}
                    <h3 className={`text-lg font-bold mb-2 transition-colors duration-500 ${
                      isCompleted ? 'text-gray-800' : 'text-gray-400'
                    }`}>
                      {item.title}
                    </h3>

                    {/* Subtítulo */}
                    <p className={`text-sm transition-colors duration-500 ${
                      isCompleted ? 'text-gray-600' : 'text-gray-400'
                    }`}>
                      {item.subtitle}
                    </p>

                    {/* Barra de Progresso Individual */}
                    <div className="mt-4 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        className={`h-full transition-all duration-1000 ease-out ${
                          isCompleted ? item.progressColor : 'bg-gray-300'
                        }`}
                        style={{ width: isCompleted ? '100%' : '0%' }}
                      />
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* Mensagem de Segurança */}
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-600">
              Suas informações estão sendo processadas com segurança
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default LoadingPagamento;