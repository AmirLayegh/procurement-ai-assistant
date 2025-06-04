
"use client";

import { useState, useEffect, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { Filter } from 'lucide-react';
import { FiltersPanelContent } from '@/components/filters/filters-panel-content';
import { SearchBar } from '@/components/search/search-bar';
import { ResultsList } from '@/components/search/results-list';
import type { Product, Filters } from '@/types';
import { mockProducts, defaultFilters } from '@/lib/mock-data';
// import { generateDynamicSearchQueries } from '@/ai/flows/generate-dynamic-search-queries'; // Removed this import
import { useToast } from '@/hooks/use-toast';

const CLOUD_RUN_API_ENDPOINT = 'https://procurement-api-186236752725.europe-north2.run.app/api/v1/search/procurement_query';

export default function SearchPage() {
  const [filters, setFilters] = useState<Filters>(defaultFilters);
  const [searchTerm, setSearchTerm] = useState('');
  const [aiQueryData, setAiQueryData] = useState<{ query: string; preference: string } | null>(null);
  const [displayedProducts, setDisplayedProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const performSearchAndFilter = useCallback(async () => {
    setIsLoading(true);
    
    let queryToSendToApi = searchTerm;
    
    if (aiQueryData) {
      queryToSendToApi = aiQueryData.query;
    }
    
    if (!queryToSendToApi?.trim()) {
      queryToSendToApi = "all products"; // Default query for initial load or empty search
    }
    
    const payload = {
      natural_query: queryToSendToApi,
      limit: 20 // As per API example and previous setting
    };

    try {
      console.log("Calling API with payload:", payload);
      toast({ title: "Fetching Products", description: `Query: ${payload.natural_query}` });

      const response = await fetch(CLOUD_RUN_API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("API Error Response:", response.status, errorText);
        throw new Error(`API Error: ${response.status} ${response.statusText}. ${errorText || ''}`);
      }

      const apiResponse = await response.json();
      
      const productsFromApi: Product[] = apiResponse.entries?.map((entry: any) => ({
        id: entry.id,
        name: entry.fields.name,
        category: entry.fields.category,
        brand: entry.fields.brand,
        department: entry.fields.department,
        cost: entry.fields.cost,
        retailPrice: entry.fields.retail_price,
        profitMargin: entry.fields.profit_margin_percent,
        totalOrders: entry.fields.total_orders,
        // returnRate: entry.fields.return_rate_percent, // Not in current Product type
        supplierReliability: entry.fields.supplier_reliability_score,
        // avgSalePrice: entry.fields.avg_sale_price, // Not in current Product type
        revenue: entry.fields.total_revenue,
        // score: entry.metadata?.score || 0 // Not in current Product type
        imageUrl: 'https://placehold.co/300x200.png', // Placeholder as API doesn't provide it
        description: entry.fields.name ? `Details for ${entry.fields.name}` : 'Product description placeholder.', // Placeholder
      })) || [];
      
      setDisplayedProducts(productsFromApi);
      toast({ 
        title: "Products Loaded", 
        description: `${productsFromApi.length} products found.`,
        variant: "default"
      });

    } catch (error: any) {
      console.error("API call failed:", error);
      toast({
        variant: "destructive",
        title: "API Error",
        description: error.message || 'An unknown error occurred while fetching products.',
      });
      setDisplayedProducts(mockProducts.slice(0, 10)); // Fallback to mock products on error
    } finally {
      setIsLoading(false);
    }
  }, [searchTerm, aiQueryData, toast]);

  // Initial load and when AI query data changes
  useEffect(() => {
    performSearchAndFilter();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [aiQueryData]); // We only want this to run when aiQueryData changes, or on initial load. performSearchAndFilter has its own deps.

  const handleSearch = async (query: string) => {
    setSearchTerm(query); // Store raw search term
    setIsLoading(true);

    if (query.trim() === '') {
      setAiQueryData(null); // Clear AI query if search is empty, triggers performSearchAndFilter with default
      // setIsLoading(false) is handled by performSearchAndFilter's finally block
      return;
    }

    // Directly set aiQueryData with the raw search query.
    // This will trigger the useEffect for performSearchAndFilter.
    console.log(`Bypassing AI flow. Using raw query for aiQueryData: ${query}`);
    toast({
      title: "Search Initiated",
      description: `Using your query: ${query}`,
    });
    // The 'preference' part of aiQueryData might not be strictly necessary now,
    // but we keep the structure for consistency with the aiQueryData state type.
    setAiQueryData({ query: query, preference: 'INCLUDE' }); 

    // setIsLoading(false) will be handled by performSearchAndFilter's finally block
  };

  return (
    <div className="flex flex-col lg:flex-row h-[calc(100vh-theme(spacing.14))]">
      {/* Desktop Filter Panel */}
      <aside className="hidden lg:block w-72 p-4 border-r overflow-y-auto bg-card">
        <h2 className="text-xl font-semibold mb-4">Filters</h2>
        <FiltersPanelContent filters={filters} onFiltersChange={setFilters} />
        <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
          <p className="text-sm text-yellow-800">
            <strong>Note:</strong> Filters are not yet connected to the API. Use natural language in search instead (e.g., "dresses under $50").
          </p>
        </div>
      </aside>

      {/* Mobile Filter Trigger and Sheet */}
      <div className="lg:hidden p-4 border-b">
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="outline" className="w-full">
              <Filter className="mr-2 h-4 w-4" />
              Show Filters
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-[300px] sm:w-[400px] p-0">
            <SheetHeader className="p-4 border-b">
              <SheetTitle>Filters</SheetTitle>
            </SheetHeader>
            <div className="p-4 overflow-y-auto">
              <FiltersPanelContent filters={filters} onFiltersChange={setFilters} />
              <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                <p className="text-sm text-yellow-800">
                  <strong>Note:</strong> Filters are not yet connected to the API. Use natural language in search instead.
                </p>
              </div>
            </div>
          </SheetContent>
        </Sheet>
      </div>

      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="p-4 md:p-6 border-b">
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
          <div className="mt-2 text-sm text-gray-600">
            Try: "products under $5", "dresses with high profit margin", "accessories from reliable suppliers"
          </div>
        </div>
        <div className="flex-1 overflow-y-auto p-4 md:p-6">
          {isLoading ? (
            <div className="flex justify-center items-center h-full">
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                <p className="text-lg">Loading products...</p>
              </div>
            </div>
          ) : (
            <ResultsList products={displayedProducts} />
          )}
        </div>
      </div>
    </div>
  );
}
