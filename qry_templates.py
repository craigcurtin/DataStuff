# set up some templates ... look at jinja templates for complex queries ... very helpful!
# https://engineeringfordatascience.com/posts/python_string_formatting_for_data_science/


simple_sql_queries = {
    'page':
'''SELECT   * 
   FROM Person.Person
   ORDER BY BusinessEntityID
   OFFSET (@PageNo - 1) * @RowCountPerPage ROWS
   FETCH NEXT @RowCountPerPage ROWS ONLY
   GO ''',
    'backorders':   '''SELECT TOP (1000) *  FROM [controlTower].[qryBackorders]''',
    'foo':  'SELECT TOP (10) *  FROM [controlTower].[qryLoadRouteListStatus]',
    'bar':  'SELECT TOP ({_max_records}) *  FROM {{table}}'
}

jinja_sql_queries = {
'foo': '''
SELECT
    date
    {%- for product in target_products %}
    , SUM(CASE WHEN product_name = '{{asset_classes}}' THEN order_value END) AS sum_{{asset_classes}}_value
    {%- endfor %}
FROM orders
{% if cities_filter -%}
WHERE
    {%- for city in cities %}
    city = '{{city}}'
    {% if not loop.last -%}
    OR
    {%- endif -%}
    {%- endfor %}
{% endif -%}
GROUP BY date''',

'bar': '''
SELECT
    date
    {%- for asset in asset_classes %}
    , SUM(CASE WHEN product_name = '{{asset_classes}}' THEN order_value END) AS sum_{{asset_classes}}_value
    {%- endfor %}
FROM orders
{% if cities_filter -%}
WHERE
    {%- for city in cities %}
    city = '{{city}}'
    {% if not loop.last -%}
    OR
    {%- endif -%}
    {%- endfor %}
{% endif -%}
GROUP BY date
''',
}
