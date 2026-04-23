import CardDash from "@/components/molecules/CardDash/cardDash";
import ChatWidget from "@/components/molecules/ChatWidget/chatWidget";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

type Product = {
  product_id: string;
  name: string;
  category: string;
};

const API_BASE = "http://localhost:8000";

export default function Home() {

  const [productCount, setProductCount] = useState(0);
  const [products, setProducts] = useState<Product[]>([]);
  const [totalSales, setTotalSales] = useState(0);

  useEffect(() => {
    fetch(`${API_BASE}/order_items/total_revenue`)
      .then((res) => res.json())
      .then((data: { total_revenue: number }) => setTotalSales(data.total_revenue));
    fetch(`${API_BASE}/products/count`)
      .then((res) => res.json())
      .then((data: { total_products: number }) => setProductCount(data.total_products));
    fetch(`${API_BASE}/products/best-selling?limit=10`)
      .then((res) => res.json())
      .then((data: Product[]) => setProducts(data));
  }, []);

  const currentDate = new Date().toString().split(" ").slice(1, 4).join(" ");

  const cleanCategoryName = (category: string) => {
    return category.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
  }

  const navigate = useNavigate();

  return (
    <div className="h-full w-full flex flex-col p-5 gap-7 font-sans">
      <div className="flex flex-col gap-1">
        <h1 className="font-bold text-2xl">Visão geral</h1>
        <p className="font-light text-sm">Tenha uma visão geral da performance da sua loja.</p>
      </div>
      <div className="w-full flex flex-wrap gap-2">
        <CardDash title="Vendas" content={`R$ ${totalSales.toFixed(2)}`} date={currentDate} />
        <CardDash title="Produtos" content={productCount.toString()} date={currentDate} />
      </div>
      <div className="flex flex-col gap-1">
        <h1 className="font-bold text-2xl">Melhores performances</h1>
        <p className="font-light text-sm">Veja os produtos que melhor performam.</p>
      </div>
      <div className="w-full flex flex-col gap-2">
        {products.map((product, index) => (
          <div key={product.product_id} className="border border-gray-300 rounded-lg p-4 hover:bg-gray-100 hover:cursor-pointer hover:shadow-md hover:border-blue-500" onClick={() => navigate(`/products/${product.product_id}`)}>
            <p className="text-xl font-bold text-gray-800">#{index + 1}</p>
            <h2 className="font-bold text-lg">{product.name}</h2>
            <p className="text-gray-600">Categoria: {cleanCategoryName(product.category)}</p>
          </div>
        ))}
      </div>
      <ChatWidget />
    </div>
  )
}
