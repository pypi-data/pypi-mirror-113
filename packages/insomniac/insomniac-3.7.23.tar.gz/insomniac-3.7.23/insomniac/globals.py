# These constants can be set by the external UI-layer process, don't change them manually
is_ui_process = False
execution_id = ''
task_id = ''
executable_name = 'insomniac'


def is_insomniac():
    return execution_id == ''
