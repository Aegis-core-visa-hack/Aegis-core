import { Header } from "@/components/layout/Header";
import { MetricCard } from "@/components/dashboard/MetricCard";
import { RiskHeatmap } from "@/components/dashboard/RiskHeatmap";
import { AlertList } from "@/components/dashboard/AlertList";
import { AgentStatus } from "@/components/dashboard/AgentStatus";
import { mockDashboard, mockAlerts, mockRiskHeatmap } from "@/lib/mockData";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container max-w-screen-2xl px-4 py-8">
        {/* Page Title */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight">Command Center</h1>
          <p className="text-muted-foreground">
            Real-time compliance monitoring across your ecosystem
          </p>
        </div>

        {/* Metric Cards */}
        <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            title="Compliance Score"
            value={`${mockDashboard.compliance_score}%`}
            change={mockDashboard.score_change}
            changeLabel="%"
            trend={mockDashboard.score_change > 0 ? "up" : "down"}
          />
          <MetricCard
            title="Open Violations"
            value={mockDashboard.open_violations}
            change={-5}
            trend="down"
          />
          <MetricCard
            title="Critical Alerts"
            value={mockDashboard.critical_alerts}
            trend="neutral"
          />
          <MetricCard
            title="Agents Online"
            value={`${mockDashboard.agents.filter(a => a.status === 'online').length}/${mockDashboard.agents.length}`}
            trend="neutral"
          />
        </div>

        {/* Risk Heatmap */}
        <div className="mb-8">
          <RiskHeatmap data={mockRiskHeatmap} />
        </div>

        {/* Two Column Layout: Alerts + Agent Status */}
        <div className="grid gap-6 lg:grid-cols-2">
          <AlertList alerts={mockAlerts.slice(0, 5)} />
          <AgentStatus agents={mockDashboard.agents} />
        </div>
      </main>
    </div>
  );
}
