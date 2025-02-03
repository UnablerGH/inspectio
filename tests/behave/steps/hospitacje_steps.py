from behave import given, when, then
from app import app

@given('aplikacja jest uruchomiona')
def step_impl(context):
    app.testing = True
    context.client = app.test_client()

@when('wysyłam żądanie GET do "{endpoint}"')
def step_impl(context, endpoint):
    context.response = context.client.get(endpoint)

@when('wysyłam żądanie POST do "{endpoint}"')
def step_impl(context, endpoint):
    context.response = context.client.post(endpoint)

@when('wysyłam żądanie POST do "{endpoint}" z danymi:')
def step_impl(context, endpoint):
    payload = context.text.strip()
    context.response = context.client.post(
        endpoint,
        data=payload,
        content_type='application/json'
    )

@then('otrzymuję status {status_code:d}')
def step_impl(context, status_code):
    actual = context.response.status_code
    assert actual == status_code, f"Expected status {status_code} but got {actual}"

@then('odpowiedź zawiera "{text}"')
def step_impl(context, text):
    data = context.response.get_data(as_text=True)
    assert text in data, f"Expected response to contain '{text}', but got: {data}"
