import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from rag.retriever import TicketRetriever
from rag.utils import setup_logger

logger = setup_logger("generator")

class TicketAnswerGenerator:
    """
    Genero la respuesta usando el LLM
    """

    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-0.5B-Instruct",
        device: str = None, # type: ignore
    ):
        self.device: str = device or ("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Cargando modelo de generación: {model_name} ({self.device})")

        # Cargar tokenizer y modelo
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
        ).to(self.device) # type: ignore
        logger.info(f"Modelo cargado en: {next(self.model.parameters()).device}")
        self.model.eval()

        # Inicializar el retriever FAISS
        self.retriever = TicketRetriever()

    def build_prompt(self, query: str, retrieved_docs: list) -> list:
        """
        Forza al modelo a responder únicamente en base a los tickets recuperados.
        """
        # Construir contexto con los tickets más relevantes
        context_lines = []
        for d in retrieved_docs:
            content = d.get("content") or d.get("text") or ""
            snippet = f"- [Ticket {d.get('ticket_id', 'N/A')}] {content.strip()}"
            context_lines.append(snippet)

        # Limitar longitud del contexto (previene truncamiento de entrada)
        context = "\n".join(context_lines)[:2000]

        system_prompt = (
            "Eres un experto en soporte técnico de un casino. "
            "Tu tarea es responder a las consultas **exclusivamente** usando la información "
            "de los tickets proporcionados a continuación. "
            "La respuesta tiene que ser creada con información contenida en esos tickets"
            "En el caso de no poder tener toda la información necesaria en los tickets, responde: "
            "'No se encontró evidencia suficiente'. "
            "No inventes información ni uses conocimiento fuera de los tickets, pero siempre trata de dar una respuesta basada en los tickets"
        )

        user_prompt = (
            f"--- TICKETS RELEVANTES ---\n"
            f"{context}\n"
            f"--- FIN DE TICKETS ---\n\n"
            f"PREGUNTA DEL USUARIO:\n{query}\n\n"
            "Responde **únicamente** citando la información textual de los tickets. Si algo no se menciona explícitamente, no lo incluyas."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return messages


    def generate_answer(self, query: str, top_k: int = 3, max_new_tokens: int = 200) -> str:
        """
        Recupera contexto y genera una respuesta textual.
        """
        retrieved = self.retriever.search(query, top_k=top_k)
        if not retrieved:
            return "No se encontraron documentos relevantes."

        messages = self.build_prompt(query, retrieved)

        logger.info("Generando respuesta...")
        try:
            inputs = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors="pt",
            ).to(self.device)

            # outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.4,                # más estable
                top_p=0.9,
                repetition_penalty=1.1,
                do_sample=True,                 # mejora la naturalidad
            )
            answer = self.tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True
            ).strip()

            return answer or "No se generó respuesta."

        except Exception as e:
            logger.error(f"Error durante la generación: {e}")
            return f"Error al generar la respuesta: {e}"


if __name__ == "__main__":
    qa = TicketAnswerGenerator()
    query = input("Ingrese su pregunta: ")
    answer = qa.generate_answer(query, top_k=3)
    print("\nRespuesta del asistente:\n")
    print(answer)
