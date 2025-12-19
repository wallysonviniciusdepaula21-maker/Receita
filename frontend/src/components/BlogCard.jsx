import React from 'react';
import { Card } from './ui/card';

const BlogCard = ({ post }) => {
  return (
    <Card className="overflow-hidden hover:shadow-lg transition-all duration-300 hover:-translate-y-1 cursor-pointer bg-white">
      {/* Image */}
      <div className="relative h-48 overflow-hidden">
        <img 
          src={post.image} 
          alt={post.title}
          className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
        />
      </div>
      
      {/* Content */}
      <div className="p-5">
        <h3 className="text-lg font-semibold text-gray-800 mb-2 line-clamp-2 hover:text-blue-900 transition-colors">
          {post.title}
        </h3>
        <p className="text-sm italic text-gray-500">
          {post.date}
        </p>
      </div>
    </Card>
  );
};

export default BlogCard;