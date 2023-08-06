<%!
from pyramid_helpers.funcs.articles import build_search_query
%>\
<% route_name = request.matched_route.name if request.matched_route else '' %>\
<%def name="head()">
</%def>\
<!DOCTYPE html>
<html>
<head>
    <title>The Pyramid Web Application Development Framework</title>
    <meta charset="utf-8">

    <!-- jQuery -->
    <script type="text/javascript" src="${request.static_url('pyramid_helpers:static/lib/jquery-2.1.0.min.js')}"></script>

    <!-- Boostrap -->
    <link rel="stylesheet" href="${request.static_url('pyramid_helpers:static/lib/bootstrap-3.3.2-dist/css/bootstrap.min.css')}" type="text/css" media="screen" />
    <script type="text/javascript" src="${request.static_url('pyramid_helpers:static/lib/bootstrap-3.3.2-dist/js/bootstrap.min.js')}"></script>

    <!-- Pyramid Helpers -->
    <link rel="stylesheet" href="${request.static_url('pyramid_helpers:static/css/pyramid-helpers.css')}" type="text/css" media="screen" />
    <script type="text/javascript" src="${request.static_url('pyramid_helpers:static/js/pyramid-helpers.js', version=2014040501)}"></script>

${self.head()}
</head>

<body>
    <header>
        <nav class="navbar navbar-inverse navbar-fixed-top">
            <div class="container">
                <a class="navbar-brand" href="${request.route_path('index')}">Pyramid Helpers</a>
                <ul class="nav navbar-nav">
                    <li${' class="active"' if route_name.startswith('articles.') else '' | n}><a href="${request.route_path('articles.search')}">${translate('Articles')}</a></li>
                    <li${' class="active"' if route_name == 'predicates' else '' | n}><a href="${request.route_path('predicates')}">${translate('Predicates')}</a></li>
                    <li${' class="active"' if route_name == 'validators' else '' | n}><a href="${request.route_path('validators')}">${translate('Validators')}</a></li>
                    <li${' class="active"' if route_name == 'i18n' else '' | n}><a href="${request.route_path('i18n')}">${translate('I18n')}</a></li>
% if authenticated_user is not None:
                    <li${' class="active"' if route_name == 'api-doc' else '' | n}><a href="${request.route_path('api-doc')}">${translate('API Doc')}</a></li>
% endif
                </ul><!-- /.navbar-nav -->
                <div class="nav navbar-nav navbar-right">
% if authenticated_user is None:
                    <a class="btn btn-primary navbar-btn" href="${request.route_path('login')}" title="${translate('Login')}">${translate('login')}</a>
% else:
                    <p class="navbar-text">${authenticated_user.fullname}</p>
    % if has_permission('articles.create'):
                    <a class="btn btn-success navbar-btn" href="${request.route_path('articles.create')}" title="${translate('New article')}">${translate('New article')}</a>
    % endif
                    <a class="btn btn-primary navbar-btn" href="${request.route_path('logout')}" title="${translate('Logout')}">${translate('logout')}</a>
% endif
                </div>
            </div>
        </nav>
    </header>

    <div class="container">
% if not request.exception and route_name not in ('login', 'logout'):
    <% breadcrumb.insert(0, (translate('Home'), request.route_path('index'))) %>\
        <ol class="breadcrumb">
    % for name, url in breadcrumb[:-1]:
            <li><a href="${url}">${name}</a></li>
    % endfor
    <% name, url = breadcrumb[-1] %>
            <li class="active">${name}</li>
        </ol>
% endif
        <section>
${self.body()}
        </section>
    </div><!-- /.container -->

    <footer>
        <div class="text-center">&copy; Copyright 2011-2021 Cyril Lacoux, <a href="http://easter-eggs.com">Easter-eggs</a>.</div>
    </footer>
</body>
</html>
