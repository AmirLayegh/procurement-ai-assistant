export interface Product {
  id: string;
  name: string;
  category: string;
  brand: string;
  cost: number;
  retailPrice: number;
  profitMargin: number; // Percentage, e.g., 20 for 20%
  supplierReliability: number; // Score (e.g., 0-100 or 1-5)
  totalOrders: number;
  revenue: number;
  department: 'Women' | 'Men' | 'Kids' | 'All';
  imageUrl: string;
  description: string;
}

export interface Filters {
  priceRange: [number, number];
  department: string;
  category: string;
  brand: string;
}
