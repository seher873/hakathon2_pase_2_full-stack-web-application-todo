'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { motion } from 'framer-motion';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            AI-Powered Todo App
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Choose from our dashboard options to get started
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <Card className="h-full flex flex-col rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-0 bg-gradient-to-br from-purple-500 to-indigo-600 text-white">
              <CardHeader>
                <CardTitle className="text-2xl">AI Todo Landing</CardTitle>
                <CardDescription className="text-purple-100">
                  Modern landing page for the AI-powered todo application
                </CardDescription>
              </CardHeader>
              <CardContent className="flex-grow">
                <p className="mb-6 text-purple-100">
                  Experience our natural language processing todo app with a beautiful gradient UI.
                </p>
                <Button asChild className="w-full bg-white text-purple-600 hover:bg-purple-50">
                  <Link href="/ai-todo">View Page</Link>
                </Button>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.2 }}
          >
            <Card className="h-full flex flex-col rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-0 bg-gradient-to-br from-indigo-500 to-blue-600 text-white">
              <CardHeader>
                <CardTitle className="text-2xl">Dashboard Phases</CardTitle>
                <CardDescription className="text-indigo-100">
                  Track progress through each phase of development
                </CardDescription>
              </CardHeader>
              <CardContent className="flex-grow">
                <p className="mb-6 text-indigo-100">
                  Visualize the 6 phases of the hackathon with points and descriptions.
                </p>
                <Button asChild variant="secondary" className="w-full bg-white text-indigo-600 hover:bg-indigo-50">
                  <Link href="/dashboard-phases">View Phases</Link>
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.3 }}
          className="mt-12 text-center"
        >
          <p className="text-gray-600 mb-4">
            Or navigate directly to your existing application:
          </p>
          <Button asChild variant="outline" className="border-gray-300 text-gray-700 hover:bg-gray-50">
            <Link href="/dashboard">Go to Existing Dashboard</Link>
          </Button>
        </motion.div>
      </div>
    </div>
  );
}