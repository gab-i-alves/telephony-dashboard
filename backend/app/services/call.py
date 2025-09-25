import httpx
import logging
import asyncio
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from datetime import datetime as dta

from app import schemas
from app.repositories.call import call_repo

logger = logging.getLogger(__name__)

EXTERNAL_API_URL = "http://217.196.61.183:8080/calls"
PAGE_LIMIT = 500

def parse_duration_to_seconds(duration_str: str) -> int:
    """
    Converte 'HH:MM:SS' (str) para segundos (int).
    """
    if not duration_str or not isinstance(duration_str, str):
        return 0
    try:
        h, m, s = map(int, duration_str.split(':'))
        return h * 3600 + m * 60 + s
    except (ValueError, AttributeError):
        return 0

class CallService:
    async def _fetch_page(self, client: httpx.AsyncClient, page: int) -> List[dict]:
        try:
            response = await client.get(
                EXTERNAL_API_URL,
                params={"page": page, "limit": PAGE_LIMIT}
            )
            response.raise_for_status()
            return response.json().get("data", [])
        except httpx.HTTPStatusError as e:
            logger.error(f"Erro ao buscar a página {page}: {e}")
            return []
        
    async def ingest_calls_from_external_api(self, db: Session) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                first_page_response = await client.get(EXTERNAL_API_URL, params={"page": 1, "limit": PAGE_LIMIT})
                first_page_response.raise_for_status()
                
                response_data = first_page_response.json()
                total_records = response_data.get("total", 0)
                
                if total_records == 0:
                    return {"message": "Nenhuma chamada encontrada na API externa."}

                all_calls_raw = response_data.get("data", [])

                total_pages = (total_records + PAGE_LIMIT - 1) // PAGE_LIMIT

                if total_pages > 1:
                    tasks = [self._fetch_page(client, page) for page in range(2, total_pages + 1)]
                    remaining_pages_results = await asyncio.gather(*tasks)
                    for page_result in remaining_pages_results:
                        all_calls_raw.extend(page_result)

                calls_to_create: List[schemas.CallCreate] = []
                failed_count = 0

                for call_data in all_calls_raw:
                    try:
                        start_time_str = call_data.get("data")
                        start_time = dta.strptime(start_time_str, '%Y-%m-%d %H:%M:%S') if start_time_str else None

                        transformed_data = {
                            "external_id": call_data.get("chamada_id"),
                            "start_time": start_time,
                            "end_time": None,
                            "duration": parse_duration_to_seconds(call_data.get("duracao")),
                            "source_number": call_data.get("origem"),
                            "destination_number": call_data.get("destino"),
                            "status_code": call_data.get("sip_code"),
                            "call_status": call_data.get("motivo_desligamento"),
                        }
                        
                        if transformed_data["external_id"] and transformed_data["start_time"]:
                            calls_to_create.append(schemas.CallCreate(**transformed_data))
                        else:
                            failed_count += 1
                    except (ValueError, TypeError) as e:
                        failed_count += 1
                        logger.error(f"Falha ao processar registro: {call_data}. Erro: {e}")

                if calls_to_create:
                    call_repo.bulk_insert_calls(db, calls_in=calls_to_create)

                return {
                    "message": "Ingestão concluída.",
                    "total_de_registros_na_api": total_records,
                    "salvos_com_sucesso": len(calls_to_create),
                    "falhas_de_processamento": failed_count
                }

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"Erro ao comunicar com a API externa: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro inesperado: {str(e)}")

call_service = CallService()