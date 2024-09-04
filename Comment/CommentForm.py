from typing import List


# класс-форма для валидации комментария пока только по длине
class CommentCreateForm:
    def __init__(self,  comment: str):
        self.errors: List = []
        self.comment: str = comment

    async def is_valid(self):
        if len(self.comment) > 500:
            self.errors.append('Превышена длина комментария, максимальная длина одного сообщения - 500 символов')

        if not self.errors:
            return True

        return False