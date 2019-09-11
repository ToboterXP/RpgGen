from historyGen.events.lifeEvents import *
from historyGen.events.battleEvents import *
from historyGen.events.professionEvents import *
from historyGen.events.itemEvents import *
from historyGen.events.locationEvents import *
from historyGen.events.adminEvents import *


HISTORIC_EVENTS = [
    HEvBirth,
    HEvBattle,
    HEvDiplomaticBattle,
    HEvUnspecifiedDeath,
    HEvChooseProfession,
    HEvImproveAtProfession,
    HEvCreateMasterPiece,
    HEvBuyMasterpiece,
    HEvAcquireLeftItem,
    HEvTravel,
    HEvFoundLocation,
    HEvActiveFoundLocation,
    HEvBecomeAdmin,
    HEvResignAsAdmin,
    HEvAssassinateLeader
    ]
                 
HISTORIC_EVENT_CHANCES = {
    HEvBirth : 0.8,
    HEvBattle : 2,
    HEvDiplomaticBattle : 2,
    HEvUnspecifiedDeath : 1,
    HEvChooseProfession : 1,
    HEvImproveAtProfession : 0.3,
    HEvCreateMasterPiece : 1,
    HEvBuyMasterpiece : 1,
    HEvAcquireLeftItem : 0.5,
    HEvTravel : 0.8,
    HEvFoundLocation: 0.5,
    HEvActiveFoundLocation: 0.5,
    HEvBecomeAdmin: 0.5,
    HEvResignAsAdmin: 0.5,
    HEvAssassinateLeader: 0.5
    }
