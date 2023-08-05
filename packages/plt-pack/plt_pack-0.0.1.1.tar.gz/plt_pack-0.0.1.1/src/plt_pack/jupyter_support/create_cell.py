def create_new_jupyter_cell(func_code: str):
    try:
        from IPython.core.getipython import get_ipython
    except ImportError:
        raise ImportError('Could not import IPython.core.getipython.')
    shell = get_ipython()
    payload = dict(
        source='set_next_input',
        text=func_code,
        replace=False,
    )
    shell.payload_manager.write_payload(payload, single=False)
