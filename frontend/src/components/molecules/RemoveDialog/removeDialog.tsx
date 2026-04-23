import { Button } from "@/components/atoms/Button/button";
import {
    Dialog,
    DialogTrigger,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogFooter,
    DialogClose,
  } from "@/components/atoms/dialog"

type RemoveDialogProps = {
    title: string;
    description: string;
    triggerText: string;
    onConfirm: () => void;
}

export default function RemoveDialog({ title, description, triggerText, onConfirm }: RemoveDialogProps) {
    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button variant="destructive" size="lg">
                    {triggerText}
                </Button>
            </DialogTrigger>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>{title}</DialogTitle>
                    <DialogDescription>{description}</DialogDescription>
                </DialogHeader>
                <DialogFooter>
                    <DialogClose asChild>
                        <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded transition-colors duration-300">
                            Cancelar
                        </button>
                    </DialogClose>
                    <button
                        onClick={onConfirm}
                        className="bg-red-500 hover:bg-red-700 text-white px-4 py-2 rounded transition-colors duration-300"
                    >
                        Confirmar
                    </button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}