from model.entities.calax import Calax
from model.entities.room import Room

def findRoomInCalaxByPlayerId(player_id: str, calax: Calax) -> None | Room :
    for room in calax.rooms:
        for player in room.players:
            if player.id == player_id:
                return room
    return None