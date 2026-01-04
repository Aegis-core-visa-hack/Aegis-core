'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';

export function Header() {
    const pathname = usePathname();

    return (
        <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-14 max-w-screen-2xl items-center px-4">
                <Link href="/" className="mr-6 flex items-center space-x-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
                        <span className="text-lg font-bold text-primary-foreground">A</span>
                    </div>
                    <span className="hidden font-bold sm:inline-block">AEGIS</span>
                </Link>

                <nav className="flex items-center gap-4 text-sm lg:gap-6">
                    <Link
                        href="/"
                        className={cn(
                            "transition-colors hover:text-foreground/80",
                            pathname === "/" ? "text-foreground" : "text-foreground/60"
                        )}
                    >
                        Dashboard
                    </Link>
                    <Link
                        href="/alerts"
                        className={cn(
                            "transition-colors hover:text-foreground/80",
                            pathname?.startsWith("/alerts") ? "text-foreground" : "text-foreground/60"
                        )}
                    >
                        Alerts
                    </Link>
                    <Link
                        href="/entities"
                        className={cn(
                            "transition-colors hover:text-foreground/80",
                            pathname === "/entities" ? "text-foreground" : "text-foreground/60"
                        )}
                    >
                        Entities
                    </Link>
                </nav>

                <div className="flex flex-1 items-center justify-end gap-2">
                    <Link
                        href="/chat"
                        className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90"
                    >
                        Ask AEGIS
                    </Link>
                </div>
            </div>
        </header>
    );
}
