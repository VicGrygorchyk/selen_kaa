
class Component:

    def __init__(self, source):
        self.source = source

    def __getattr__(self, attr):
        try:
            orig_attr = self.source.web_element.__getattribute__(attr)
        except AttributeError:
            try:
                orig_attr = self.source.__getattribute__(attr)
            except AttributeError as exc:
                raise AttributeError(f"Component\'s source has no attribute {attr}.\n{exc}")
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                result = orig_attr(*args, **kwargs)
                # prevent recursion
                if result == self.source:
                    return self
                return result
            return hooked
        return orig_attr
