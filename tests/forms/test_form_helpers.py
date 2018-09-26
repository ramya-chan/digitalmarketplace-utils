
import pytest

from dmutils.forms.helpers import get_errors_from_wtform

from html.parser import HTMLParser
import wtforms
from werkzeug import MultiDict


class IDParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])

    @classmethod
    def parse_ids(cls, string):
        parser = cls()
        parser.feed(string)
        parser.close()
        return parser.ids


class DateForm(wtforms.Form):
    year = wtforms.fields.IntegerField(validators=[wtforms.validators.InputRequired()])
    month = wtforms.fields.IntegerField(validators=[wtforms.validators.InputRequired()])
    day = wtforms.fields.IntegerField(validators=[wtforms.validators.InputRequired()])


fields = (
    # (name, field),
    ("name", wtforms.fields.StringField(validators=[wtforms.validators.InputRequired()])),
    ("date_of_birth", wtforms.fields.FormField(DateForm)),
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

    def test_each_value_has_an_input_name_which_is_the_html_id_for_the_form_element(self, form, errors):
        input_names = set(error["input_name"] for error in errors.values())
        ids = set(IDParser.parse_ids("".join(field() for field in form)))
        assert input_names <= ids

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
                "year": {
                    "input_name": "date_of_birth-year",
                    "question": "Year",
                    "message": "This field is required.",
                },
                "month": {
                    "input_name": "date_of_birth-month",
                    "question": "Month",
                    "message": "This field is required.",
                },
                "day": {
                    "input_name": "date_of_birth-day",
                    "question": "Day",
                    "message": "This field is required.",
                },
            }
        )
