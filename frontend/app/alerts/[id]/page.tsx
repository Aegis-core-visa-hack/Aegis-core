"use client";

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { Header } from "@/components/layout/Header";
import { Badge } from "@/components/ui/badge";
import { AlertActions } from "@/components/alerts/AlertActions";
import { alertsApi, AlertDetail as AlertDetailType } from "@/lib/api";
import { mockAlertDetail, mockAlerts } from "@/lib/mockData";
import { cn } from "@/lib/utils";

const severityStyles = {
    critical: 'bg-red-500/20 text-red-400 border-red-500/50',
    high: 'bg-orange-500/20 text-orange-400 border-orange-500/50',
    medium: 'bg-amber-500/20 text-amber-400 border-amber-500/50',
    low: 'bg-blue-500/20 text-blue-400 border-blue-500/50',
};

export default function AlertDetailPage() {
    const params = useParams();
    const id = params.id as string;

    const [detail, setDetail] = useState<AlertDetailType | null>(null);
    const [loading, setLoading] = useState(true);
    const [useApi, setUseApi] = useState(true);
    const [notFound, setNotFound] = useState(false);

    useEffect(() => {
        async function fetchAlertDetail() {
            try {
                const res = await alertsApi.getDetail(id);
                setDetail(res.data);
                setUseApi(true);
            } catch (error) {
                console.error("API unavailable, using mock data:", error);
                // Fall back to mock data
                const mockAlert = id === 'ALT-002' ? mockAlertDetail : mockAlerts.find(a => a.id === id);
                if (!mockAlert) {
                    setNotFound(true);
                } else {
                    const fallbackDetail: AlertDetailType = id === 'ALT-002'
                        ? mockAlertDetail as AlertDetailType
                        : {
                            ...mockAlert,
                            evidence: `Alert ${id} triggered at ${mockAlert.timestamp}`,
                            recommendations: [
                                "Review the alert details",
                                "Investigate the root cause",
                                "Take appropriate action"
                            ],
                            context: {
                                similar_violations: 1,
                                entity_name: mockAlert.entity_id || 'Unknown',
                                entity_volume: 'N/A'
                            }
                        } as AlertDetailType;
                    setDetail(fallbackDetail);
                }
                setUseApi(false);
            } finally {
                setLoading(false);
            }
        }
        fetchAlertDetail();
    }, [id]);

    if (loading) {
        return (
            <div className="min-h-screen bg-background">
                <Header />
                <main className="container max-w-screen-2xl px-4 py-8">
                    <div className="flex items-center justify-center h-[60vh]">
                        <div className="flex flex-col items-center gap-4">
                            <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin" />
                            <p className="text-muted-foreground">Loading alert details...</p>
                        </div>
                    </div>
                </main>
            </div>
        );
    }

    if (notFound || !detail) {
        return (
            <div className="min-h-screen bg-background">
                <Header />
                <main className="container max-w-screen-2xl px-4 py-8">
                    <Link
                        href="/alerts"
                        className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-6"
                    >
                        ← Back to Alerts
                    </Link>
                    <div className="text-center py-16">
                        <h1 className="text-2xl font-bold mb-2">Alert Not Found</h1>
                        <p className="text-muted-foreground">The alert {id} could not be found.</p>
                    </div>
                </main>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background">
            <Header />
            <main className="container max-w-screen-2xl px-4 py-8">
                {/* Back link */}
                <div className="flex items-center justify-between mb-6">
                    <Link
                        href="/alerts"
                        className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground"
                    >
                        ← Back to Alerts
                    </Link>
                    {!useApi && (
                        <span className="text-xs px-2 py-1 bg-yellow-500/10 text-yellow-500 rounded-md">
                            Demo Mode
                        </span>
                    )}
                </div>

                {/* Alert header */}
                <div className="mb-8">
                    <div className="flex items-center gap-3 mb-2">
                        <Badge
                            variant="outline"
                            className={cn("text-xs uppercase", severityStyles[detail.severity])}
                        >
                            {detail.severity}
                        </Badge>
                        <span className="text-sm text-muted-foreground">{detail.id}</span>
                    </div>
                    <h1 className="text-2xl font-bold tracking-tight">{detail.title}</h1>
                    <p className="text-muted-foreground mt-1">{detail.description}</p>
                </div>

                <div className="grid gap-6 lg:grid-cols-3">
                    {/* Main content - 2 cols */}
                    <div className="lg:col-span-2 space-y-6">
                        {/* Details */}
                        <div className="rounded-xl border border-border/50 bg-card p-6">
                            <h2 className="text-lg font-semibold mb-4">Details</h2>
                            <dl className="grid grid-cols-2 gap-4">
                                <div>
                                    <dt className="text-sm text-muted-foreground">Regulation</dt>
                                    <dd className="font-medium">{detail.regulation || 'N/A'}</dd>
                                </div>
                                <div>
                                    <dt className="text-sm text-muted-foreground">Detected</dt>
                                    <dd className="font-medium">{new Date(detail.timestamp).toLocaleString()}</dd>
                                </div>
                                <div>
                                    <dt className="text-sm text-muted-foreground">Entity</dt>
                                    <dd className="font-medium">{detail.context?.entity_name || detail.entity_id || 'N/A'}</dd>
                                </div>
                                <div>
                                    <dt className="text-sm text-muted-foreground">Status</dt>
                                    <dd className="font-medium capitalize">{detail.status}</dd>
                                </div>
                            </dl>
                        </div>

                        {/* Evidence */}
                        <div className="rounded-xl border border-border/50 bg-card p-6">
                            <h2 className="text-lg font-semibold mb-4">Evidence</h2>
                            <pre className="rounded-lg bg-muted/50 p-4 text-sm font-mono overflow-x-auto whitespace-pre-wrap">
                                {detail.evidence}
                            </pre>
                        </div>

                        {/* Recommendations */}
                        <div className="rounded-xl border border-border/50 bg-card p-6">
                            <h2 className="text-lg font-semibold mb-4">Recommended Actions</h2>
                            <ul className="space-y-2">
                                {detail.recommendations.map((rec, i) => (
                                    <li key={i} className="flex items-start gap-2">
                                        <span className="text-primary font-medium">{i + 1}.</span>
                                        <span>{rec}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>

                    {/* Sidebar - 1 col */}
                    <div className="space-y-6">
                        {/* Actions */}
                        <div className="rounded-xl border border-border/50 bg-card p-6">
                            <h2 className="text-lg font-semibold mb-4">Actions</h2>
                            <AlertActions alertId={detail.id} />
                        </div>

                        {/* Context */}
                        {detail.context && (
                            <div className="rounded-xl border border-border/50 bg-card p-6">
                                <h2 className="text-lg font-semibold mb-4">Context</h2>
                                <dl className="space-y-3">
                                    <div>
                                        <dt className="text-sm text-muted-foreground">Similar Violations</dt>
                                        <dd className="font-medium">{detail.context.similar_violations}</dd>
                                    </div>
                                    <div>
                                        <dt className="text-sm text-muted-foreground">Entity Volume</dt>
                                        <dd className="font-medium">{detail.context.entity_volume}</dd>
                                    </div>
                                </dl>
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}
