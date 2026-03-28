from datetime import datetime
from uuid import UUID

from loguru import logger

from core.const import DT_FORMAT
from core.types import OpportunityDict


def serialize_dict_for_response(data: dict) -> dict:
    """Конвертирует datetime и UUID в строки для JSON-ответа."""
    result = {}
    for k, v in data.items():
        if isinstance(v, datetime):
            result[k] = v.strftime(DT_FORMAT)
        elif isinstance(v, UUID):
            result[k] = str(v)
        else:
            result[k] = v
    return result


def convert_uuid_to_str_in_data(
    items: list[OpportunityDict] | OpportunityDict,
) -> list[OpportunityDict] | OpportunityDict:
    if items is None:
        raise ValueError("No values in items")
    if isinstance(items, list):
        try:
            for item in items:
                item["id"], item["company_id"], item["created_by"] = (
                    str(item["id"]),
                    str(item["company_id"]),
                    str(item["created_by"]),
                )
        except Exception as e:
            logger.error(e)

    elif isinstance(items, dict):
        try:
            items["id"], items["company_id"], items["created_by"] = (
                str(items["id"]),
                str(items["company_id"]),
                str(items["created_by"]),
            )
        except Exception as e:
            logger.error(e)

    return items
