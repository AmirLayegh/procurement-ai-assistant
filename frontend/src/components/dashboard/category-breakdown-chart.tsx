"use client"

import type { Product } from '@/types';
import { Pie, PieChart, ResponsiveContainer, Cell, Tooltip, Legend } from 'recharts';
import { ChartConfig, ChartContainer, ChartTooltipContent } from "@/components/ui/chart"

interface CategoryBreakdownChartProps {
  data: Product[];
}

const chartColors = [
  "hsl(var(--chart-1))",
  "hsl(var(--chart-2))",
  "hsl(var(--chart-3))",
  "hsl(var(--chart-4))",
  "hsl(var(--chart-5))",
];

export function CategoryBreakdownChart({ data }: CategoryBreakdownChartProps) {
  const categoryData: { [key: string]: number } = {};
  data.forEach(product => {
    if (!categoryData[product.category]) {
      categoryData[product.category] = 0;
    }
    categoryData[product.category] += product.revenue;
  });

  const chartData = Object.entries(categoryData).map(([name, value]) => ({ name, value }));

  const chartConfig = chartData.reduce<ChartConfig>((acc, entry, index) => {
    acc[entry.name] = {
      label: entry.name,
      color: chartColors[index % chartColors.length],
    };
    return acc;
  }, {});


  return (
    <ChartContainer config={chartConfig} className="h-[300px] w-full max-w-xs mx-auto">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Tooltip content={<ChartTooltipContent nameKey="name" />} />
          <Legend/>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            labelLine={false}
            label={({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
              const RADIAN = Math.PI / 180;
              const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
              const x = cx + radius * Math.cos(-midAngle * RADIAN);
              const y = cy + radius * Math.sin(-midAngle * RADIAN);
              return (percent * 100) > 5 ? ( // Only show label if percent is > 5%
                <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" fontSize="10px">
                  {`${(percent * 100).toFixed(0)}%`}
                </text>
              ) : null;
            }}
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={chartConfig[entry.name]?.color || chartColors[index % chartColors.length]} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
}
