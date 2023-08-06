<%namespace name="form" file="/form-tags.mako"/>\
<%inherit file="/site.mako" />\
<%form:form name="article" method="post">
<div class="panel panel-default">
    <div class="panel-heading">
        <h2>${title}</h2>
    </div>

    <div class="panel-body">
        <div class="form-group">
            <label for="title">${translate('Title')}</label>
            <%form:text id="title" name="title" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="status">${translate('Status')}</label>
            <%form:select id="status" name="status" class_="form-control">
                <%form:option value=""></%form:option>
                <%form:option value="draft">${translate('Draft')}</%form:option>
                <%form:option value="published">${translate('Published')}</%form:option>
                <%form:option value="refused">${translate('Refused')}</%form:option>
            </%form:select>
        </div>

        <div class="form-group">
            <label for="text">${translate('Text')}</label>
            <%form:textarea id="text" name="text" rows="10" cols="50" class_="form-control"/>
        </div>
    </div><!-- /.panel-body -->

    <div class="panel-footer text-right">
        <input class="btn btn-primary" type="submit" name="save" value="${translate('Save')}" />
        <a class="btn btn-default" href="${cancel_link}" title="${translate('Cancel')}">${translate('Cancel')}</a>
    </div><!-- /.panel-footer -->
</div><!-- /.panel -->
</%form:form>
