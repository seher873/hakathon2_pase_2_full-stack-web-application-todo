import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function PhasePage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <Card className="rounded-xl shadow-lg">
          <CardHeader className="bg-gradient-to-r from-green-500 to-teal-600 text-white rounded-t-xl">
            <CardTitle className="text-2xl">Phase 2: Application Development</CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <div className="prose max-w-none">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Complete Working Application</h2>
              <p className="text-gray-600 mb-6">
                Phase 2 delivered a complete working application with frontend and backend integration. This included user authentication, database operations, and deployment of both the frontend and backend as public services.
              </p>

              <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Key Accomplishments:</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-2">
                <li>Full-stack application with React frontend and FastAPI backend</li>
                <li>User authentication and authorization system</li>
                <li>Database integration with SQLAlchemy ORM</li>
                <li>Complete task management CRUD operations</li>
                <li>Responsive UI design with Tailwind CSS</li>
                <li>API documentation and testing</li>
              </ul>

              <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Technologies Used:</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-2">
                <li>Next.js 14 with App Router for frontend</li>
                <li>FastAPI for backend API</li>
                <li>TypeScript for type safety</li>
                <li>SQLAlchemy with SQLModel for database operations</li>
                <li>Tailwind CSS for styling</li>
                <li>JWT-based authentication</li>
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