'use client';

import { useState, useRef, useEffect } from 'react';
import { Header } from "@/components/layout/Header";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
    actions?: string[];
}

const suggestedQueries = [
    "What's our current PCI risk?",
    "Which banks have expiring certifications?",
    "Show me new regulations this week",
    "Generate compliance summary"
];

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: '1',
            role: 'assistant',
            content: `**Welcome to AEGIS Chat!**

I'm your AI compliance assistant. I can help you with:
- Checking compliance status across your ecosystem
- Finding relevant regulations
- Generating reports and summaries
- Answering questions about your compliance posture

What would you like to know?`,
            timestamp: new Date(),
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
            timestamp: new Date(),
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            // Call the backend API
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input }),
            });

            const data = await response.json();

            const assistantMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: data.data.response,
                timestamp: new Date(),
                actions: data.data.suggested_actions,
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            // Fallback to mock on error
            console.error('Chat API error:', error);
            const assistantMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: 'Sorry, I encountered an error connecting to the backend. Please ensure the backend server is running on http://localhost:8000',
                timestamp: new Date(),
            };
            setMessages(prev => [...prev, assistantMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSuggestedQuery = (query: string) => {
        setInput(query);
    };

    return (
        <div className="flex min-h-screen flex-col bg-background">
            <Header />
            <main className="flex flex-1 flex-col container max-w-screen-lg px-4 py-6">
                <div className="mb-4">
                    <h1 className="text-2xl font-bold tracking-tight">Ask AEGIS</h1>
                    <p className="text-muted-foreground">
                        Natural language interface for compliance queries
                    </p>
                </div>

                {/* Chat Messages */}
                <div className="flex-1 rounded-xl border border-border/50 bg-card mb-4">
                    <ScrollArea className="h-[calc(100vh-320px)] p-4" ref={scrollRef}>
                        <div className="space-y-4">
                            {messages.map((message) => (
                                <div
                                    key={message.id}
                                    className={cn(
                                        "flex",
                                        message.role === 'user' ? 'justify-end' : 'justify-start'
                                    )}
                                >
                                    <div
                                        className={cn(
                                            "max-w-[80%] rounded-lg px-4 py-3",
                                            message.role === 'user'
                                                ? 'bg-primary text-primary-foreground'
                                                : 'bg-muted'
                                        )}
                                    >
                                        <div className="prose prose-sm dark:prose-invert max-w-none">
                                            {message.content.split('\n').map((line, i) => (
                                                <p key={i} className={cn("mb-1 last:mb-0", line.startsWith('**') && 'font-semibold')}>
                                                    {line.replace(/\*\*/g, '')}
                                                </p>
                                            ))}
                                        </div>
                                        {message.actions && message.actions.length > 0 && (
                                            <div className="mt-3 flex flex-wrap gap-2">
                                                {message.actions.map((action) => (
                                                    <Button
                                                        key={action}
                                                        variant="outline"
                                                        size="sm"
                                                        onClick={() => console.log(`Action: ${action}`)}
                                                    >
                                                        {action}
                                                    </Button>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                            {isLoading && (
                                <div className="flex justify-start">
                                    <div className="bg-muted rounded-lg px-4 py-3">
                                        <div className="flex gap-1">
                                            <span className="h-2 w-2 rounded-full bg-muted-foreground/50 animate-bounce" style={{ animationDelay: '0ms' }} />
                                            <span className="h-2 w-2 rounded-full bg-muted-foreground/50 animate-bounce" style={{ animationDelay: '150ms' }} />
                                            <span className="h-2 w-2 rounded-full bg-muted-foreground/50 animate-bounce" style={{ animationDelay: '300ms' }} />
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </ScrollArea>
                </div>

                {/* Suggested Queries */}
                <div className="mb-4 flex flex-wrap gap-2">
                    {suggestedQueries.map((query) => (
                        <Button
                            key={query}
                            variant="outline"
                            size="sm"
                            onClick={() => handleSuggestedQuery(query)}
                            className="text-xs"
                        >
                            {query}
                        </Button>
                    ))}
                </div>

                {/* Input */}
                <div className="flex gap-2">
                    <Input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Ask about compliance, regulations, or risks..."
                        className="flex-1"
                        disabled={isLoading}
                    />
                    <Button onClick={handleSend} disabled={isLoading || !input.trim()}>
                        Send
                    </Button>
                </div>
            </main>
        </div>
    );
}
