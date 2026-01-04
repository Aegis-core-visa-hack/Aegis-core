import Link from 'next/link';
import { Header } from "@/components/layout/Header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { mockEntities } from "@/lib/mockData";
import { cn } from "@/lib/utils";

export default function EntitiesPage() {
    const riskStyles = {
        high: 'bg-red-500/20 text-red-400 border-red-500/50',
        medium: 'bg-amber-500/20 text-amber-400 border-amber-500/50',
        low: 'bg-green-500/20 text-green-400 border-green-500/50',
    };

    const pciStatusStyles = {
        valid: { icon: '✅', label: 'Valid', class: 'text-green-400' },
        expiring: { icon: '⚠️', label: 'Expiring', class: 'text-amber-400' },
        expired: { icon: '❌', label: 'Expired', class: 'text-red-400' },
    };

    const typeLabels = {
        bank: 'Bank',
        merchant: 'Merchant',
        vendor: 'Vendor',
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        const now = new Date();
        const diff = date.getTime() - now.getTime();
        const days = Math.ceil(diff / (1000 * 60 * 60 * 24));

        if (days < 0) return 'Expired';
        if (days <= 30) return `${days} days`;
        return date.toLocaleDateString();
    };

    return (
        <div className="min-h-screen bg-background">
            <Header />
            <main className="container max-w-screen-2xl px-4 py-8">
                <div className="mb-8 flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">Entities</h1>
                        <p className="text-muted-foreground">
                            {mockEntities.length} entities • {mockEntities.filter(e => e.risk_level === 'high').length} high risk
                        </p>
                    </div>
                    <Button variant="outline">Export</Button>
                </div>

                {/* Filters */}
                <div className="mb-6 flex flex-wrap gap-3">
                    <Input placeholder="Search entities..." className="max-w-xs" />
                    <Button variant="outline" size="sm">All Types</Button>
                    <Button variant="outline" size="sm">All Risk Levels</Button>
                    <Button variant="outline" size="sm">All PCI Status</Button>
                </div>

                {/* Table */}
                <div className="rounded-xl border border-border/50 bg-card">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>ID</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>PCI Status</TableHead>
                                <TableHead>Risk Level</TableHead>
                                <TableHead>Violations</TableHead>
                                <TableHead className="text-right">Action</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {mockEntities.map((entity) => (
                                <TableRow key={entity.id}>
                                    <TableCell className="font-mono text-sm">{entity.id}</TableCell>
                                    <TableCell className="font-medium">{entity.name}</TableCell>
                                    <TableCell>
                                        <Badge variant="outline" className="capitalize">
                                            {typeLabels[entity.type]}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <span className={cn("flex items-center gap-1", pciStatusStyles[entity.pci_status].class)}>
                                            <span>{pciStatusStyles[entity.pci_status].icon}</span>
                                            <span>{formatDate(entity.pci_expiry)}</span>
                                        </span>
                                    </TableCell>
                                    <TableCell>
                                        <Badge
                                            variant="outline"
                                            className={cn("uppercase text-xs", riskStyles[entity.risk_level])}
                                        >
                                            {entity.risk_level}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        {entity.violation_count > 0 ? (
                                            <span className="text-red-400">{entity.violation_count}</span>
                                        ) : (
                                            <span className="text-muted-foreground">0</span>
                                        )}
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="ghost" size="sm">
                                            View
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </div>

                {/* Pagination */}
                <div className="mt-4 flex items-center justify-between">
                    <p className="text-sm text-muted-foreground">
                        Showing {mockEntities.length} of {mockEntities.length} entities
                    </p>
                    <div className="flex gap-1">
                        <Button variant="outline" size="sm" disabled>←</Button>
                        <Button variant="outline" size="sm" className="bg-primary text-primary-foreground">1</Button>
                        <Button variant="outline" size="sm" disabled>→</Button>
                    </div>
                </div>
            </main>
        </div>
    );
}
