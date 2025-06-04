"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Briefcase, LayoutDashboard, Search as SearchIcon, PanelLeft } from 'lucide-react';
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarTrigger,
  useSidebar,
} from '@/components/ui/sidebar';
import { cn } from '@/lib/utils';

export function AppNavSidebar() {
  const pathname = usePathname();
  const { isMobile } = useSidebar();

  const menuItems = [
    { href: '/', label: 'Search', icon: SearchIcon },
    { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  ];

  return (
    <Sidebar
      side="left"
      variant="sidebar"
      collapsible={isMobile ? "offcanvas" : "icon"}
      className="border-r"
    >
      <SidebarHeader className="p-3 justify-between">
        <Link href="/" className="flex items-center gap-2 font-semibold text-lg text-primary hover:text-primary/90">
          <Briefcase className="h-7 w-7" />
          <span className={cn("group-data-[collapsible=icon]:hidden", {"hidden": isMobile && !useSidebar().openMobile })}>ProcureAI</span>
        </Link>
        {!isMobile && <SidebarTrigger className="hidden lg:flex" />}
      </SidebarHeader>
      <SidebarContent className="p-2">
        <SidebarMenu>
          {menuItems.map((item) => (
            <SidebarMenuItem key={item.href}>
              <Link href={item.href} passHref legacyBehavior>
                <SidebarMenuButton
                  asChild
                  isActive={pathname === item.href}
                  tooltip={{ children: item.label, className: "group-data-[collapsible=icon]:block hidden" }}
                  className="justify-start"
                >
                  <a>
                    <item.icon className="h-5 w-5" />
                    <span className="group-data-[collapsible=icon]:hidden">{item.label}</span>
                  </a>
                </SidebarMenuButton>
              </Link>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarContent>
    </Sidebar>
  );
}
