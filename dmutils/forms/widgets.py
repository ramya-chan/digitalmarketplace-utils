
from flask import current_app

__all__ = ["DMCheckboxInput", "DMDateInput", "DMRadioInput", "DMTextInput", "DMTextArea", "DMUnitInput"]


class WidgetParamsMixin:

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)
        self.__params__ = {k for k in dir(self) if not k.startswith("_")}

    def params(self, field, **kwargs):
        params = {}

        for param in self.__params__:
            value = getattr(self, param, None)
            if value is None:
                value = getattr(field, param, None)
            params[param] = value

        params.update(kwargs)

        return params

    def __call__(self, field, **kwargs):
        return self.params(field, **kwargs)


class JinjaWidgetMixin:
    def render(self, *args, **kwargs):
        return current_app.jinja_env.get_template(self.__template__).render(*args, **kwargs)


class DMJinjaWidgetBase(JinjaWidgetMixin, WidgetParamsMixin):

    def __init__(self, hide_question=False, **kwargs):
        super().__init__(**kwargs)

        if hide_question:
            self.__params__.discard("question")

    def __call__(self, field, **kwargs):
        return self.render(self.params(field, **kwargs))


class DMJinjaWidget(DMJinjaWidgetBase):
    # we include common template arguments here to avoid repetition
    error = None
    name = None
    hint = None
    question = None
    question_advice = None
    value = None


class DMSelectionButtons(DMJinjaWidget):
    __template__ = "toolkit/forms/selection-buttons.html"

    type = None
    inline = None
    options = None


class DMCheckboxInput(DMSelectionButtons):
    type = "checkbox"


class DMDateInput(DMJinjaWidget):
    __template__ = "toolkit/forms/date.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__params__.discard("value")

    def __call__(self, field, **kwargs):
        return super().__call__(field, data=field.value, **kwargs)


class DMRadioInput(DMSelectionButtons):
    type = "radio"


class DMTextInput(DMJinjaWidget):
    __template__ = "toolkit/forms/textbox.html"


class DMTextArea(DMTextInput):
    large = True

    def __init__(self, max_length_in_words=None, **kwargs):
        if max_length_in_words:
            self.max_length_in_words = max_length_in_words

        super().__init__(**kwargs)


class DMUnitInput(DMTextInput):
    unit = None
    unit_in_full = None
    unit_position = None
