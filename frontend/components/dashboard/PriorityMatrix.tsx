"use client";

import { cn } from "@/lib/utils";

interface PriorityIssue {
    id: string;
    title: string;
    entity: string | null;
    severity: string;
    due: string;
    due_date: string;
}

interface PriorityMatrixData {
    matrix: {
        critical: { overdue: PriorityIssue[]; this_week: PriorityIssue[]; this_month: PriorityIssue[]; later: PriorityIssue[] };
        high: { overdue: PriorityIssue[]; this_week: PriorityIssue[]; this_month: PriorityIssue[]; later: PriorityIssue[] };
        medium: { overdue: PriorityIssue[]; this_week: PriorityIssue[]; this_month: PriorityIssue[]; later: PriorityIssue[] };
        low: { overdue: PriorityIssue[]; this_week: PriorityIssue[]; this_month: PriorityIssue[]; later: PriorityIssue[] };
    };
    summary: {
        total_issues: number;
        overdue: number;
        critical_overdue: number;
        needs_attention: number;
    };
}

interface PriorityMatrixProps {
    data: PriorityMatrixData;
    className?: string;
}

const severityLabels = {
    critical: "Critical",
    high: "High",
    medium: "Medium",
    low: "Low",
};

const dueLabels = {
    overdue: "Overdue",
    this_week: "This Week",
    this_month: "This Month",
    later: "Later",
};

const severityColors = {
    critical: "text-red-400",
    high: "text-orange-400",
    medium: "text-amber-400",
    low: "text-blue-400",
};

const cellStyles = {
    critical: {
        overdue: "bg-red-500/30 border-red-500/60",
        this_week: "bg-red-500/20 border-red-500/40",
        this_month: "bg-red-500/10 border-red-500/20",
        later: "bg-red-500/5 border-red-500/10",
    },
    high: {
        overdue: "bg-orange-500/30 border-orange-500/60",
        this_week: "bg-orange-500/20 border-orange-500/40",
        this_month: "bg-orange-500/10 border-orange-500/20",
        later: "bg-orange-500/5 border-orange-500/10",
    },
    medium: {
        overdue: "bg-amber-500/20 border-amber-500/40",
        this_week: "bg-amber-500/15 border-amber-500/30",
        this_month: "bg-amber-500/10 border-amber-500/20",
        later: "bg-amber-500/5 border-amber-500/10",
    },
    low: {
        overdue: "bg-blue-500/15 border-blue-500/30",
        this_week: "bg-blue-500/10 border-blue-500/20",
        this_month: "bg-blue-500/5 border-blue-500/10",
        later: "bg-slate-500/5 border-slate-500/10",
    },
};

export function PriorityMatrix({ data, className }: PriorityMatrixProps) {
    const severities = ["critical", "high", "medium", "low"] as const;
    const dueDates = ["overdue", "this_week", "this_month", "later"] as const;

    const getCount = (severity: typeof severities[number], due: typeof dueDates[number]) => {
        return data.matrix[severity][due].length;
    };

    return (
        <div className={cn("rounded-xl border border-border/50 bg-card p-6", className)}>
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold">Priority Matrix</h3>
                <div className="flex gap-4 text-sm">
                    <span className="text-muted-foreground">
                        <span className="text-red-400 font-semibold">{data.summary.needs_attention}</span> need attention
                    </span>
                    <span className="text-muted-foreground">
                        <span className="text-orange-400 font-semibold">{data.summary.overdue}</span> overdue
                    </span>
                </div>
            </div>

            {/* Matrix Grid */}
            <div className="overflow-x-auto">
                <table className="w-full border-collapse">
                    <thead>
                        <tr>
                            <th className="p-2 text-left text-sm font-medium text-muted-foreground w-24">
                                Severity
                            </th>
                            {dueDates.map((due) => (
                                <th key={due} className="p-2 text-center text-sm font-medium text-muted-foreground">
                                    {dueLabels[due]}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {severities.map((severity) => (
                            <tr key={severity}>
                                <td className={cn("p-2 font-medium text-sm", severityColors[severity])}>
                                    {severityLabels[severity]}
                                </td>
                                {dueDates.map((due) => {
                                    const count = getCount(severity, due);
                                    const items = data.matrix[severity][due];
                                    return (
                                        <td key={due} className="p-1">
                                            <div
                                                className={cn(
                                                    "relative rounded-lg border p-3 min-h-[60px] transition-all hover:scale-[1.02]",
                                                    cellStyles[severity][due],
                                                    count > 0 && "cursor-pointer"
                                                )}
                                                title={items.map(i => i.title).join("\n")}
                                            >
                                                {count > 0 ? (
                                                    <div className="flex flex-col items-center justify-center h-full">
                                                        <span className="text-2xl font-bold">{count}</span>
                                                        <span className="text-xs text-muted-foreground">
                                                            {count === 1 ? "issue" : "issues"}
                                                        </span>
                                                    </div>
                                                ) : (
                                                    <div className="flex items-center justify-center h-full text-muted-foreground/50">
                                                        —
                                                    </div>
                                                )}
                                            </div>
                                        </td>
                                    );
                                })}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Legend */}
            <div className="mt-4 flex items-center justify-center gap-6 text-xs text-muted-foreground">
                <span>← Most Urgent</span>
                <div className="h-2 w-32 rounded-full bg-gradient-to-r from-red-500/60 via-amber-500/40 to-slate-500/20" />
                <span>Less Urgent →</span>
            </div>
        </div>
    );
}
