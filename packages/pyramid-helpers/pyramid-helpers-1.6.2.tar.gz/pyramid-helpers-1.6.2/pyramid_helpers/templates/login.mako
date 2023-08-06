<%namespace name="form" file="/form-tags.mako"/>\
<%inherit file="/site.mako" />\
<%form:form name="login_form" action="${request.route_path('login')}" method="post">
    <%form:hidden name="redirect" />
    <div class="row">
        <div class="col-md-6 col-md-offset-3">
            <div class="panel panel-default panel-login">
                <div class="panel-heading">${translate('Login')}</div>
                <div class="panel-body">
                    <div class="form-group">
                        <label for="username" class="sr-only">${translate('Username')}</label>
                        <div class="input-group">
                            <div class="input-group-addon"><i class="glyphicon glyphicon-user"> </i></div>
                            <%form:text id="username" placeholder="${translate('Username')}" name="username" class_="form-control input-lg" />
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="password" class="sr-only">${translate('Password')}</label>
                        <div class="input-group">
                            <div class="input-group-addon"><i class="glyphicon glyphicon-lock"> </i></div>
                            <%form:password id="password" placeholder="${translate('Password')}" name="password" class_="form-control input-lg" />
                        </div>
                    </div>
                    <input type="submit" class="btn btn-primary btn-lg btn-block" name="enter" value="${translate('Enter')}" />
                </div>
            </div><!-- /.panel -->
        </div><!-- /.col -->
    </div><!-- /.row -->
</%form:form>
