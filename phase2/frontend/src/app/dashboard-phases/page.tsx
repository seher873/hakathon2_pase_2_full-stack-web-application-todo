'use client';

import { Card, CardContent } from '@/components/ui/card';
import { CheckCircle, Code, Zap, Brain, Cloud, Trophy } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';
import Link from 'next/link';

// Define phase data
const phases = [
  {
    id: 1,
    title: "Foundation",
    description: "Setting up the project foundation, including repository structure, environment configuration, and core application logic. The goal was to establish a clean, scalable base for future phases.",
    points: 100,
    icon: CheckCircle,
    color: "bg-blue-100",
    iconColor: "text-blue-600"
  },
  {
    id: 2,
    title: "Application Development",
    description: "Deliver a complete working application with frontend and backend integration. This included user authentication, database operations, and deployment of both the frontend and backend as public services.",
    points: 200,
    icon: Code,
    color: "bg-green-100",
    iconColor: "text-green-600"
  },
  {
    id: 3,
    title: "AI System (Skills & Agents)",
    description: "Introduction of the AI orchestration layer. Using SpecKit, AI skills and sub-agents were formally specified, planned, and implemented to safely interpret user intent, plan actions, execute tasks, and validate results.",
    points: 300,
    icon: Brain,
    color: "bg-purple-100",
    iconColor: "text-purple-600"
  },
  {
    id: 4,
    title: "Build/Implement",
    description: "Implementation of the planned system with focus on code quality, testing, and integration.",
    points: 400,
    icon: Cloud,
    color: "bg-indigo-100",
    iconColor: "text-indigo-600"
  },
  {
    id: 5,
    title: "Validate & Polish",
    description: "Prove the system is correct, safe, and clear with extensive testing, validation, and polish.",
    points: 500,
    icon: Zap,
    color: "bg-yellow-100",
    iconColor: "text-yellow-600"
  },
  {
    id: 6,
    title: "Final Deployment",
    description: "Production deployment, monitoring setup, and final delivery of the complete system.",
    points: 600,
    icon: Trophy,
    color: "bg-pink-100",
    iconColor: "text-pink-600"
  }
];

export default function DashboardPhasesPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-indigo-50 to-violet-50 py-12 px-4 sm:px-6">
      <div className="max-w-6xl mx-auto">
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Hackathon Dashboard</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Track your progress through each phase of the AI-Powered Todo App development
          </p>
        </motion.div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {phases.map((phase, index) => {
            const IconComponent = phase.icon;
            return (
              <motion.div
                key={phase.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <Link href={`/phase-${phase.id}`}>
                  <Card className={`${phase.color} rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 hover:scale-[1.02] cursor-pointer border-0`}>
                    <CardContent className="p-6">
                      <div className="flex flex-col h-full">
                        <div className="flex justify-between items-start mb-4">
                          <div className={`p-3 rounded-lg ${phase.color} ${phase.iconColor}`}>
                            <IconComponent className="h-6 w-6" />
                          </div>
                          <span className="text-lg font-bold text-gray-700">{phase.points} Points</span>
                        </div>
                        
                        <h3 className="text-xl font-bold text-gray-900 mb-2">{phase.title}</h3>
                        
                        <p className="text-gray-600 mb-4 flex-grow">{phase.description}</p>
                        
                        <Button variant="outline" className="mt-auto w-full border-gray-300 text-gray-700 hover:bg-gray-50">
                          View Details
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
}