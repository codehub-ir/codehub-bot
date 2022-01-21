from .add_paste import creator as add_paste_creator
from .start_command import creator as start_command_creator
from .share_paste import creator as share_paste_creator
from .change_lang import creator as change_lang_creator

CREATORES = (
    add_paste_creator,
    start_command_creator,
    share_paste_creator,
    change_lang_creator,
)

def get_handlers(model):
    for creator in CREATORES:
        yield creator(model)
