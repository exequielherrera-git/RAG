from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class MantisNote(BaseModel):
    id: Optional[int]
    text: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class MantisTicket(BaseModel):
    id: Any
    summary: str
    description: Optional[str] = ""
    notes: Optional[List[MantisNote]] = []
    project: Optional[dict] = None
    category: Optional[dict] = None
    status: Optional[dict] = None
    resolution: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def canonical_text(self, include_notes: int = 5) -> str:
        """
        Devuelve texto unificado: título + descripción + últimos N comentarios
        """
        parts = []

        # Encabezado con contexto
        if self.project or self.category:
            context = []
            if self.project:
                context.append(f"Proyecto: {self.project.get('name', '')}")
            if self.category:
                context.append(f"Categoría: {self.category.get('name', '')}")
            parts.append(" | ".join(context))

        parts.append(f"Título: {self.summary}")
        parts.append(f"Descripción: {self.description or ''}")

        # Incluir comentarios / notas
        if self.notes:
            last_notes = self.notes[-include_notes:]
            joined_notes = "\n".join([n.text for n in last_notes if n.text])
            parts.append("Notas / Comentarios:")
            parts.append(joined_notes)

        # Estado final (opcional)
        if self.status:
            parts.append(f"Estado actual: {self.status.get('name', '')}")
        if self.resolution:
            parts.append(f"Resolución: {self.resolution.get('name', '')}")

        return "\n".join([p for p in parts if p.strip()])