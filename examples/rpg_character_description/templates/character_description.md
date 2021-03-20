# Character Description: {{ info["player_supplied"]["Character Name"] }}

{{ info["player_supplied"]["Character Name"] }} is a {{ info["player_supplied"]["Character Race"] }} {{ info["player_supplied"]["Character Class"] }} from {{ info["dm_supplied"]["Character Origin City"] }}.

He lived through {{ info["dm_supplied"]["Calamity"] }}

{%- if info["player_supplied"]["Character Brothers"] %}

He has {{ info["player_supplied"]["Character Brothers"]|length }} brothers:

{% for brother in info["player_supplied"]["Character Brothers"] -%}
- {{ brother }}
{% endfor -%}
{%- else %}

He is an only child.
{% endif %}
