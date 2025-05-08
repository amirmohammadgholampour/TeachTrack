from functools import wraps 

def attending_validations(view_func):
    @wraps(view_func)
    def _wrap_view(request, *args, **kwargs):
        pass 
        return view_func(request, *args, **kwargs)
    return _wrap_view