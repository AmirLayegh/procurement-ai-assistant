import Image from 'next/image';
import type { Product } from '@/types';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { DollarSign, Percent, TrendingUp, CheckCircle, ShoppingCart } from 'lucide-react';

interface ProductCardProps {
  product: Product;
}

export function ProductCard({ product }: ProductCardProps) {
  return (
    <Card className="flex flex-col h-full shadow-lg hover:shadow-xl transition-shadow duration-300 rounded-lg overflow-hidden">
      <CardHeader className="p-0">
        <div className="relative w-full h-48">
          <Image
            src={product.imageUrl}
            alt={product.name}
            layout="fill"
            objectFit="cover"
            data-ai-hint="product image"
          />
        </div>
      </CardHeader>
      <CardContent className="p-4 flex-grow">
        <CardTitle className="text-lg font-semibold mb-1">{product.name}</CardTitle>
        <div className="flex items-center space-x-2 mb-2">
            <Badge variant="secondary">{product.category}</Badge>
            <Badge variant="outline">{product.brand}</Badge>
        </div>
        <CardDescription className="text-xs text-muted-foreground mb-3 h-10 overflow-hidden">
            {product.description}
        </CardDescription>
        
        <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
            <div className="flex items-center" title="Cost">
                <DollarSign className="h-4 w-4 mr-1 text-muted-foreground" /> Cost: ${product.cost.toFixed(2)}
            </div>
            <div className="flex items-center" title="Retail Price">
                <DollarSign className="h-4 w-4 mr-1 text-muted-foreground" /> Retail: ${product.retailPrice.toFixed(2)}
            </div>
            <div className="flex items-center" title="Profit Margin">
                <Percent className="h-4 w-4 mr-1 text-muted-foreground" /> Margin: {product.profitMargin.toFixed(1)}%
            </div>
            <div className="flex items-center" title="Supplier Reliability">
                <CheckCircle className="h-4 w-4 mr-1 text-green-500" /> Reliability: {product.supplierReliability}%
            </div>
        </div>
      </CardContent>
      <CardFooter className="p-4 bg-muted/50 border-t">
        <div className="flex justify-between w-full text-xs text-muted-foreground">
            <div className="flex items-center" title="Total Orders">
                <ShoppingCart className="h-3.5 w-3.5 mr-1" /> Orders: {product.totalOrders}
            </div>
            <div className="flex items-center" title="Total Revenue">
                <TrendingUp className="h-3.5 w-3.5 mr-1" /> Revenue: ${product.revenue.toLocaleString()}
            </div>
        </div>
      </CardFooter>
    </Card>
  );
}
