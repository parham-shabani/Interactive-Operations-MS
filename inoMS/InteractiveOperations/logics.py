# *Note: You can group methods that are implemented for a specific purpose into classes with appropriate names.

class TestNameClass:
    @classmethod
    def test_function_name(cls, actor_id: int, actor_type: str, actor_ids: list[int]):
        result = {
            'actor_id': actor_id,
            "actor_type": actor_type,
            "actor_ids": actor_ids
        }
        # ......

        return result


class NameClass:
    pass
