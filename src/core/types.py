from datetime import datetime
from decimal import Decimal
from typing import Union
from uuid import UUID

from database.dto.opportunity import OpportunityDTO

OpportunityDict = dict[str, Union[str, int, datetime, Decimal, UUID]]
