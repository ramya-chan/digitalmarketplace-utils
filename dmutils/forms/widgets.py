
from flask import current_app

__all__ = ["DMCheckboxInput", "DMDateInput", "DMRadioInput", "DMTextInput", "DMTextArea", "DMUnitInput"]


def updatedefault(self, other):
    """
    Update the dictionary with the key/value pairs from :other: where the key does not already exist. Returns None.

    >>> d = {'one': 1, 'two': 2, 'three': 3}
    >>> updatedefault(d, {'three': None, 'four': 4})
    >>> d
    {'one': 1, 'two': 2, 'three': 3, 'four': 4}
    """
    for k, v in other.items():
        self.setdefault(k, v)


def getattrs(object, names, *args):
    return {name: getattr(object, name, *args) for name in names}


class WidgetParamsMixin:

    def params(self, field, **kwargs):
        field_params = getattrs(field, self._params, None)
        updatedefault(kwargs, field_params)

        return kwargs

    def __call__(self, field, **kwargs):
        return self.params(field, **kwargs)


class JinjaWidgetMixin:
    def render(self, *args, **kwargs):
        return current_app.jinja_env.get_template(self.__template__).render(*args, **kwargs)


class DMJinjaWidgetBase(JinjaWidgetMixin, WidgetParamsMixin):

    def __init__(self, hide_question=False, **kwargs):
        super().__init__(**kwargs)

        if hide_question:
            self._params.discard("question")

    def __call__(self, field, **kwargs):
        return self.render(self.params(field, **kwargs))


class DMJinjaWidget(DMJinjaWidgetBase):

    def __init__(self, **kwargs):
        # we include common template arguments here to avoid repetition
        self._params = {
            "error",
            "name",
            "hint",
            "question",
            "question_advice",
            "value",
        }


class DMSelectionButtons(DMJinjaWidget):
    __template__ = "toolkit/forms/selection-buttons.html"

    def __init__(self, type=None, **kwargs):
        super().__init__(**kwargs)

        self._params.add("options")

        if type is not None:
            self.type = type

    def params(self, field, **kwargs):
        kwargs.setdefault("type", self.type)
        return super().params(field, **kwargs)


class DMCheckboxInput(DMSelectionButtons):
    type = "checkbox"


class DMDateInput(DMJinjaWidget):
    __template__ = "toolkit/forms/date.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._params.discard("value")

    def __call__(self, field, **kwargs):
        return super().__call__(field, data=field.value, **kwargs)


class DMRadioInput(DMSelectionButtons):
    type = "radio"


class DMTextInput(DMJinjaWidget):
    __template__ = "toolkit/forms/textbox.html"


class DMTextArea(DMTextInput):
    large = True

    def __init__(self, max_length_in_words=None, **kwargs):
        self.max_length_in_words = max_length_in_words

        super().__init__(**kwargs)

    def params(self, field, **kwargs):
        if self.max_length_in_words:
            kwargs.setdefault("max_length_in_words", self.max_length_in_words)
        kwargs.setdefault("large", self.large)
        return super().params(field, **kwargs)


class DMUnitInput(DMTextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._params |= {
            "unit",
            "unit_in_full",
            "unit_position",
        }
