<%namespace name="paginate" file="/paginate.mako"/>
<%
labels = {
    'draft': 'warning',
    'published': 'success',
    'refused': 'danger',
}
pager = request.pagers['articles']
%>\
% if pager.total:
<p>
    % if pager.pages > 1:
    ${translate('article from {0} to {1} on {2}').format(pager.first_item, pager.last_item, pager.total)}
    % else:
    ${pluralize('{0} article', '{0} articles', pager.total).format(pager.total)}
    % endif
    <a class="btn btn-default btn-xs pull-right" href="${request.route_path('articles.search', _query=dict(csv=1))}" title="${translate('Download CSV')}"><i class="glyphicon glyphicon-list"> </i></a>
</p>
<table class="table table-bordered">
    <tbody>
    % for article in pager:
        <tr>
            <td>
                <a href="${request.route_path('articles.visual', article=article.id)}" title="${translate('View article "{0}"').format(article.title)}">#${article.id}</a>
            </td>
            <td>
                <a href="${request.route_path('articles.visual', article=article.id)}" title="${translate('View article "{0}"').format(article.title)}">${article.title}</a>
            </td>
            <td>
                ${translate(article.status.capitalize())}
            </td>
        % if has_permission('articles.modify'):
            <td class="text-right">
                <a class="btn btn-default btn-xs" href="${request.route_path('articles.modify', article=article.id)}" title="${translate('Edit article {0}').format(article.title)}"><i class="glyphicon glyphicon-edit"> </i></a>
            % if has_permission('articles.delete'):
                <a class="btn btn-default btn-xs" href="${request.route_path('articles.delete', article=article.id)}" title="${translate('Delete article {0}').format(article.title)}"><i class="glyphicon glyphicon-trash"> </i></a>
            % endif>
            </td>
        % endif
        </tr>
    % endfor
    </tbody>
    <thead>
        <th>
            <a class="partial-link" href="${pager.link(sort='id', order='toggle')}" title="${translate('Ordering using this column')}">
                <span class="${pager.header_class('id')}"></span>
                ${translate('Id')}
            </a>
        </th>
        <th>
            <a class="partial-link" href="${pager.link(sort='title', order='toggle')}" title="${translate('Ordering using this column')}">
                <span class="${pager.header_class('title')}"></span>
                ${translate('Title')}
            </a>
        </th>
        <th>
            <a class="partial-link" href="${pager.link(sort='status', order='toggle')}" title="${translate('Ordering using this column')}">
                <span class="${pager.header_class('status')}"></span>
                ${translate('Status')}
            </a>
        </th>
    % if has_permission('articles.modify'):
        <th class="text-right">${translate('Actions')}</th>
    % endif
    </thead>
</table>
<div class="text-right">
${paginate.render_pages(pager)}
${paginate.render_limit(pager)}
</div>
% else:
<div class="alert alert-info">${translate('No article.')}</div>
% endif
