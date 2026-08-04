import frappe
import requests
import json


@frappe.whitelist()
def extract_fields_llm(text, missing_fields):
    """LLM-fallback извлечение полей претензии, не покрытых regex-слоем."""
    api_key = frappe.conf.get("deepseek_api_key")
    if not api_key:
        frappe.throw("DeepSeek API key не настроен (site_config.json: deepseek_api_key)")

    if isinstance(missing_fields, str):
        missing_fields = json.loads(missing_fields)

    field_descriptions = {
        "claim_number": "номер претензии",
        "claim_date": "дата претензии (формат YYYY-MM-DD)",
        "amount": "сумма претензии (число, без пробелов и валюты)",
        "currency": "код валюты (USD/RUB/KZT и т.п.)",
        "contract_ref": "номер договора",
        "amendment_ref": "номер допсоглашения",
        "clause_refs": "пункты договора, упомянутые в претензии",
    }
    fields_prompt = "\n".join(f"- {f}: {field_descriptions.get(f, f)}" for f in missing_fields)

    prompt = (
        "Извлеки из текста претензии перечисленные поля. Ответь ТОЛЬКО JSON-объектом "
        "без пояснений и markdown-разметки, ключи — точные fieldname из списка. "
        f"Если поле не найдено — null.\n\nПоля:\n{fields_prompt}\n\nТекст претензии:\n{text[:8000]}"
    )

    try:
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0, "max_tokens": 800},
            timeout=30,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        result = json.loads(content)
    except Exception as e:
        frappe.log_error(f"LLM extraction failed: {e}", "Claim PDF LLM Fallback")
        frappe.throw(f"Ошибка обращения к LLM: {e}")

    return result
