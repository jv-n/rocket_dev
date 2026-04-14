import { useEffect, useState } from "react";
import { Button } from "@/components/atoms/Button/button";
import { Input } from "@/components/atoms/input";
import CardProducts from "@/components/molecules/CardProducts/cardproducts";
import Product from "../Product";
import ProductDialog from "@/components/molecules/ProductDialog/productDialog";

const API_BASE = "http://localhost:8000";
const PAGE_SIZE = 10;

type Product = {
  product_id: string;
  name: string;
  category: string;
};

type ImageCategory = {
  category_name: string;
  image_url: string;
};

export default function ListProducts() {

  const cleanCategoryName = (category: string) => {
    return category.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
  }

  const [searchQuery, setSearchQuery] = useState("");
  const [activeQuery, setActiveQuery] = useState("");
  const [products, setProducts] = useState<Product[]>([]);
  const [imageMap, setImageMap] = useState<Record<string, string>>({});
  const [skip, setSkip] = useState(0);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/image_categories/`)
      .then((res) => res.json())
      .then((data: ImageCategory[]) => {
        const map = Object.fromEntries(data.map((ic) => [ic.category_name, ic.image_url]));
        setImageMap(map);
      });
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      setActiveQuery(searchQuery);
      setSkip(0);
    }, 300);
    return () => clearTimeout(timer);
  }, [searchQuery]);

  useEffect(() => {
    async function fetchProducts() {
      setLoading(true);
      try {
        const url = activeQuery.trim()
          ? `${API_BASE}/products/search/?query=${encodeURIComponent(activeQuery)}&skip=${skip}&limit=${PAGE_SIZE}`
          : `${API_BASE}/products/?skip=${skip}&limit=${PAGE_SIZE}`;
        const res = await fetch(url);
        const data: Product[] = await res.json();
        setProducts((prev) => skip === 0 ? data : [...prev, ...data]);
        setHasMore(data.length === PAGE_SIZE);
      } finally {
        setLoading(false);
      }
    }
    fetchProducts();
  }, [skip, activeQuery]);

  return (
    <div className="h-full w-full flex flex-col p-5 gap-7 font-sans">
      <div className="flex flex-row justify-between items-center">
        <div className="flex flex-col gap-1">
          <h1 className="font-bold text-2xl">Todos os produtos</h1>
          <p className="font-light text-sm">Listagem de todos os produtos do catálogo.</p>
        </div>
        <ProductDialog />
      </div>
      
      <Input
        placeholder="Buscar produtos..."
        className="w-full max-w-sm"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />

      <div className="w-full flex flex-col gap-2">
        {products.map((product) => (
          <CardProducts
            key={product.product_id}
            name={product.name}
            category={cleanCategoryName(product.category)}
            product_id={product.product_id}
            imageUrl={imageMap[product.category] ?? "https://via.placeholder.com/150"}
          />
        ))}
        {loading && <p className="text-sm text-muted-foreground text-center">Carregando...</p>}
        {!loading && hasMore && (
          <Button variant="outline" onClick={() => setSkip((prev) => prev + PAGE_SIZE)}>
            Carregar mais
          </Button>
        )}
        {!loading && !hasMore && products.length > 0 && (
          <p className="text-sm text-muted-foreground text-center">Todos os produtos foram carregados.</p>
        )}
      </div>
    </div>
  )
}