import React from 'react';
import { Card } from './ui/card';
import { Avatar, AvatarImage, AvatarFallback } from './ui/avatar';
import { Instagram, Youtube, Mail, Phone } from 'lucide-react';
import { authorInfo, categories, archives } from '../mock';

const Sidebar = () => {
  return (
    <aside className="space-y-6">
      {/* Blogger Badge */}
      <div className="flex justify-start">
        <img 
          src="https://www.gstatic.com/blogger/img/blogger_logo_round_35.png" 
          alt="Blogger"
          className="h-12"
        />
      </div>

      {/* Author Profile */}
      <Card className="p-6 bg-white">
        <div className="flex items-start space-x-4">
          <Avatar className="w-16 h-16">
            <AvatarImage src={authorInfo.avatar} alt={authorInfo.name} />
            <AvatarFallback>RG</AvatarFallback>
          </Avatar>
          <div className="flex-1">
            <h3 className="font-bold text-lg text-gray-900">{authorInfo.name}</h3>
            <p className="text-sm text-gray-600 mt-1">{authorInfo.location}</p>
            <p className="text-sm text-gray-700 mt-3 leading-relaxed">{authorInfo.bio}</p>
            <button className="text-sm text-blue-700 hover:underline mt-3">
              Visitar perfil
            </button>
          </div>
        </div>
      </Card>

      {/* Ad Section */}
      <Card className="p-6 bg-white text-center">
        <h3 className="font-bold text-lg mb-3">Mostre-se e anuncie no Top RG</h3>
        <p className="text-sm text-gray-700 mb-3">
          No Top RG, milhares de acessos ao dia!
        </p>
        <div className="text-sm text-gray-700 space-y-1">
          <div className="flex items-center justify-center space-x-2">
            <Phone className="w-4 h-4" />
            <span>(11) 97266 6802</span>
          </div>
          <div className="flex items-center justify-center space-x-2">
            <Mail className="w-4 h-4" />
            <span className="text-xs">toprg.imprensa@gmail.com</span>
          </div>
        </div>
      </Card>

      {/* Archive */}
      <Card className="p-6 bg-white">
        <h3 className="font-bold text-lg mb-4 text-gray-900">Arquivo</h3>
        <ul className="space-y-2">
          {archives.map((archive, index) => (
            <li key={index}>
              <button className="text-sm text-blue-700 hover:underline text-left">
                {archive}
              </button>
            </li>
          ))}
        </ul>
      </Card>

      {/* Categories */}
      <Card className="p-6 bg-white">
        <h3 className="font-bold text-lg mb-4 text-gray-900">Marcadores</h3>
        <div className="flex flex-wrap gap-2">
          {categories.map((category, index) => (
            <button
              key={index}
              className="text-sm bg-gray-100 hover:bg-gray-200 px-3 py-1 rounded-full text-gray-700 transition-colors"
            >
              {category}
            </button>
          ))}
        </div>
      </Card>

      {/* Social Media */}
      <Card className="p-6 bg-white">
        <h3 className="font-bold text-lg mb-4 text-gray-900">Instagram</h3>
        <button className="flex items-center space-x-2 text-pink-600 hover:text-pink-700">
          <Instagram className="w-8 h-8" />
          <span className="font-semibold">Seguir</span>
        </button>
      </Card>

      <Card className="p-6 bg-white">
        <h3 className="font-bold text-lg mb-4 text-gray-900">YouTube</h3>
        <button className="flex items-center space-x-2 text-red-600 hover:text-red-700">
          <Youtube className="w-8 h-8" />
          <span className="font-semibold">Inscrever-se</span>
        </button>
      </Card>

      {/* Partner Badges */}
      <Card className="p-6 bg-white text-center">
        <h3 className="font-bold text-lg mb-4 text-gray-900">Carretão Ipanema</h3>
        <div className="w-24 h-24 mx-auto rounded-full bg-gradient-to-br from-amber-900 to-amber-700 flex items-center justify-center">
          <span className="text-white font-bold text-sm">CARRETÃO</span>
        </div>
      </Card>

      <Card className="p-6 bg-white text-center">
        <h3 className="font-bold text-lg mb-4 text-gray-900">Porcão BH</h3>
        <div className="w-24 h-24 mx-auto rounded-full bg-gradient-to-br from-red-700 to-red-900 flex items-center justify-center">
          <span className="text-white font-bold text-sm">PORCÃO</span>
        </div>
      </Card>
    </aside>
  );
};

export default Sidebar;