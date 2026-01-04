"use client";

import { useEffect, useState } from "react";
import { Header } from "@/components/layout/Header";
import { MetricCard } from "@/components/dashboard/MetricCard";
import { RiskHeatmap } from "@/components/dashboard/RiskHeatmap";
import { AlertList } from "@/components/dashboard/AlertList";
import { AgentStatus } from "@/components/dashboard/AgentStatus";
import { dashboardApi, Alert, Agent, RiskHeatmapItem, DashboardSummary } from "@/lib/api";
import { mockDashboard, mockAlerts, mockRiskHeatmap } from "@/lib/mockData";

export default function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [heatmap, setHeatmap] = useState<RiskHeatmapItem[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [useApi, setUseApi] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [summaryRes, alertsRes, heatmapRes, agentsRes] = await Promise.all([
          dashboardApi.getSummary(),
          dashboardApi.getRecentAlerts(5),
          dashboardApi.getRiskHeatmap(),
          dashboardApi.getAgentActivity(),
        ]);

        setSummary(summaryRes.data);
        setAlerts(alertsRes.data.alerts);
        setHeatmap(heatmapRes.data.regulations);
        setAgents(agentsRes.data.agents);
        setUseApi(true);
      } catch (error) {
        console.error("API unavailable, using mock data:", error);
        setUseApi(false);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  // Use API data or fall back to mock data
  const displaySummary = summary || {
    compliance_score: { value: mockDashboard.compliance_score, change: mockDashboard.score_change, trend: "up" as const },
    at_risk_entities: { value: 12, change: -2, trend: "down" as const },
    violations_24h: { value: mockDashboard.open_violations, change: 8, trend: "up" as const },
    agents_online: mockDashboard.agents.filter(a => a.status === "online").length,
    agents_total: mockDashboard.agents.length,
  };

  const displayAlerts = useApi ? alerts : mockAlerts.slice(0, 5);
  const displayHeatmap = useApi ? heatmap : mockRiskHeatmap.map(h => ({ ...h, score: 0, open_violations: h.violation_count, jurisdiction: "Global" }));
  const displayAgents = useApi ? agents : mockDashboard.agents.map(a => ({
    ...a,
    display_name: a.name,
    description: "",
    status: a.status as Agent["status"]
  }));

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <main className="container max-w-screen-2xl px-4 py-8">
          <div className="flex items-center justify-center h-[60vh]">
            <div className="flex flex-col items-center gap-4">
              <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin" />
              <p className="text-muted-foreground">Loading dashboard...</p>
            </div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container max-w-screen-2xl px-4 py-8">
        {/* Page Title */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Command Center</h1>
            <p className="text-muted-foreground">
              Real-time compliance monitoring across your ecosystem
            </p>
          </div>
          {!useApi && (
            <span className="text-xs px-2 py-1 bg-yellow-500/10 text-yellow-500 rounded-md">
              Demo Mode (API offline)
            </span>
          )}
        </div>

        {/* Metric Cards */}
        <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            title="Compliance Score"
            value={`${displaySummary.compliance_score.value}%`}
            change={displaySummary.compliance_score.change}
            changeLabel="%"
            trend={displaySummary.compliance_score.trend}
          />
          <MetricCard
            title="At-Risk Entities"
            value={displaySummary.at_risk_entities.value}
            change={displaySummary.at_risk_entities.change}
            trend={displaySummary.at_risk_entities.trend}
          />
          <MetricCard
            title="Violations (24h)"
            value={displaySummary.violations_24h.value}
            change={displaySummary.violations_24h.change}
            trend={displaySummary.violations_24h.trend}
          />
          <MetricCard
            title="Agents Online"
            value={`${displaySummary.agents_online}/${displaySummary.agents_total}`}
            trend="neutral"
          />
        </div>

        {/* Risk Heatmap */}
        <div className="mb-8">
          <RiskHeatmap data={displayHeatmap} />
        </div>

        {/* Two Column Layout: Alerts + Agent Status */}
        <div className="grid gap-6 lg:grid-cols-2">
          <AlertList alerts={displayAlerts} />
          <AgentStatus agents={displayAgents} />
        </div>
      </main>
    </div>
  );
}
