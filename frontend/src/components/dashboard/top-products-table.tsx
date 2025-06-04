import type { Product } from '@/types';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';

interface TopProductsTableProps {
  products: Product[];
}

export function TopProductsTable({ products }: TopProductsTableProps) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-[250px]">Product Name</TableHead>
          <TableHead>Category</TableHead>
          <TableHead>Brand</TableHead>
          <TableHead className="text-right">Revenue</TableHead>
          <TableHead className="text-right">Profit Margin</TableHead>
          <TableHead className="text-right">Total Orders</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {products.map((product) => (
          <TableRow key={product.id}>
            <TableCell className="font-medium">{product.name}</TableCell>
            <TableCell><Badge variant="outline">{product.category}</Badge></TableCell>
            <TableCell>{product.brand}</TableCell>
            <TableCell className="text-right">${product.revenue.toLocaleString()}</TableCell>
            <TableCell className="text-right">{product.profitMargin.toFixed(1)}%</TableCell>
            <TableCell className="text-right">{product.totalOrders.toLocaleString()}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
