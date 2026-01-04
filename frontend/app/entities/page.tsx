"use client";

import { useEffect, useState } from 'react';
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
import { entitiesApi, Entity } from "@/lib/api";
import { mockEntities } from "@/lib/mockData";
import { cn } from "@/lib/utils";

export default function EntitiesPage() {
    const [entities, setEntities] = useState<Entity[]>([]);
    const [loading, setLoading] = useState(true);
    const [useApi, setUseApi] = useState(true);
    const [typeFilter, setTypeFilter] = useState<string>('');
    const [riskFilter, setRiskFilter] = useState<string>('');
    const [pciFilter, setPciFilter] = useState<string>('');
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        async function fetchEntities() {
            try {
                const res = await entitiesApi.list(
                    typeFilter || undefined,
                    riskFilter || undefined,
                    pciFilter || undefined
                );
                setEntities(res.data);
                setUseApi(true);
            } catch (error) {
                console.error("API unavailable, using mock data:", error);
                setEntities(mockEntities);
                setUseApi(false);
            } finally {
                setLoading(false);
            }
        }
        fetchEntities();
    }, [typeFilter, riskFilter, pciFilter]);

    // Filter entities by search term
    const filteredEntities = entities.filter(e =>
        e.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        e.id.toLowerCase().includes(searchTerm.toLowerCase())
    );

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

    if (loading) {
        return (
            <div className="min-h-screen bg-background">
                <Header />
                <main className="container max-w-screen-2xl px-4 py-8">
                    <div className="flex items-center justify-center h-[60vh]">
                        <div className="flex flex-col items-center gap-4">
                            <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin" />
                            <p className="text-muted-foreground">Loading entities...</p>
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
                        <h1 className="text-3xl font-bold tracking-tight">Entities</h1>
                        <p className="text-muted-foreground">
                            {filteredEntities.length} entities • {filteredEntities.filter(e => e.risk_level === 'high').length} high risk
                            {!useApi && <span className="ml-2 text-yellow-500">(Demo Mode)</span>}
                        </p>
                    </div>
                    <Button variant="outline">Export</Button>
                </div>

                {/* Filters */}
                <div className="mb-6 flex flex-wrap gap-3">
                    <Input
                        placeholder="Search entities..."
                        className="max-w-xs"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                    <select
                        value={typeFilter}
                        onChange={(e) => setTypeFilter(e.target.value)}
                        className="px-3 py-2 text-sm rounded-md border border-border bg-background"
                    >
                        <option value="">All Types</option>
                        <option value="bank">Banks</option>
                        <option value="merchant">Merchants</option>
                        <option value="vendor">Vendors</option>
                    </select>
                    <select
                        value={riskFilter}
                        onChange={(e) => setRiskFilter(e.target.value)}
                        className="px-3 py-2 text-sm rounded-md border border-border bg-background"
                    >
                        <option value="">All Risk Levels</option>
                        <option value="high">High Risk</option>
                        <option value="medium">Medium Risk</option>
                        <option value="low">Low Risk</option>
                    </select>
                    <select
                        value={pciFilter}
                        onChange={(e) => setPciFilter(e.target.value)}
                        className="px-3 py-2 text-sm rounded-md border border-border bg-background"
                    >
                        <option value="">All PCI Status</option>
                        <option value="valid">Valid</option>
                        <option value="expiring">Expiring</option>
                        <option value="expired">Expired</option>
                    </select>
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
                            {filteredEntities.map((entity) => (
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
                            {filteredEntities.length === 0 && (
                                <TableRow>
                                    <TableCell colSpan={7} className="text-center py-8 text-muted-foreground">
                                        No entities found matching your filters.
                                    </TableCell>
                                </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </div>

                {/* Pagination */}
                <div className="mt-4 flex items-center justify-between">
                    <p className="text-sm text-muted-foreground">
                        Showing {filteredEntities.length} of {entities.length} entities
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
