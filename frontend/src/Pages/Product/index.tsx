import ProductDialogEdit from "@/components/molecules/ProductDialog/productDialogEdit";
import { Button } from "@/components/atoms/Button/button";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import RemoveDialog from "@/components/molecules/RemoveDialog/removeDialog";

type Product = {
  product_id: string;
  name: string;
  category: string;
  height_cm: number | null;
  width_cm: number | null;
  length_cm: number | null;
  weight_grams: number | null;
};

type Product_sales = {
  orders_count: number;
  total_revenue: number;
  total_freight: number;
};

type Product_review = {
  review_id: string;
  order_id: string;
  rating: number;
  comment_title: string | null;
  comment_date: string;
  comment: string | null;
};

type ImageCategory = {
  category_name: string;
  image_url: string;
};

const API_BASE = "http://localhost:8000";

export default function Product() {

  const REVIEWS_PAGE_SIZE = 5;

  const { id } = useParams();
  const [product, setProduct] = useState<Product | null>(null);
  const [sales, setSales] = useState<Product_sales | null>(null);
  const [reviews, setReviews] = useState<Product_review[]>([]);
  const [reviewsSkip, setReviewsSkip] = useState(0);
  const [reviewsLoading, setReviewsLoading] = useState(false);
  const [reviewsHasMore, setReviewsHasMore] = useState(true);
  const [image, setImage] = useState<ImageCategory | null>(null);

  function removeProduct() {
    fetch(`${API_BASE}/products/${id}`, {
      method: "DELETE",
    }).then(() => {
      window.location.href = "/products";
    });
  }

  useEffect(() => {
    async function fetchData() {
      const [productRes, salesRes] = await Promise.all([
        fetch(`${API_BASE}/products/${id}`).then((res) => res.json()),
        fetch(`${API_BASE}/products/${id}/sales`).then((res) => res.json()),
      ]);
      setProduct(productRes);
      setSales(salesRes);
    }
    fetchData();
  }, [id]);

  useEffect(() => {
    async function fetchReviews() {
      setReviewsLoading(true);
      try {
        const data: Product_review[] = await fetch(
          `${API_BASE}/order_reviews/by_product/?product_id=${id}&skip=${reviewsSkip}&limit=${REVIEWS_PAGE_SIZE}`
        ).then((res) => res.json());
        setReviews((prev) => reviewsSkip === 0 ? data : [...prev, ...data]);
        setReviewsHasMore(data.length === REVIEWS_PAGE_SIZE);
      } finally {
        setReviewsLoading(false);
      }
    }
    fetchReviews();
  }, [id, reviewsSkip]);

  useEffect(
    () => {
      if (product) {
        fetch(`${API_BASE}/image_categories/${product.category}`)
          .then((res) => res.json())
          .then((data: ImageCategory) => setImage(data));
      }
    },
    [product]
  )

  return (
    <div className="h-full w-full flex flex-col p-5 gap-7 font-sans">
      <div className="flex flex-col gap-1">
        {product && <h1 className="font-bold text-2xl">{product.name}</h1>}
        <p className="font-light text-sm">Tenha uma visão geral do produto.</p>
      </div>
      <div>
        <div className="flex flex-row justify-between items-center">
          <h2 className="font-semibold text-lg">Detalhes</h2>
            {product && <div className="flex flex-row items-center gap-2">
              <ProductDialogEdit 
              productId={product.product_id} 
              initialName={product.name} 
              initialCategory={product.category} 
              initialWeight={product.weight_grams} 
              initialLength={product.length_cm} 
              initialWidth={product.width_cm} 
              initialHeight={product.height_cm} />
              <RemoveDialog title="Remover produto" description="Tem certeza de que deseja remover este produto?" triggerText="Remover" onConfirm={removeProduct}/>
            </div>}
        </div>
        {product ? (
          <div className="flex flex-row justify-center items-center gap-2 mt-2 p-4 border rounded-md bg-white shadow-sm">
            <img src={image?.image_url || ""} alt={product.name} className="w-32 h-32 object-cover rounded-md" />
            <div className="flex flex-col gap-2 mt-2 w-full p-4">
              <p><span className="font-medium">ID:</span> {product.product_id}</p>
              <p><span className="font-medium">Categoria:</span> {product.category}</p>
              <p><span className="font-medium">Dimensões (cm):</span> {product.length_cm} x {product.width_cm} x {product.height_cm}</p>
              <p><span className="font-medium">Peso (g):</span> {product.weight_grams}</p>
            </div>
          </div>
        ) : (
          <p>Carregando detalhes...</p>
        )}
      </div>
      <div className="flex flex-col gap-1">
        <h2 className="font-semibold text-lg">Performance de vendas</h2>
        {sales ? (
          <div className="flex flex-col justify-center items-start gap-4 mt-2 p-4 border rounded-md bg-white shadow-sm">
            <p><span className="font-medium">Total de Pedidos:</span> {sales.orders_count}</p>
            <p><span className="font-medium">Receita Total:</span> R$ {sales.total_revenue.toFixed(2)}</p>
            <p><span className="font-medium">Frete Total:</span> R$ {sales.total_freight.toFixed(2)}</p>
          </div>
        ) : (
          <p>Carregando performance de vendas...</p>
        )}
      </div>
      <div className="flex flex-col gap-1">
        <h2 className="font-semibold text-lg">Avaliações</h2>
        {reviews.length > 0 ? (
          <div className="flex flex-col gap-4 mt-2">
            {reviews.map((review) => (
              <div key={review.review_id} className="p-4 border rounded-md bg-white shadow-sm">
                <p><span className="font-medium">Pedido ID:</span> {review.order_id}</p>
                <p><span className="font-medium">Data da Avaliação:</span> {new Date(review.comment_date).toLocaleDateString()}</p>
                <p><span className="font-medium">Avaliação:</span> {review.rating} / 5</p>
                <p><span className="font-medium">Título do Comentário:</span> {review.comment_title || "Sem título"}</p>
                {review.comment && <p><span className="font-medium">Comentário:</span> {review.comment}</p>}
              </div>
            ))}
            {reviewsLoading && <p className="text-sm text-muted-foreground text-center">Carregando...</p>}
            {!reviewsLoading && reviewsHasMore && (
              <Button variant="outline" onClick={() => setReviewsSkip((prev) => prev + REVIEWS_PAGE_SIZE)}>
                Carregar mais
              </Button>
            )}
            {!reviewsLoading && !reviewsHasMore && (
              <p className="text-sm text-muted-foreground text-center">Todas as avaliações foram carregadas.</p>
            )}
          </div>
        ) : (
          <p>Nenhuma avaliação encontrada para este produto.</p>
        )}
      </div>
    </div>
  )
}