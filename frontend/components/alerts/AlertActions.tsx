'use client';

import { Button } from "@/components/ui/button";

interface AlertActionsProps {
    alertId: string;
}

export function AlertActions({ alertId }: AlertActionsProps) {
    const handleCreateCase = () => {
        console.log(`Creating case for alert ${alertId}...`);
        alert('Case created! (Demo)');
    };

    const handleSendAlert = () => {
        console.log(`Sending alert for ${alertId}...`);
        alert('Alert sent to stakeholders! (Demo)');
    };

    const handleMarkResolved = () => {
        console.log(`Marking ${alertId} as resolved...`);
        alert('Alert marked as resolved! (Demo)');
    };

    return (
        <div className="space-y-2">
            <Button className="w-full" onClick={handleCreateCase}>
                Create Case
            </Button>
            <Button variant="outline" className="w-full" onClick={handleSendAlert}>
                Send Alert
            </Button>
            <Button variant="secondary" className="w-full" onClick={handleMarkResolved}>
                Mark Resolved
            </Button>
        </div>
    );
}
