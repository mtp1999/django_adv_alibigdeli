{% extends "mail_templated/base.tpl" %}

{% block subject %}
account verification
{% endblock %}

{% block html %}
This is an <strong>html</strong> message.
click<a href="http://127.0.0.1:8000/accounts/api/v1/verification/{{ token }}/" target="_blank">here</a> to verify
{% endblock %}