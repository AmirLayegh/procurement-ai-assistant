import type { ReactNode } from 'react';
import { AppNavSidebar } from '@/components/layout/app-nav-sidebar';
import { AppMainContentArea } from '@/components/layout/app-main-content-area';

export default function MainAppLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen bg-background">
      <AppNavSidebar />
      <AppMainContentArea>
        {children}
      </AppMainContentArea>
    </div>
  );
}
