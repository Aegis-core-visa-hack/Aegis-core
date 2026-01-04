import { cn } from "@/lib/utils";

interface RiskItem {
    name: string;
    risk_level: 'high' | 'medium' | 'low';
    violation_count: number;
}

interface RiskHeatmapProps {
    data: RiskItem[];
    className?: string;
}

export function RiskHeatmap({ data, className }: RiskHeatmapProps) {
    const riskColors = {
        high: 'bg-red-500/20 border-red-500/50 text-red-400',
        medium: 'bg-amber-500/20 border-amber-500/50 text-amber-400',
        low: 'bg-green-500/20 border-green-500/50 text-green-400'
    };

    const riskEmoji = {
        high: '🔴',
        medium: '🟡',
        low: '🟢'
    };

    return (
        <div className={cn("rounded-xl border border-border/50 bg-card p-6", className)}>
            <h3 className="mb-4 text-lg font-semibold">Regulation Risk Heatmap</h3>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-5">
                {data.map((item) => (
                    <div
                        key={item.name}
                        className={cn(
                            "flex flex-col items-center justify-center rounded-lg border p-4 transition-all hover:scale-105",
                            riskColors[item.risk_level]
                        )}
                    >
                        <span className="text-sm font-medium">{item.name}</span>
                        <span className="mt-1 text-2xl">{riskEmoji[item.risk_level]}</span>
                        <span className="mt-1 text-xs opacity-80">
                            {item.violation_count} {item.violation_count === 1 ? 'issue' : 'issues'}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
}
