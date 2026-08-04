import frappe
import requests
import json


FIELD_DESCRIPTIONS = {
    "claim_number": "номер претензии (как в тексте, без изменений)",
    "claim_date": "дата претензии, в любом формате, как написано в тексте",
    "contract_ref": "номер договора/контракта",
    "amendment_ref": "номер допсоглашения",
    "amount_line": "сумма претензии — сырая строка из текста, включая валюту, без пересчёта",
    "clause_refs": "пункты договора, упомянутые в претензии (через запятую)",
}


@frappe.whitelist()
def extract_fields_via_llm(text, missing_fields):
    """LLM-fallback извлечение полей претензии, не покрытых regex-слоем.
    Возвращает {"success": True, "fields": {...}} либо {"success": False, "error": "..."}.
    """
    api_key = frappe.conf.get("deepseek_api_key")
    if not api_key:
        return {"success": False, "error": "DeepSeek API key не настроен (site_config.json)"}

    if isinstance(missing_fields, str):
        fields_list = [f.strip() for f in missing_fields.split(",") if f.strip()]
    else:
        fields_list = list(missing_fields)

    if not fields_list:
        return {"success": True, "fields": {}}

    fields_prompt = "\n".join(f"- {f}: {FIELD_DESCRIPTIONS.get(f, f)}" for f in fields_list)

    prompt = (
        "Извлеки из текста претензии перечисленные поля. Ответь ТОЛЬКО JSON-объектом "
        "без пояснений и markdown-разметки, ключи — точные fieldname из списка. "
        f"Если поле не найдено в тексте — не включай его в JSON (не пиши null).\n\nПоля:\n{fields_prompt}\n\n"
        f"Текст претензии:\n{text[:8000]}"
    )

    try:
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_tokens": 800,
            },
            timeout=30,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        fields = json.loads(content)
        fields = {k: v for k, v in fields.items() if v}
    except Exception as e:
        frappe.log_error(f"LLM extraction failed: {e}", "Claim PDF LLM Fallback")
        return {"success": False, "error": str(e)}

    return {"success": True, "fields": fields}
