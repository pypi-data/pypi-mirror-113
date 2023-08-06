def jupyter_code(func_code: str):
    from IPython.display import Code
    return Code(func_code)


def display_code(func_code: str):
    from IPython.display import display
    display(jupyter_code(func_code))

__all__ = ['jupyter_code', 'display_code']
