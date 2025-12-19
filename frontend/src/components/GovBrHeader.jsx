import React from 'react';
import { Bell, User } from 'lucide-react';

const GovBrHeader = () => {
  return (
    <header className="bg-white shadow-sm py-4 px-6">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Logo e Título */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center">
            <span className="text-2xl font-bold text-blue-600">g</span>
            <span className="text-2xl font-bold text-orange-500">o</span>
            <span className="text-2xl font-bold text-blue-600">v</span>
            <span className="text-2xl font-bold text-green-500">.</span>
            <span className="text-2xl font-bold text-blue-600">b</span>
            <span className="text-2xl font-bold text-orange-500">r</span>
          </div>
          <div className="ml-4">
            <h1 className="text-lg font-semibold text-gray-800">Meu Imposto de Renda</h1>
            <p className="text-sm text-gray-600">Receita Federal</p>
          </div>
        </div>

        {/* Sistema gov.br */}
        <div className="flex items-center space-x-4">
          <button className="relative p-2 hover:bg-gray-100 rounded-full transition-colors">
            <Bell className="w-5 h-5 text-gray-600" />
          </button>
          <div className="flex items-center space-x-2">
            <div className="text-right">
              <p className="text-sm text-gray-600">Sistema</p>
              <p className="text-sm font-semibold text-gray-800">gov.br</p>
            </div>
            <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
              <User className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default GovBrHeader;