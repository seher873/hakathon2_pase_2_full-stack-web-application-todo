import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function PhasePage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <Card className="rounded-xl shadow-lg">
          <CardHeader className="bg-gradient-to-r from-pink-500 to-rose-600 text-white rounded-t-xl">
            <CardTitle className="text-2xl">Phase 6: Final Deployment</CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <div className="prose max-w-none">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Production Deployment</h2>
              <p className="text-gray-600 mb-6">
                Phase 6 focused on production deployment, monitoring setup, and final delivery of the complete system, ensuring all components are operational and performing optimally in the live environment.
              </p>

              <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Key Accomplishments:</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-2">
                <li>Production environment setup and configuration</li>
                <li>Monitoring and alerting system implementation</li>
                <li>Backup and disaster recovery procedures</li>
                <li>Performance tuning and optimization for production</li>
                <li>Security hardening and compliance verification</li>
                <li>Final system integration and go-live preparation</li>
              </ul>

              <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Technologies Used:</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-2">
                <li>Cloud deployment platforms and services</li>
                <li>Monitoring and observability tools</li>
                <li>Security scanning and hardening tools</li>
                <li>Performance optimization utilities</li>
                <li>Backup and recovery solutions</li>
                <li>Production deployment automation</li>
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