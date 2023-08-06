<%inherit file="/site.mako" />\
<div class="page-header">
    <h2>${translate('Predicates')}</h2>
</div>

<h3>Enum</h3>
<ul class="list-unstyled">
    <li><a href="${request.route_path('predicates.enum', predicate='value1')}">predicate=value1</a></li>
    <li><a href="${request.route_path('predicates.enum', predicate='value2')}">predicate=value2</a></li>
    <li><a href="${request.route_path('predicates.enum', predicate='value3')}">predicate=value3</a> (invalid)</li>
</ul>

${translate('Current:')} <code>predicate=${request.matchdict.get('predicate')}</code>

<h3>Numeric</h3>
<ul class="list-unstyled">
    <li><a href="${request.route_path('predicates.numeric-1', predicate1='1')}">predicate1=1</a></li>
    <li><a href="${request.route_path('predicates.numeric-1', predicate1='2')}">predicate1=2</a></li>
    <li><a href="${request.route_path('predicates.numeric-1', predicate1='a')}">predicate1=a</a> (invalid)</li>
    <li><a href="${request.route_path('predicates.numeric-2', predicate1='1', predicate2='3')}">predicate1=1, predicate2=3</a></li>
    <li><a href="${request.route_path('predicates.numeric-2', predicate1='2', predicate2='4')}">predicate1=2, predicate2=4</a></li>
    <li><a href="${request.route_path('predicates.numeric-2', predicate1='a', predicate2='3')}">predicate1=a, predicate2=3</a> (invalid)</li>
    <li><a href="${request.route_path('predicates.numeric-2', predicate1='1', predicate2='b')}">predicate1=1, predicate2=b</a> (invalid)</li>
    <li><a href="${request.route_path('predicates.numeric-2', predicate1='a', predicate2='b')}">predicate1=a, predicate2=b</a> (invalid)</li>
</ul>

${translate('Current:')} <code>predicate1=${request.matchdict.get('predicate1')}</code>, <code>predicate2=${request.matchdict.get('predicate2')}</code>
