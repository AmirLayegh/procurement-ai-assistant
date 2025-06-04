"use client"

import type { Product } from '@/types';
import { Bar, BarChart, CartesianGrid, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ChartConfig, ChartContainer, ChartTooltipContent } from "@/components/ui/chart"

interface CostProfitMarginChartProps {
  data: Product[];
}

const chartConfig = {
  cost: {
    label: "Cost",
    color: "hsl(var(--chart-2))",
  },
  profitMargin: {
    label: "Profit Margin (%)",
    color: "hsl(var(--chart-1))",
  },
} satisfies ChartConfig

export function CostProfitMarginChart({ data }: CostProfitMarginChartProps) {
  const chartData = data.map(p => ({
    name: p.name.length > 15 ? p.name.substring(0,12) + "..." : p.name, // Truncate long names
    cost: p.cost,
    profitMargin: parseFloat(p.profitMargin.toFixed(1)),
  })).slice(0, 10); // Show top 10 for readability

  return (
    <ChartContainer config={chartConfig} className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" tick={{ fontSize: 10 }} interval={0} angle={-30} textAnchor="end" height={50}/>
          <YAxis yAxisId="left" orientation="left" stroke="hsl(var(--chart-2))" tick={{ fontSize: 10 }} />
          <YAxis yAxisId="right" orientation="right" stroke="hsl(var(--chart-1))" tick={{ fontSize: 10 }} />
          <Tooltip content={<ChartTooltipContent />} />
          <Legend />
          <Bar yAxisId="left" dataKey="cost" fill="var(--color-cost)" radius={[4, 4, 0, 0]} />
          <Bar yAxisId="right" dataKey="profitMargin" fill="var(--color-profitMargin)" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
}
