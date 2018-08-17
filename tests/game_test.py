from app import app
from models import GameModel


def test_game():
    a = GameModel.find_by_game_id(57509)

    assert a.game_id == 57509