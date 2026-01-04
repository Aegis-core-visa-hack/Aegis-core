import Link from 'next/link';
import { Header } from "@/components/layout/Header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { mockAlerts } from "@/lib/mockData";
import { cn } from "@/lib/utils";

export default function AlertsPage() {
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

    return (
        <div className="min-h-screen bg-background">
            <Header />
            <main className="container max-w-screen-2xl px-4 py-8">
                <div className="mb-8 flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">Alerts</h1>
                        <p className="text-muted-foreground">
                            {mockAlerts.length} total alerts • {mockAlerts.filter(a => a.status === 'open').length} open
                        </p>
                    </div>
                    <Button variant="outline">Export</Button>
                </div>

                <div className="rounded-xl border border-border/50 bg-card">
                    <div className="divide-y divide-border/50">
                        {mockAlerts.map((alert) => (
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
                    </div>
                </div>
            </main>
        </div>
    );
}
