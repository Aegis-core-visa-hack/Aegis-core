import Link from 'next/link';
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

interface Alert {
    id: string;
    severity: 'critical' | 'high' | 'medium' | 'low';
    title: string;
    description: string;
    timestamp: string;
    entity_id?: string | null;
    regulation?: string;
    status: string;
}

interface AlertListProps {
    alerts: Alert[];
    className?: string;
    showViewAll?: boolean;
}

export function AlertList({ alerts, className, showViewAll = true }: AlertListProps) {
    const severityStyles = {
        critical: 'bg-red-500/20 text-red-400 border-red-500/50',
        high: 'bg-orange-500/20 text-orange-400 border-orange-500/50',
        medium: 'bg-amber-500/20 text-amber-400 border-amber-500/50',
        low: 'bg-blue-500/20 text-blue-400 border-blue-500/50',
    };

    const severityIcon = {
        critical: '🔴',
        high: '🟠',
        medium: '🟡',
        low: '🔵',
    };

    const formatTime = (timestamp: string) => {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now.getTime() - date.getTime();
        const minutes = Math.floor(diff / 60000);

        if (minutes < 60) return `${minutes} min ago`;
        if (minutes < 1440) return `${Math.floor(minutes / 60)} hours ago`;
        return date.toLocaleDateString();
    };

    return (
        <div className={cn("rounded-xl border border-border/50 bg-card p-6", className)}>
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold">Recent Alerts</h3>
                {showViewAll && (
                    <Link href="/alerts" className="text-sm text-primary hover:underline">
                        View All →
                    </Link>
                )}
            </div>
            <div className="space-y-3">
                {alerts.map((alert) => (
                    <Link
                        key={alert.id}
                        href={`/alerts/${alert.id}`}
                        className="flex items-start gap-3 rounded-lg p-3 transition-colors hover:bg-muted/50"
                    >
                        <span className="mt-0.5 text-lg">{severityIcon[alert.severity]}</span>
                        <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2">
                                <span className="text-xs text-muted-foreground">{formatTime(alert.timestamp)}</span>
                                <Badge
                                    variant="outline"
                                    className={cn("text-xs uppercase", severityStyles[alert.severity])}
                                >
                                    {alert.severity}
                                </Badge>
                            </div>
                            <p className="mt-1 font-medium truncate">{alert.title}</p>
                            <p className="text-sm text-muted-foreground truncate">{alert.description}</p>
                        </div>
                    </Link>
                ))}
            </div>
        </div>
    );
}
