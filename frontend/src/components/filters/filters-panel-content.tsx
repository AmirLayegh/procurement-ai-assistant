"use client";

import type { Filters } from '@/types';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { departments, categories, brands } from '@/lib/mock-data';
import { Separator } from '../ui/separator';

interface FiltersPanelContentProps {
  filters: Filters;
  onFiltersChange: (newFilters: Filters) => void;
}

export function FiltersPanelContent({ filters, onFiltersChange }: FiltersPanelContentProps) {
  const handlePriceChange = (newRange: [number, number]) => {
    onFiltersChange({ ...filters, priceRange: newRange });
  };

  const handleDepartmentChange = (value: string) => {
    onFiltersChange({ ...filters, department: value });
  };

  const handleCategoryChange = (value: string) => {
    onFiltersChange({ ...filters, category: value });
  };

  const handleBrandChange = (value: string) => {
    onFiltersChange({ ...filters, brand: value });
  };

  return (
    <div className="space-y-6">
      <div>
        <Label htmlFor="price-range" className="text-sm font-medium">Price Range</Label>
        <div className="mt-2 flex justify-between text-xs text-muted-foreground">
          <span>${filters.priceRange[0]}</span>
          <span>${filters.priceRange[1]}</span>
        </div>
        <Slider
          id="price-range"
          min={0}
          max={500} // Max price in mock data or a reasonable upper limit
          step={10}
          value={filters.priceRange}
          onValueChange={(value) => handlePriceChange(value as [number, number])}
          className="mt-1"
        />
      </div>

      <Separator />

      <div>
        <Label htmlFor="department-select" className="text-sm font-medium">Department</Label>
        <Select value={filters.department} onValueChange={handleDepartmentChange}>
          <SelectTrigger id="department-select" className="mt-1">
            <SelectValue placeholder="Select Department" />
          </SelectTrigger>
          <SelectContent>
            {departments.map(dept => (
              <SelectItem key={dept} value={dept}>{dept}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <Separator />

      <div>
        <Label htmlFor="category-select" className="text-sm font-medium">Category</Label>
        <Select value={filters.category} onValueChange={handleCategoryChange}>
          <SelectTrigger id="category-select" className="mt-1">
            <SelectValue placeholder="Select Category" />
          </SelectTrigger>
          <SelectContent>
            {categories.map(cat => (
              <SelectItem key={cat} value={cat}>{cat}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <Separator />
      
      <div>
        <Label htmlFor="brand-select" className="text-sm font-medium">Brand</Label>
        <Select value={filters.brand} onValueChange={handleBrandChange}>
          <SelectTrigger id="brand-select" className="mt-1">
            <SelectValue placeholder="Select Brand" />
          </SelectTrigger>
          <SelectContent>
            {brands.map(brand => (
              <SelectItem key={brand} value={brand}>{brand}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
