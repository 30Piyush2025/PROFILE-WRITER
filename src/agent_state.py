from typing import TypedDict, List, Optional

class AgentState(TypedDict, total=False):
    request: str
    context: str
    content_type: str
    custom_label: Optional[str]
    num_variations: int
    outputs: List[str]
