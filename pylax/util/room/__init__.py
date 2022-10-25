from model.entities.pylax import Pylax
from model.entities.room import Room

def findRoomInpylaxByPlayerId(player_id: str, pylax: Pylax) -> None | Room :
    for room in pylax.rooms:
        for player in room.players:
            if player.id == player_id:
                return room
    return None