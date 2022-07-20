from wolframclient.language import wl, wlexpr, Global
from wolframclient.evaluation import WolframLanguageSession



def wlBlock(vars_dict: dict, expr):
    R"""
    `Block` function in wolfram language.

    Examples:
    
        >>> wlSess = WolframLanguageSession()
        >>> expr = 'x = -1\nNIntegrate[z^2,{z,x,y}]'
        >>> wlSess.evaluate(wlBlock({'x': None, 'y': 2}, expr))

        this is equivalent to:

        >>> Block[{x, y=2}, x=-1; NIntegrate[z^2,{z,x,y}]]

    Args:
        vars_dict (dict): 
        expr (str): wolfram language code

    Returns:
        expr
    """
    ret = wl.Block(
        wl.List(
            *[wl.Set(getattr(Global, key), value) if value is not None else getattr(Global, key)
              for key, value in vars_dict.items()]
        ),
        wlexpr(expr) if isinstance(expr, str) else expr
    )
    return ret
