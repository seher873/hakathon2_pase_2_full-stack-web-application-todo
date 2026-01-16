import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function PhasePage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <Card className="rounded-xl shadow-lg">
          <CardHeader className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-t-xl">
            <CardTitle className="text-2xl">Phase 1: Foundation</CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <div className="prose max-w-none">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Project Foundation & Setup</h2>
              <p className="text-gray-600 mb-6">
                Phase 1 focused on setting up the project foundation, including repository structure, environment configuration, and core application logic. The goal was to establish a clean, scalable base for future phases.
              </p>

              <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Key Accomplishments:</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-2">
                <li>Established project repository structure</li>
                <li>Configured development environments</li>
                <li>Defined core application architecture</li>
                <li>Created foundational components and utilities</li>
                <li>Implemented basic project scaffolding</li>
              </ul>

              <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Technologies Used:</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-2">
                <li>Repository structure and organization</li>
                <li>Environment configuration tools</li>
                <li>Basic project setup utilities</li>
                <li>Foundational libraries and frameworks</li>
              </ul>

              <div className="flex gap-4 mt-8">
                <Button asChild>
                  <Link href="/dashboard-phases">Back to Dashboard</Link>
                </Button>
                <Button variant="outline" asChild>
                  <Link href="/">Home</Link>
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}