import { cn } from "@/lib/utils";

interface MetricCardProps {
    title: string;
    value: string | number;
    change?: number;
    changeLabel?: string;
    icon?: React.ReactNode;
    trend?: 'up' | 'down' | 'neutral';
    className?: string;
}

export function MetricCard({
    title,
    value,
    change,
    changeLabel,
    trend = 'neutral',
    className
}: MetricCardProps) {
    const trendColor = {
        up: 'text-green-500',
        down: 'text-red-500',
        neutral: 'text-muted-foreground'
    };

    const trendIcon = {
        up: '▲',
        down: '▼',
        neutral: ''
    };

    return (
        <div className={cn(
            "rounded-xl border border-border/50 bg-card p-6 shadow-sm transition-all hover:border-border hover:shadow-md",
            className
        )}>
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <div className="mt-2 flex items-baseline gap-2">
                <span className="text-3xl font-bold tracking-tight">{value}</span>
                {change !== undefined && (
                    <span className={cn("text-sm font-medium", trendColor[trend])}>
                        {trendIcon[trend]} {change > 0 ? '+' : ''}{change}{changeLabel || ''}
                    </span>
                )}
            </div>
        </div>
    );
}
