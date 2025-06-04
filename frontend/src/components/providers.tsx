"use client";

import { SidebarProvider } from "@/components/ui/sidebar";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Toaster } from "@/components/ui/toaster";
import type { ReactNode } from 'react';

export function Providers({ children }: { children: ReactNode }) {
  return (
    <TooltipProvider delayDuration={0}>
      <SidebarProvider defaultOpen={true} open={true} onOpenChange={()=>{}}>
        {children}
        <Toaster />
      </SidebarProvider>
    </TooltipProvider>
  );
}
