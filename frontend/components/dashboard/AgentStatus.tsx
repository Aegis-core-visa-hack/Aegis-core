import { cn } from "@/lib/utils";

interface Agent {
    id: number;
    name: string;
    status: 'online' | 'offline' | 'error';
    last_run: string;
    stats?: string;
}

interface AgentStatusProps {
    agents: Agent[];
    className?: string;
}

export function AgentStatus({ agents, className }: AgentStatusProps) {
    const statusStyles = {
        online: 'bg-green-500',
        offline: 'bg-gray-500',
        error: 'bg-red-500'
    };

    return (
        <div className={cn("rounded-xl border border-border/50 bg-card p-6", className)}>
            <h3 className="mb-4 text-lg font-semibold">Agent Status</h3>
            <div className="space-y-3">
                {agents.map((agent) => (
                    <div
                        key={agent.id}
                        className="flex items-center justify-between rounded-lg p-3 transition-colors hover:bg-muted/50"
                    >
                        <div className="flex items-center gap-3">
                            <span
                                className={cn(
                                    "h-2.5 w-2.5 rounded-full animate-pulse",
                                    statusStyles[agent.status]
                                )}
                            />
                            <span className="font-medium">Agent {agent.id}</span>
                            <span className="text-sm text-muted-foreground">({agent.name})</span>
                        </div>
                        <div className="text-right text-sm">
                            <span className="text-muted-foreground">
                                {agent.stats ? agent.stats : `Last: ${agent.last_run}`}
                            </span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
