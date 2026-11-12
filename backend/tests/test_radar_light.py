"""Unit and API tests for the low-memory RADAR path. No external API calls."""
import io

from app import create_app
from app.api.radar_light import _filter_topics


SOURCE = (
    "FCC 2022 Direito Civil: impenhorabilidade de bem de família. "
    "FCC 2023 Direito Processual Civil: recurso de agravo de instrumento. "
    "Material resumido para Analista Jurídico da DPE-AM. "
    "São exemplos de subassuntos; não são estatísticas validadas da banca."
)


def test_filter_discards_fabricated_quote():
    result = _filter_topics({
        "topicos": [
            {"disciplina": "Direito Civil", "subassunto": "Bem de família",
             "trecho_evidencia": "impenhorabilidade de bem de família",
             "justificativa": "Há referência documental."},
            {"disciplina": "Direito Civil", "subassunto": "Direito cambial",
             "trecho_evidencia": "cobrança de cheque com avalista",
             "justificativa": "Inventado pelo modelo."},
        ]
    }, SOURCE)
    assert len(result) == 1
    assert result[0]["subassunto"] == "Bem de família"
    assert result[0]["evidencia_conferida"] is True
    assert "probabilidade" not in result[0]


def test_filter_caps_each_discipline_to_five():
    doc = "Direito Civil e Processo Civil: termo de comparação documental."
    rows = [
        {"disciplina": "Direito Civil", "subassunto": "Assunto " + str(i),
         "trecho_evidencia": "termo de comparação documental",
         "justificativa": "Referência"}
        for i in range(12)
    ]
    result = _filter_topics({"topicos": rows}, doc)
    assert len(result) == 5
    assert result[-1]["posicao"] == 5


def test_document_api_is_grounded_and_never_starts_oasis(monkeypatch):
    import app.utils.llm_client as llm_mod

    calls = []

    class DummyClient:
        def chat_json(self, **kwargs):
            calls.append(kwargs)
            return {
                "topicos": [{
                    "disciplina": "Direito Processual Civil",
                    "subassunto": "Agravo de instrumento",
                    "trecho_evidencia": "recurso de agravo de instrumento",
                    "justificativa": "Trecho existente."
                }]
            }

    monkeypatch.setattr(llm_mod, "LLMClient", lambda: DummyClient())
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.post("/api/radar-light/analyze", data={
        "arquivo": (io.BytesIO(SOURCE.encode()), "fcc.md"),
    }, content_type="multipart/form-data")

    assert response.status_code == 200
    result = response.json
    assert result["success"] is True
    assert result["zep"]["estado"] == "nao_solicitado"
    assert len(result["topicos"]) == 1
    assert result["topicos"][0]["evidencia_conferida"]
    assert len(calls) == 1
    status = client.get("/api/radar-light/status")
    assert status.json["oasis_enabled"] is False


def test_api_rejects_unsupported_format_without_model_call():
    app = create_app()
    app.config["TESTING"] = True
    result = app.test_client().post("/api/radar-light/analyze", data={
        "arquivo": (io.BytesIO(SOURCE.encode()), "arquivo.pdf"),
    }, content_type="multipart/form-data")
    assert result.status_code == 415


def test_api_rejects_more_than_64k_without_model_call():
    app = create_app()
    app.config["TESTING"] = True
    result = app.test_client().post("/api/radar-light/analyze", data={
        "arquivo": (io.BytesIO(b"x" * 65537), "arquivo.md"),
    }, content_type="multipart/form-data")
    assert result.status_code == 413
