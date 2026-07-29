# trade_claims/trade_claims/api/llm_extraction.py
#
# LLM-fallback извлечение полей претензии из PDF (раздел 14.2 ТЗ v6).
# Используется, когда детерминированный regex/anchor-слой (Client Script
# "Claim PDF Extraction Buttons") не нашёл значение для одного или
# нескольких полей.
#
# ВАЖНО: этот код НЕ может жить как Server Script — safe_exec-песочница
# Frappe блокирует прямой сетевой доступ (requests не проброшен в globals,
# frappe.integrations.utils.make_post_request внутри тоже не работает —
# проверено эмпирически на сервере: 'NoneType' object is not callable).
# Поэтому вызов внешнего LLM API вынесен в обычный код приложения, который
# исполняется без ограничений safe_exec.

import json

import frappe
import requests


@frappe.whitelist()
def extract_fields_via_llm(text: str, missing_fields):
	"""
	Fallback-извлечение полей претензии через LLM (DeepSeek или любой
	OpenAI-совместимый эндпоинт), настроенный в LLM Settings.

	Args:
		text: полный текст письма (реконструированный из PDF на клиенте).
		missing_fields: список (или строка через запятую) кодов полей,
			которые не удалось найти регулярными выражениями. Ожидаемые
			коды: claim_number, claim_date, contract_ref, amendment_ref,
			amount_line, clause_refs.

	Returns:
		{"success": bool, "fields": {code: value_or_None, ...}, "error": str|None}
	"""
	settings = frappe.get_single("LLM Settings")
	if not settings.enabled:
		return {"success": False, "error": "LLM fallback отключён в LLM Settings", "fields": {}}

	if isinstance(missing_fields, str):
		missing_list = [f.strip() for f in missing_fields.split(",") if f.strip()]
	else:
		missing_list = [str(f).strip() for f in (missing_fields or []) if str(f).strip()]

	if not missing_list:
		return {"success": True, "fields": {}, "error": None}

	if not settings.api_base_url or not settings.model:
		return {"success": False, "error": "В LLM Settings не заполнен api_base_url или model", "fields": {}}

	api_key = settings.get_password("api_key")
	if not api_key:
		return {"success": False, "error": "В LLM Settings не задан api_key", "fields": {}}

	prompt = (settings.prompt_template or "{text}\n\nМissing: {missing_fields}") \
		.replace("{text}", text or "") \
		.replace("{missing_fields}", ", ".join(missing_list))

	url = settings.api_base_url.rstrip("/") + "/chat/completions"
	payload = {
		"model": settings.model,
		"messages": [{"role": "user", "content": prompt}],
		"temperature": 0,
		"max_tokens": 600,
	}

	try:
		resp = requests.post(
			url,
			headers={
				"Authorization": f"Bearer {api_key}",
				"Content-Type": "application/json",
			},
			json=payload,
			timeout=30,
		)
		resp.raise_for_status()
		content = resp.json()["choices"][0]["message"]["content"]
	except Exception as e:
		frappe.log_error(title="LLM PDF Extraction failed", message=frappe.get_traceback())
		return {"success": False, "error": str(e), "fields": {}}

	# Модель иногда оборачивает JSON в ```json ... ``` — убираем перед парсингом
	cleaned = content.strip()
	if cleaned.startswith("```"):
		cleaned = cleaned.strip("`")
		if cleaned[:4].lower() == "json":
			cleaned = cleaned[4:]
		cleaned = cleaned.strip()

	try:
		parsed = json.loads(cleaned)
	except Exception:
		return {
			"success": False,
			"error": "LLM вернул невалидный JSON: " + content[:300],
			"fields": {},
		}

	if not isinstance(parsed, dict):
		return {"success": False, "error": "LLM вернул не объект JSON", "fields": {}}

	# Оставляем только запрошенные поля, отбрасываем прочее
	fields = {k: v for k, v in parsed.items() if k in missing_list and v not in (None, "", "null")}
	return {"success": True, "fields": fields, "error": None}
