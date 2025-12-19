import React from 'react';

const Header = () => {
  return (
    <header className="relative h-64 overflow-hidden">
      {/* Background Image with Blur */}
      <div 
        className="absolute inset-0 bg-cover bg-center"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&h=400&fit=crop)',
          filter: 'blur(3px)',
          transform: 'scale(1.1)'
        }}
      />
      
      {/* Overlay */}
      <div className="absolute inset-0 bg-black/20" />
      
      {/* Content */}
      <div className="relative z-10 container mx-auto px-4 h-full flex flex-col justify-center items-start">
        <div className="max-w-4xl">
          <h1 className="text-5xl md:text-6xl font-bold text-[#1e3a8a] mb-2 drop-shadow-lg">
            Top RG - toprg.blogspot.com
          </h1>
          <p className="text-2xl md:text-3xl italic text-[#1e3a8a] drop-shadow-md">
            Fundado em junho de 2005 - por Renato Galvão
          </p>
        </div>
        
        {/* Search Bar */}
        <div className="absolute top-4 right-4">
          <button className="text-sm text-gray-600 hover:text-gray-800 bg-white/80 px-4 py-2 rounded">
            Pesquisar este blog
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;