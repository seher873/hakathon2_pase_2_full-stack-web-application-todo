import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function PhasePage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <Card className="rounded-xl shadow-lg">
          <CardHeader className="bg-gradient-to-r from-yellow-500 to-orange-600 text-white rounded-t-xl">
            <CardTitle className="text-2xl">Phase 5: Validate & Polish</CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <div className="prose max-w-none">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">System Validation & Polish</h2>
              <p className="text-gray-600 mb-6">
                Phase 5 focused on proving the system is correct, safe, and clear with extensive testing, validation, and refinement of all aspects of the application.
              </p>

              <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Key Accomplishments:</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-2">
                <li>Extensive testing and validation across all components</li>
                <li>Security audit and vulnerability assessment</li>
                <li>Performance benchmarking and optimization</li>
                <li>User experience refinement and accessibility improvements</li>
                <li>Documentation completion and user guides</li>
                <li>Final system integration and deployment validation</li>
              </ul>

              <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Technologies Used:</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-2">
                <li>Testing and validation frameworks</li>
                <li>Security scanning and penetration tools</li>
                <li>Performance monitoring and profiling tools</li>
                <li>Accessibility testing utilities</li>
                <li>Documentation generators</li>
                <li>Quality assurance and CI/CD pipelines</li>
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