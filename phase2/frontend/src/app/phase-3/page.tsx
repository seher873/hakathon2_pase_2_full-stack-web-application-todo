import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function PhasePage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <Card className="rounded-xl shadow-lg">
          <CardHeader className="bg-gradient-to-r from-purple-500 to-violet-600 text-white rounded-t-xl">
            <CardTitle className="text-2xl">Phase 3: AI System (Skills & Agents)</CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <div className="prose max-w-none">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">AI Orchestration Layer</h2>
              <p className="text-gray-600 mb-6">
                Phase 3 introduced the AI orchestration layer. Using SpecKit, AI skills and sub-agents were formally specified, planned, and implemented to safely interpret user intent, plan actions, execute tasks, and validate results.
              </p>

              <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Key Accomplishments:</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-2">
                <li>AI skills framework and specification system</li>
                <li>Natural language processing for task management</li>
                <li>Intent interpretation and action planning</li>
                <li>Skill execution and validation mechanisms</li>
                <li>Sub-agent orchestration system</li>
                <li>Safe AI interaction protocols</li>
              </ul>

              <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Technologies Used:</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-2">
                <li>SpecKit for AI skill specification</li>
                <li>Natural Language Processing (NLP) systems</li>
                <li>Intent classification algorithms</li>
                <li>AI orchestration frameworks</li>
                <li>Safety validation layers</li>
                <li>Agent communication protocols</li>
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