
"use client";

import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Search as SearchIcon, Loader2 } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string) => void; // Parent's search initiation function
  isLoading: boolean; // To show loading state on button
}

export function SearchBar({ onSearch, isLoading }: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query); // Pass the raw query to the parent's onSearch handler
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <Input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search products (e.g., 'products under $50 with high profit margins')"
        className="flex-grow"
        aria-label="Search products"
      />
      <Button type="submit" variant="warning" disabled={isLoading}>
        {isLoading ? (
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
        ) : (
          <SearchIcon className="mr-2 h-4 w-4" />
        )}
        Search
      </Button>
    </form>
  );
}
