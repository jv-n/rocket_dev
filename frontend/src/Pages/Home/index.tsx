import CardDash from "@/components/molecules/CardDash/cardDash";


export default function Home() {
  return (
    <div className="h-full w-full flex flex-col p-5 gap-7 font-sans">
      <div className="flex flex-col gap-1">
        <h1 className="font-bold text-2xl">Visão geral</h1>
        <p className="font-light text-sm">Tenha uma visão geral da performance da sua loja.</p>
      </div>
      <div className="w-full flex flex-wrap gap-2">
        <CardDash title="Vendas" content="R$ 10.000,00" date="2024-02-01" />
        <CardDash title="Produtos" content="150" date="2024-02-01" />
        <CardDash title="Clientes" content="80" date="2024-02-01" />
        <CardDash title="Avaliações" content="4.5/5" date="2024-02-01" />
      </div>
      <div className="flex flex-col gap-1">
        <h1 className="font-bold text-2xl">Melhores performances</h1>
        <p className="font-light text-sm">Veja os produtos que melhor performam.</p>
      </div>

    </div>
  )
}