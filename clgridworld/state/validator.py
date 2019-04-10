from clgridworld.state.state import GridWorldState


class TerminalStateValidator:

    @staticmethod
    def is_terminal_state(state: GridWorldState) -> bool:
        return state.is_in_pit() or (state.player_has_key() and state.lock_is_unlocked())