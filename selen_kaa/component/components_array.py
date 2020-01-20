
class ComponentsArray:

    def __init__(self, source_array):
        self.source_array = source_array

    def __getattr__(self, attr):
        try:
            orig_attr = self.source_array.__getattribute__(attr)
        except AttributeError:
            try:
                orig_attr = self.source_array._lazy_array.__getattribute__(attr)
            except AttributeError as exc:
                raise AttributeError(f"Component\'s array has no attribute {attr}.\n{exc}")
            orig_attr = self.source_array.__getattribute__(attr)
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                result = orig_attr(*args, **kwargs)
                # prevent recursion
                if result == self.source_array:
                    return self
                return result
            return hooked
        return orig_attr
