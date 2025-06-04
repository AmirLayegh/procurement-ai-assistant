"use client";

import { TopProductsTable } from '@/components/dashboard/top-products-table';
import { CostProfitMarginChart } from '@/components/dashboard/cost-profit-margin-chart';
import { CategoryBreakdownChart } from '@/components/dashboard/category-breakdown-chart';
import { mockProducts } from '@/lib/mock-data';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { DollarSign, ListChecks, PieChart as PieChartIcon } from 'lucide-react';

export default function DashboardPage() {
  // Sort products by revenue for top products, or use a dedicated API/logic
  const topProducts = [...mockProducts].sort((a, b) => b.revenue - a.revenue).slice(0, 5);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Procurement Dashboard</h1>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${mockProducts.reduce((sum, p) => sum + p.revenue, 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              Across all listed products
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Orders</CardTitle>
            <ListChecks className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {mockProducts.reduce((sum, p) => sum + p.totalOrders, 0).toLocaleString()}
            </div>
             <p className="text-xs text-muted-foreground">
              Total orders placed
            </p>
          </CardContent>
        </Card>
         <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Product Categories</CardTitle>
            <PieChartIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {[...new Set(mockProducts.map(p => p.category))].length}
            </div>
             <p className="text-xs text-muted-foreground">
              Unique categories available
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-2">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Cost vs. Profit Margin</CardTitle>
          </CardHeader>
          <CardContent className="pl-2">
            <CostProfitMarginChart data={mockProducts} />
          </CardContent>
        </Card>
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Category Breakdown (by Revenue)</CardTitle>
          </CardHeader>
          <CardContent className="flex justify-center items-center">
            <CategoryBreakdownChart data={mockProducts} />
          </CardContent>
        </Card>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Top Performing Products (by Revenue)</CardTitle>
        </CardHeader>
        <CardContent>
          <TopProductsTable products={topProducts} />
        </CardContent>
      </Card>
    </div>
  );
}
