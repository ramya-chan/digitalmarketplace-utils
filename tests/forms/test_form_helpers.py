
import pytest

from dmutils.forms.helpers import get_errors_from_wtform

import wtforms
from werkzeug import MultiDict


fields = (
    # (name, field),
    ("name", wtforms.fields.StringField(validators=[wtforms.validators.InputRequired()])),
)


@pytest.fixture(params=fields)
def form(request):
    name, field = request.param

    class Form(wtforms.Form):
        pass

    setattr(Form, name, field)

    form = Form(MultiDict())
    assert not form.validate()
    return form


class TestGetErrorsFromWTForm:

    @pytest.fixture
    def errors(self, form):
        return get_errors_from_wtform(form)

    def test_returns_an_iterable_where_each_value_is_a_dictionary(self, errors):
        assert len(errors)
        assert all(isinstance(v, dict) for v in errors.values())

    def test_each_value_has_a_message_string(self, errors):
        assert all(isinstance(v["message"], str) for v in errors.values())

    def test_if_values_are_supplied_output_is_empty(self):
        class Form(wtforms.Form):
            pass

        for name, field in fields:
            setattr(Form, name, field)

        form = Form(MultiDict({
            "name": "Bob Blob",
            "date_of_birth-year": "2012",
            "date_of_birth-month": "05",
            "date_of_birth-day": "04",
            "any_other_details": "true",
            "true": "more details",
        }))

        assert form.validate()
        assert len(get_errors_from_wtform(form)) == 0

    def test_example_output(self):
        class Form(wtforms.Form):
            pass

        for name, field in fields:
            setattr(Form, name, field)

        form = Form(MultiDict())
        assert not form.validate()

        errors = get_errors_from_wtform(form)

        assert (
            errors
            ==
            {
                "name": {
                    "input_name": "name",
                    "question": "Name",
                    "message": "This field is required.",
                },
            }
        )
