import { Button } from "@/components/atoms/Button/button";
import { Card, CardContent, CardTitle } from "@/components/atoms/card";
import { useNavigate } from "react-router-dom";

type CardProductsProps = {
    name: string;
    category: string;
    product_id: string;
    imageUrl: string;   
}



export default function CardProducts({ name, category, product_id, imageUrl }: CardProductsProps) {
    const navigate = useNavigate();

    return (
        <Card className="flex flex-row items-center justify-between w-full shadow-sm hover:shadow-md hover:shadow-primary/50 transition-shadow duration-300">
            <CardContent className="flex flex-row gap-4 items-center justify-start">
                <img src={imageUrl} alt={name} className="w-12 h-12 rounded-sm object-cover" />
                <CardTitle>{name}</CardTitle>
                <p className="font-light text-md">{category}</p>
            </CardContent>
            <CardContent>
                <Button variant="outline" size="sm" onClick={() => navigate(`/products/${product_id}`)}>
                    Ver Detalhes
                </Button>
            </CardContent>
        </Card>
    )
}