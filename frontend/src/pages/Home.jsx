import React from 'react';
import GovBrHeader from '../components/GovBrHeader';
import LoginCard from '../components/LoginCard';

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100 to-blue-50">
      <GovBrHeader />
      
      <main className="container mx-auto px-4 py-16">
        <LoginCard />
      </main>
    </div>
  );
};

export default Home;