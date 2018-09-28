
import mock
import pytest

import dmutils.forms.fields
import dmutils.forms.mixins
import dmutils.forms.widgets

import wtforms


def get_render_context(widget):
    call = widget.render.call_args
    return dict(call[0][1], **call[1])


@pytest.fixture(autouse=True)
def render():
    patch = mock.patch("dmutils.forms.widgets.DMJinjaWidgetBase.render", autospec=True)
    yield patch.start()
    patch.stop()


@pytest.fixture(params=dmutils.forms.widgets.__all__)
def widget_class(request):
    return getattr(dmutils.forms.widgets, request.param)


@pytest.fixture
def widget(widget_class):
    return widget_class()


@pytest.fixture
def field():
    return mock.Mock(
        spec=[
            "name",
            "question",
            "question_advice",
            "hint",
            "error",
            "value",
            "options",
            "unit",
            "unit_in_full",
            "unit_position",
        ]
    )


def test_calling_widget_calls_template_render(widget, field):
    widget(field)
    assert widget.render.called


def test_template_context_is_populated_from_field(widget):
    field = mock.Mock()  # use a blank mock to collect all attributes
    context = widget.params(field)
    widget(field)
    for k in context:
        if context[k] is not None:
            continue
        assert k in dir(field)
        assert k in get_render_context(widget)


def test_template_context_includes_hint(widget, field):
    field.hint = "Hint text."
    assert widget.params(field)["hint"] == "Hint text."


def test_template_context_includes_question_advice(widget, field):
    field.question_advice = "Advice text."
    assert widget.params(field)["question_advice"] == "Advice text."


class TestDMTextArea:
    @pytest.fixture()
    def widget_class(self):
        return dmutils.forms.widgets.DMTextArea

    def test_dm_text_area_sends_large_is_true_to_template(self, widget, field):
        assert widget.params(field)["large"] is True

    @pytest.mark.parametrize("max_length_in_words", (1, 45, 100))
    def test_dm_text_area_can_send_max_length_in_words_to_template(self, widget_class, max_length_in_words, field):
        widget = widget_class()
        assert "max_length_in_words" not in widget.params(field)

        widget = widget_class(max_length_in_words=max_length_in_words)
        assert widget.params(field)["max_length_in_words"] == max_length_in_words

    def test_dm_text_area_max_words_template_constant_is_instance_variable(self, widget_class):
        widget1 = widget_class(max_length_in_words=mock.sentinel.max_length1)
        widget2 = widget_class(max_length_in_words=mock.sentinel.max_length2)

        widget1(mock.Mock())
        max_length1 = get_render_context(widget1)["max_length_in_words"]

        widget2(mock.Mock())
        max_length2 = get_render_context(widget2)["max_length_in_words"]

        assert max_length1 != max_length2


class TestDMDateInput:
    @pytest.fixture()
    def widget_class(self):
        return dmutils.forms.widgets.DMDateInput

    def test_dm_date_input_does_not_send_value_to_template(self, widget, field):
        widget(field)
        assert "value" not in get_render_context(widget)

    def test_sends_render_argument_data_which_is_equal_to_field_value(self, widget, field):
        widget(field)
        assert get_render_context(widget)["data"] == field.value


class TestDMSelectionButtons:
    @pytest.fixture(params=["DMCheckboxInput", "DMRadioInput"])
    def widget_class(self, request):
        return getattr(dmutils.forms.widgets, request.param)

    def test_dm_selection_buttons_send_type_to_render(self, widget, field):
        widget(field)
        assert "type" in get_render_context(widget)


class TestDMBooleanField:
    @pytest.fixture
    def widget_class(self):
        return dmutils.forms.widgets.DMSelectionButtons

    @pytest.fixture
    def field_class(self):
        return dmutils.forms.fields.DMBooleanField

    def test_default_type_is_checkbox(self, field_class):
        class Form(wtforms.Form):
            field = field_class()

        form = Form()
        form.field()

        assert get_render_context(form.field.widget)["type"] == "checkbox"

    def test_type_can_be_customised(self, widget_class, field_class):
        class Form(wtforms.Form):
            field = field_class(widget=widget_class(type="foo"))

        form = Form()
        form.field()

        assert get_render_context(form.field.widget)["type"] == "foo"


class TestDMRadioField:
    @pytest.fixture
    def widget_class(self):
        return dmutils.forms.widgets.DMRadioInput

    @pytest.fixture
    def field_class(self):
        return dmutils.forms.fields.DMRadioField

    def test_default_type_is_radio(self, field_class):
        class Form(wtforms.Form):
            field = field_class()

        form = Form()
        form.field()

        assert get_render_context(form.field.widget)["type"] == "radio"

    def test_type_can_be_customised(self, widget_class, field_class):
        class Form(wtforms.Form):
            field = field_class(widget=widget_class(type="foo"))

        form = Form()
        form.field()

        assert get_render_context(form.field.widget)["type"] == "foo"
