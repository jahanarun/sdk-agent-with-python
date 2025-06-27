from enum import Enum

class StrategyName(Enum):
    SINGLE_CHAT="single_chat"
    GROUP_CHAT = "group_chat"
    INTENT_ROUTER = "intent_router"
    OUT_CRY = "out_cry"