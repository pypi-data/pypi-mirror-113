try:
    from IPython.display import Code
except ImportError:
    Code = None

def jupyter_code(func_code: str):
    global Code

    if not Code:
        try:
            from IPython.display import Code
        except ImportError:
            raise ImportError('Could not import IPython.display.Code')
    return Code(func_code)


__all__ = ['jupyter_code']
