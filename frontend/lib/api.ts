/**
 * AEGIS API Client
 * Connects frontend to FastAPI backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface FetchOptions {
    method?: 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE';
    body?: Record<string, unknown>;
}

async function apiFetch<T>(endpoint: string, options: FetchOptions = {}): Promise<T> {
    const { method = 'GET', body } = options;

    const config: RequestInit = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (body) {
        config.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
}

// Dashboard APIs
export const dashboardApi = {
    getSummary: () => apiFetch<{ data: DashboardSummary }>('/api/dashboard/summary'),
    getRiskHeatmap: () => apiFetch<{ data: { regulations: RiskHeatmapItem[] } }>('/api/dashboard/risk-heatmap'),
    getRecentAlerts: (limit = 10) => apiFetch<{ data: { alerts: Alert[]; unread_count: number } }>(`/api/dashboard/recent-alerts?limit=${limit}`),
    getAgentActivity: () => apiFetch<{ data: { agents: Agent[]; summary: AgentSummary } }>('/api/dashboard/agent-activity'),
};

// Alerts APIs
export const alertsApi = {
    list: (severity?: string, status?: string) => {
        const params = new URLSearchParams();
        if (severity) params.append('severity', severity);
        if (status) params.append('status', status);
        const query = params.toString();
        return apiFetch<{ data: Alert[] }>(`/api/alerts${query ? `?${query}` : ''}`);
    },
    getDetail: (id: string) => apiFetch<{ data: AlertDetail }>(`/api/alerts/${id}`),
    updateStatus: (id: string, status: string) =>
        apiFetch<{ data: AlertDetail; message: string }>(`/api/alerts/${id}?status=${status}`, { method: 'PATCH' }),
};

// Entities APIs
export const entitiesApi = {
    list: (type?: string, riskLevel?: string, pciStatus?: string) => {
        const params = new URLSearchParams();
        if (type) params.append('type', type);
        if (riskLevel) params.append('risk_level', riskLevel);
        if (pciStatus) params.append('pci_status', pciStatus);
        const query = params.toString();
        return apiFetch<{ data: Entity[] }>(`/api/entities${query ? `?${query}` : ''}`);
    },
    getDetail: (id: string) => apiFetch<{ data: EntityDetail }>(`/api/entities/${id}`),
};

// Chat APIs
export const chatApi = {
    send: (message: string, conversationId?: string) =>
        apiFetch<{ data: ChatResponse }>('/api/chat', {
            method: 'POST',
            body: { message, conversation_id: conversationId },
        }),
};

// Demo APIs
export const demoApi = {
    scan: (logContent?: string) =>
        apiFetch<{ data: ScanResult }>(`/api/demo/scan${logContent ? `?log_content=${encodeURIComponent(logContent)}` : ''}`, {
            method: 'POST',
        }),
    validateCard: (cardNumber: string) =>
        apiFetch<{ data: CardValidation }>(`/api/demo/validate-card?card_number=${encodeURIComponent(cardNumber)}`, {
            method: 'POST',
        }),
};

// Type definitions
export interface DashboardSummary {
    compliance_score: { value: number; change: number; trend: 'up' | 'down' | 'stable' };
    at_risk_entities: { value: number; change: number; trend: 'up' | 'down' | 'stable' };
    violations_24h: { value: number; change: number; trend: 'up' | 'down' | 'stable' };
    agents_online: number;
    agents_total: number;
}

export interface RiskHeatmapItem {
    name: string;
    risk_level: 'high' | 'medium' | 'low';
    score: number;
    open_violations: number;
    jurisdiction: string;
}

export interface Alert {
    id: string;
    severity: 'critical' | 'high' | 'medium' | 'low';
    title: string;
    description: string;
    timestamp: string;
    entity_id: string | null;
    regulation: string;
    status: string;
}

export interface AlertDetail extends Alert {
    evidence: string;
    recommendations: string[];
    context: {
        similar_violations: number;
        entity_name: string;
        entity_volume: string;
    };
}

export interface Entity {
    id: string;
    name: string;
    type: 'bank' | 'merchant' | 'vendor';
    pci_status: 'valid' | 'expiring' | 'expired';
    pci_expiry: string;
    risk_level: 'high' | 'medium' | 'low';
    violation_count: number;
}

export interface EntityDetail extends Entity {
    country?: string;
    violations: Alert[];
}

export interface Agent {
    id: number;
    name: string;
    display_name: string;
    status: 'online' | 'offline' | 'running' | 'error';
    last_run: string;
    description: string;
    stats?: string;
}

export interface AgentSummary {
    total: number;
    running: number;
    idle: number;
    error: number;
}

export interface ChatResponse {
    response: string;
    suggested_actions: string[];
    conversation_id: string;
}

export interface ScanResult {
    scan_result: {
        scanned_at: string;
        violations_found: number;
        violations: unknown[];
        status: string;
    };
    alert_created: Alert | null;
    message: string;
}

export interface CardValidation {
    masked_number: string;
    is_valid_luhn: boolean;
    card_type: string | null;
    would_trigger_alert: boolean;
}
