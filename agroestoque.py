"""AgroEstoque: controle simples de estoque de defensivos agrícolas.

O aplicativo organiza insumos por validade, princípio ativo e lote para reduzir
perdas por vencimento em grandes fazendas e áreas de teste de produtos.
"""

from __future__ import annotations

import json
import tkinter as tk
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from tkinter import messagebox, ttk

DATA_FILE = Path("agroestoque_dados.json")
DATE_FORMAT = "%Y-%m-%d"
WARNING_DAYS = 90


@dataclass
class DefensiveInput:
    """Representa um lote de defensivo armazenado no barracão."""

    product: str
    batch: str
    expiration: str
    active_ingredient: str
    quantity: float
    unit: str
    location: str
    origin: str
    notes: str = ""

    @property
    def expiration_date(self) -> date:
        return datetime.strptime(self.expiration, DATE_FORMAT).date()

    @property
    def days_to_expire(self) -> int:
        return (self.expiration_date - date.today()).days

    @property
    def status(self) -> str:
        days = self.days_to_expire
        if days < 0:
            return "Vencido"
        if days <= WARNING_DAYS:
            return "Atenção"
        return "Em dia"


class AgroEstoqueApp:
    """Interface gráfica para cadastro e consulta de insumos agrícolas."""

    columns = (
        "status",
        "expiration",
        "active_ingredient",
        "batch",
        "product",
        "quantity",
        "location",
        "origin",
    )

    labels = {
        "status": "Status",
        "expiration": "Validade",
        "active_ingredient": "Princípio ativo",
        "batch": "Lote",
        "product": "Produto",
        "quantity": "Quantidade",
        "location": "Local",
        "origin": "Origem/uso",
    }

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("AgroEstoque - Controle de Defensivos")
        self.root.geometry("1120x680")
        self.items: list[DefensiveInput] = []
        self._build_layout()
        self._load_data()
        self._refresh_table()

    def _build_layout(self) -> None:
        header = ttk.Label(
            self.root,
            text="AgroEstoque",
            font=("Arial", 22, "bold"),
        )
        header.pack(pady=(16, 4))

        subtitle = ttk.Label(
            self.root,
            text=(
                "Organize defensivos por lote, validade e princípio ativo "
                "para evitar perdas no fim da safra."
            ),
        )
        subtitle.pack(pady=(0, 12))

        form = ttk.LabelFrame(self.root, text="Cadastrar insumo")
        form.pack(fill="x", padx=16, pady=8)

        self.entries: dict[str, tk.Entry | ttk.Combobox] = {}
        fields = [
            ("product", "Produto comercial"),
            ("batch", "Lote"),
            ("expiration", "Validade (AAAA-MM-DD)"),
            ("active_ingredient", "Princípio ativo"),
            ("quantity", "Quantidade"),
            ("unit", "Unidade"),
            ("location", "Local no barracão"),
            ("origin", "Origem/uso"),
        ]

        for index, (key, label) in enumerate(fields):
            row = index // 4
            column = (index % 4) * 2
            ttk.Label(form, text=label).grid(row=row, column=column, sticky="w", padx=8, pady=6)
            if key == "unit":
                entry: tk.Entry | ttk.Combobox = ttk.Combobox(
                    form,
                    values=("L", "kg", "galão", "saco", "un"),
                    width=18,
                )
                entry.set("L")
            elif key == "origin":
                entry = ttk.Combobox(
                    form,
                    values=("Safra", "Teste de campo", "Sobra", "Devolução", "Outro"),
                    width=18,
                )
                entry.set("Safra")
            else:
                entry = ttk.Entry(form, width=22)
            entry.grid(row=row, column=column + 1, sticky="ew", padx=8, pady=6)
            self.entries[key] = entry

        ttk.Label(form, text="Observações").grid(row=2, column=0, sticky="w", padx=8, pady=6)
        self.notes = ttk.Entry(form, width=80)
        self.notes.grid(row=2, column=1, columnspan=5, sticky="ew", padx=8, pady=6)

        actions = ttk.Frame(form)
        actions.grid(row=2, column=6, columnspan=2, sticky="e", padx=8, pady=6)
        ttk.Button(actions, text="Adicionar", command=self._add_item).pack(side="left", padx=4)
        ttk.Button(actions, text="Limpar", command=self._clear_form).pack(side="left", padx=4)

        for column in range(8):
            form.columnconfigure(column, weight=1)

        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(fill="x", padx=16, pady=(8, 0))
        ttk.Label(filter_frame, text="Buscar por produto, lote, princípio ativo ou local:").pack(side="left")
        self.search = ttk.Entry(filter_frame, width=48)
        self.search.pack(side="left", padx=8)
        self.search.bind("<KeyRelease>", lambda _event: self._refresh_table())
        ttk.Button(filter_frame, text="Remover selecionado", command=self._remove_selected).pack(side="right")

        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=16, pady=12)
        self.table = ttk.Treeview(table_frame, columns=self.columns, show="headings", height=16)
        for column in self.columns:
            self.table.heading(column, text=self.labels[column])
            self.table.column(column, width=120, anchor="w")
        self.table.column("active_ingredient", width=170)
        self.table.column("product", width=170)
        self.table.column("quantity", width=100, anchor="e")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.summary = ttk.Label(self.root, anchor="w")
        self.summary.pack(fill="x", padx=16, pady=(0, 12))

        self.table.tag_configure("expired", background="#ffd6d6")
        self.table.tag_configure("warning", background="#fff1bf")
        self.table.tag_configure("ok", background="#dff5df")

    def _add_item(self) -> None:
        try:
            item = DefensiveInput(
                product=self._entry_value("product"),
                batch=self._entry_value("batch"),
                expiration=self._validate_date(self._entry_value("expiration")),
                active_ingredient=self._entry_value("active_ingredient"),
                quantity=self._validate_quantity(self._entry_value("quantity")),
                unit=self._entry_value("unit"),
                location=self._entry_value("location"),
                origin=self._entry_value("origin"),
                notes=self.notes.get().strip(),
            )
        except ValueError as error:
            messagebox.showerror("Cadastro incompleto", str(error))
            return

        self.items.append(item)
        self._save_data()
        self._clear_form()
        self._refresh_table()

    def _entry_value(self, key: str) -> str:
        value = self.entries[key].get().strip()
        if not value:
            raise ValueError("Preencha todos os campos obrigatórios antes de adicionar o insumo.")
        return value

    def _validate_date(self, value: str) -> str:
        try:
            datetime.strptime(value, DATE_FORMAT)
        except ValueError as exc:
            raise ValueError("Informe a validade no formato AAAA-MM-DD, por exemplo 2026-12-31.") from exc
        return value

    def _validate_quantity(self, value: str) -> float:
        normalized = value.replace(",", ".")
        try:
            quantity = float(normalized)
        except ValueError as exc:
            raise ValueError("Informe a quantidade usando apenas números.") from exc
        if quantity <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        return quantity

    def _clear_form(self) -> None:
        for key, entry in self.entries.items():
            if isinstance(entry, ttk.Combobox):
                entry.set("L" if key == "unit" else "Safra")
            else:
                entry.delete(0, tk.END)
        self.notes.delete(0, tk.END)

    def _remove_selected(self) -> None:
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Remover insumo", "Selecione um insumo para remover.")
            return
        indexes = sorted((int(item_id) for item_id in selected), reverse=True)
        for index in indexes:
            del self.items[index]
        self._save_data()
        self._refresh_table()

    def _refresh_table(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)

        query = self.search.get().strip().lower() if hasattr(self, "search") else ""
        sorted_items = sorted(
            enumerate(self.items),
            key=lambda pair: (
                pair[1].expiration_date,
                pair[1].active_ingredient.lower(),
                pair[1].batch.lower(),
            ),
        )

        visible_count = 0
        expired_count = 0
        warning_count = 0
        for original_index, item in sorted_items:
            searchable = " ".join(
                [item.product, item.batch, item.active_ingredient, item.location, item.origin]
            ).lower()
            if query and query not in searchable:
                continue

            tag = "ok"
            if item.status == "Vencido":
                tag = "expired"
                expired_count += 1
            elif item.status == "Atenção":
                tag = "warning"
                warning_count += 1

            self.table.insert(
                "",
                tk.END,
                iid=str(original_index),
                values=(
                    item.status,
                    item.expiration,
                    item.active_ingredient,
                    item.batch,
                    item.product,
                    f"{item.quantity:g} {item.unit}",
                    item.location,
                    item.origin,
                ),
                tags=(tag,),
            )
            visible_count += 1

        self.summary.config(
            text=(
                f"{visible_count} itens exibidos | {expired_count} vencidos | "
                f"{warning_count} vencem em até {WARNING_DAYS} dias"
            )
        )

    def _load_data(self) -> None:
        if not DATA_FILE.exists():
            return
        try:
            raw_items = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            self.items = [DefensiveInput(**item) for item in raw_items]
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            messagebox.showwarning(
                "Dados não carregados",
                f"Não foi possível ler {DATA_FILE.name}: {exc}",
            )
            self.items = []

    def _save_data(self) -> None:
        DATA_FILE.write_text(
            json.dumps([asdict(item) for item in self.items], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def main() -> None:
    root = tk.Tk()
    AgroEstoqueApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
