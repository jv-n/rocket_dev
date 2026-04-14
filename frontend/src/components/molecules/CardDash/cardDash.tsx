import { Card,
    CardContent,
    CardFooter,
    CardHeader,
    CardTitle,
 } from "@/components/atoms/card";

 type CardDashProps = {
    title: string;
    content: string;
    date: string;
 }

 export default function CardDash({ title, content, date }: CardDashProps) {
    return (
        <Card className="w-[45%] shadow-sm hover:shadow-md hover:shadow-primary/50 transition-shadow duration-300">
            <CardHeader>
                <CardTitle>{title}</CardTitle>
            </CardHeader>
            <CardContent>
                <p className="font-bold text-lg">{content}</p>
            </CardContent>
            <CardFooter className="text-xs color-muted-foreground">
                <p>atualizado em {new Date(date).toLocaleDateString()}</p>
            </CardFooter>
        </Card>
    )
 }