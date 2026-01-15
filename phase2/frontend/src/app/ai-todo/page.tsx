'use client';

import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { motion } from 'framer-motion';
import Link from 'next/link';

export default function AITodoLandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-600 via-purple-700 to-purple-800 flex flex-col">
      {/* Hero Section */}
      <div className="flex-grow flex items-center justify-center p-4">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="w-full max-w-2xl mx-auto text-center"
        >
          {/* Badge */}
          <Badge variant="secondary" className="mb-6 bg-purple-500/20 text-purple-100 backdrop-blur-sm">
            Hackathon Phase 5 - Cloud Deployed
          </Badge>
          
          {/* Headline */}
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-4xl md:text-6xl font-bold text-white mb-4"
          >
            AI-Powered Todo App
          </motion.h1>
          
          {/* Subtext */}
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-lg md:text-xl text-purple-200 mb-8 max-w-2xl mx-auto"
          >
            Manage tasks with natural language. Say 'kal ka kaam add karo' or 'pending tasks dikhao'
          </motion.p>
          
          {/* Buttons */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="flex flex-col sm:flex-row justify-center gap-4 mb-12"
          >
            <Button 
              size="lg" 
              className="rounded-lg shadow-lg hover:scale-105 transition-transform duration-300 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700"
            >
              <Link href="/signup">Get Started</Link>
            </Button>
            <Button 
              variant="outline" 
              size="lg" 
              className="rounded-lg shadow-lg hover:scale-105 transition-transform duration-300 border-purple-300 text-white hover:bg-purple-300/20"
            >
              <Link href="/signup">Create Account</Link>
            </Button>
          </motion.div>
          
          {/* AI Command Input */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="max-w-xl mx-auto"
          >
            <div className="relative">
              <Input
                type="text"
                placeholder="Type your task here..."
                className="w-full py-6 pl-6 pr-20 rounded-xl bg-white/10 backdrop-blur-sm border border-purple-300/30 text-white placeholder:text-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent"
              />
              <Button 
                size="sm" 
                variant="secondary" 
                className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-purple-500 hover:bg-purple-600 text-white"
              >
                Send
              </Button>
            </div>
          </motion.div>
        </motion.div>
      </div>
      
      {/* Footer */}
      <footer className="py-6 text-center text-purple-200/70 text-sm">
        <div className="container mx-auto">
          <p>© {new Date().getFullYear()} AI-Powered Todo App. All rights reserved.</p>
          <div className="mt-2 flex justify-center space-x-6">
            <Link href="#" className="hover:text-white transition-colors">About</Link>
            <Link href="#" className="hover:text-white transition-colors">Contact</Link>
            <Link href="#" className="hover:text-white transition-colors">Privacy</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}