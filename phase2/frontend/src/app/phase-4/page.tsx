import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function PhasePage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <Card className="rounded-xl shadow-lg">
          <CardHeader className="bg-gradient-to-r from-indigo-500 to-blue-600 text-white rounded-t-xl">
            <CardTitle className="text-2xl">Phase 4: Build/Implement</CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <div className="prose max-w-none">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">System Implementation</h2>
              <p className="text-gray-600 mb-6">
                Phase 4 focused on implementing the planned system with emphasis on code quality, comprehensive testing, and seamless integration of all components.
              </p>

              <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Key Accomplishments:</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-2">
                <li>Full implementation of all planned features</li>
                <li>Comprehensive unit and integration testing</li>
                <li>Code quality improvements and refactoring</li>
                <li>Performance optimization</li>
                <li>Error handling and edge case management</li>
                <li>Security enhancements and validation</li>
              </ul>

              <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Technologies Used:</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-2">
                <li>Development frameworks and libraries</li>
                <li>Testing frameworks and tools</li>
                <li>Code quality and linting tools</li>
                <li>Performance monitoring solutions</li>
                <li>Security scanning and validation tools</li>
                <li>Continuous integration systems</li>
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