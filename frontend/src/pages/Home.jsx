import React from 'react';
import Header from '../components/Header';
import BlogCard from '../components/BlogCard';
import Sidebar from '../components/Sidebar';
import { blogPosts } from '../mock';

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 via-yellow-100 to-amber-100">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_350px] gap-8">
          {/* Blog Posts Grid */}
          <div>
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
              {blogPosts.map(post => (
                <BlogCard key={post.id} post={post} />
              ))}
            </div>
            
            {/* Pagination */}
            <div className="mt-8 flex justify-center">
              <button className="px-6 py-2 bg-white text-gray-700 rounded hover:bg-gray-50 transition-colors shadow-sm">
                Postagens mais antigas
              </button>
            </div>
          </div>
          
          {/* Sidebar */}
          <div>
            <Sidebar />
          </div>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="bg-gray-800 text-white py-6 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm">
            © 2025 Top RG - toprg.blogspot.com. Todos os direitos reservados.
          </p>
          <p className="text-xs text-gray-400 mt-2">
            Fundado em junho de 2005 - por Renato Galvão
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Home;