import { useState } from "react"
import { Button } from "@/components/atoms/Button/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/atoms/dialog"
import { Field, FieldError, FieldGroup } from "@/components/atoms/field"
import { Input } from "@/components/atoms/input"
import { Label } from "@/components/atoms/label"
import { PencilEdit01Icon} from "@hugeicons/core-free-icons"
import { HugeiconsIcon } from "@hugeicons/react"

const API_BASE = "http://localhost:8000";

type FormErrors = { name?: string; category?: string };

type ProductDialogEditProps = {
  productId: string;
  initialName: string;
  initialCategory: string;
  initialWeight?: number | null;
  initialLength?: number | null;
  initialWidth?: number | null;
  initialHeight?: number | null;
};

export default function ProductDialogEdit({ productId, initialName, initialCategory, initialWeight, initialLength, initialWidth, initialHeight }: ProductDialogEditProps) {
  const [open, setOpen] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});
  const [submitting, setSubmitting] = useState(false);

  function handleOpenChange(value: boolean) {
    setOpen(value);
    if (!value) setErrors({});
  }

  async function handleSubmit(e: React.BaseSyntheticEvent) {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const data = new FormData(form);

    const name = (data.get("product_name") as string).trim();
    const category = (data.get("category") as string).trim().replace(/\s+/g, "_").toLowerCase();

    const newErrors: FormErrors = {};
    if (!name) newErrors.name = "Nome é obrigatório.";
    if (!category) newErrors.category = "Categoria é obrigatória.";

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setSubmitting(true);
    try {
      const res = await fetch(`${API_BASE}/products/${productId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          category,
          weight_grams: data.get("weight") ? Number(data.get("weight")) : null,
          length_cm: data.get("length") ? Number(data.get("length")) : null,
          width_cm: data.get("width") ? Number(data.get("width")) : null,
          height_cm: data.get("height") ? Number(data.get("height")) : null,
        }),
      });

      if (!res.ok) throw new Error("Erro ao atualizar produto.");

      form.reset();
      setOpen(false);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <Button variant="default" size="lg">
          <HugeiconsIcon icon={PencilEdit01Icon} className="w-4 h-4" color="#fff" strokeWidth={2} />
          <p>Editar Produto</p>
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-sm">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>Editar Produto</DialogTitle>
            <DialogDescription>
              Preencha os dados do produto modificado. Envie quando estiver pronto.
            </DialogDescription>
          </DialogHeader>
          <FieldGroup className="my-4">
            <Field data-invalid={!!errors.name}>
              <Label htmlFor="product_name">Nome do produto</Label>
              <Input
                id="product_name"
                name="product_name"
                placeholder="Nome do produto"
                defaultValue={initialName}
                onChange={() => setErrors((prev) => ({ ...prev, name: undefined }))}
              />
              <FieldError>{errors.name}</FieldError>
            </Field>
            <Field data-invalid={!!errors.category}>
              <Label htmlFor="category">Categoria</Label>
              <Input
                id="category"
                name="category"
                placeholder="Categoria do produto"
                defaultValue={initialCategory}
                onChange={() => setErrors((prev) => ({ ...prev, category: undefined }))}
              />
              <FieldError>{errors.category}</FieldError>
            </Field>
            <Field className="grid grid-cols-2 gap-4">
              <Label htmlFor="weight">Peso em gramas</Label>
              <Input id="weight" name="weight" type="number" placeholder="g" defaultValue={initialWeight ?? undefined} />
              <Label htmlFor="length">Comprimento</Label>
              <Input id="length" name="length" type="number" placeholder="cm" defaultValue={initialLength ?? undefined} />
              <Label htmlFor="width">Largura</Label>
              <Input id="width" name="width" type="number" placeholder="cm" defaultValue={initialWidth ?? undefined} />
              <Label htmlFor="height">Altura</Label>
              <Input id="height" name="height" type="number" placeholder="cm" defaultValue={initialHeight ?? undefined} />
            </Field>
          </FieldGroup>
          <DialogFooter>
            <DialogClose asChild>
              <Button variant="outline" type="button">Cancelar</Button>
            </DialogClose>
            <Button type="submit" disabled={submitting}>
              {submitting ? "Atualizando..." : "Atualizar Produto"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
