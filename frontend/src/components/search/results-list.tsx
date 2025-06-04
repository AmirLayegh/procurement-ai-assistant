import type { Product } from '@/types';
import { ProductCard } from './product-card';

interface ResultsListProps {
  products: Product[];
}

export function ResultsList({ products }: ResultsListProps) {
  if (products.length === 0) {
    return <p className="text-center text-muted-foreground mt-8">No products found matching your criteria.</p>;
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-4 md:gap-6">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
