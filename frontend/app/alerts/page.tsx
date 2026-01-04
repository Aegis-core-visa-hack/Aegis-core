"use client";

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Header } from "@/components/layout/Header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { alertsApi, Alert } from "@/lib/api";
import { mockAlerts } from "@/lib/mockData";
import { cn } from "@/lib/utils";

export default function AlertsPage() {
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [loading, setLoading] = useState(true);
    const [useApi, setUseApi] = useState(true);
    const [severityFilter, setSeverityFilter] = useState<string>('');
    const [statusFilter, setStatusFilter] = useState<string>('');

    useEffect(() => {
        async function fetchAlerts() {
            try {
                const res = await alertsApi.list(severityFilter || undefined, statusFilter || undefined);
                setAlerts(res.data);
                setUseApi(true);
            } catch (error) {
                console.error("API unavailable, using mock data:", error);
                setAlerts(mockAlerts);
                setUseApi(false);
            } finally {
                setLoading(false);
            }
        }
        fetchAlerts();
    }, [severityFilter, statusFilter]);

    const severityStyles = {
        critical: 'bg-red-500/20 text-red-400 border-red-500/50',
        high: 'bg-orange-500/20 text-orange-400 border-orange-500/50',
        medium: 'bg-amber-500/20 text-amber-400 border-amber-500/50',
        low: 'bg-blue-500/20 text-blue-400 border-blue-500/50',
    };

    const statusStyles = {
        open: 'bg-red-500/20 text-red-400',
        investigating: 'bg-amber-500/20 text-amber-400',
        resolved: 'bg-green-500/20 text-green-400',
    };

    const formatTime = (timestamp: string) => {
        return new Date(timestamp).toLocaleString();
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-background">
                <Header />
                <main className="container max-w-screen-2xl px-4 py-8">
                    <div className="flex items-center justify-center h-[60vh]">
                        <div className="flex flex-col items-center gap-4">
                            <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin" />
                            <p className="text-muted-foreground">Loading alerts...</p>
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
                <div className="mb-8 flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">Alerts</h1>
                        <p className="text-muted-foreground">
                            {alerts.length} total alerts • {alerts.filter(a => a.status === 'open').length} open
                            {!useApi && <span className="ml-2 text-yellow-500">(Demo Mode)</span>}
                        </p>
                    </div>
                    <div className="flex items-center gap-2">
                        <select
                            value={severityFilter}
                            onChange={(e) => setSeverityFilter(e.target.value)}
                            className="px-3 py-2 text-sm rounded-md border border-border bg-background"
                        >
                            <option value="">All Severities</option>
                            <option value="critical">Critical</option>
                            <option value="high">High</option>
                            <option value="medium">Medium</option>
                            <option value="low">Low</option>
                        </select>
                        <select
                            value={statusFilter}
                            onChange={(e) => setStatusFilter(e.target.value)}
                            className="px-3 py-2 text-sm rounded-md border border-border bg-background"
                        >
                            <option value="">All Statuses</option>
                            <option value="open">Open</option>
                            <option value="investigating">Investigating</option>
                            <option value="resolved">Resolved</option>
                        </select>
                        <Button variant="outline">Export</Button>
                    </div>
                </div>

                <div className="rounded-xl border border-border/50 bg-card">
                    <div className="divide-y divide-border/50">
                        {alerts.map((alert) => (
                            <Link
                                key={alert.id}
                                href={`/alerts/${alert.id}`}
                                className="flex items-start gap-4 p-4 transition-colors hover:bg-muted/50"
                            >
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <Badge
                                            variant="outline"
                                            className={cn("text-xs uppercase", severityStyles[alert.severity])}
                                        >
                                            {alert.severity}
                                        </Badge>
                                        <Badge
                                            variant="outline"
                                            className={cn("text-xs capitalize", statusStyles[alert.status as keyof typeof statusStyles] || '')}
                                        >
                                            {alert.status}
                                        </Badge>
                                        <span className="text-sm text-muted-foreground">{alert.id}</span>
                                    </div>
                                    <h3 className="font-semibold">{alert.title}</h3>
                                    <p className="text-sm text-muted-foreground">{alert.description}</p>
                                </div>
                                <div className="text-right text-sm">
                                    <p className="text-muted-foreground">{formatTime(alert.timestamp)}</p>
                                    {alert.regulation && (
                                        <p className="text-xs text-primary">{alert.regulation}</p>
                                    )}
                                </div>
                            </Link>
                        ))}
                        {alerts.length === 0 && (
                            <div className="p-8 text-center text-muted-foreground">
                                No alerts found matching your filters.
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}
