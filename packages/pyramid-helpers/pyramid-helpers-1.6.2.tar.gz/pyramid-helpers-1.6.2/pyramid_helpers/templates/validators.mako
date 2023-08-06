<%!
import pprint
%>\
<%namespace name="form" file="/form-tags.mako"/>\
<%inherit file="/site.mako" />\
<div class="page-header">
    <h2>${translate('Validators')}</h2>
</div>
<%form:form name="validators_form" method="post" enctype="multipart/form-data">
    <%form:hidden name="hidden_input" />
    <fieldset>
        <legend>${translate('Standard inputs')}</legend>

        <div class="form-group">
            <label for="text-input">${translate('Text')}</label>
            <%form:text id="text-input" name="text_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="textarea-input">${translate('Text area')}</label>
            <%form:textarea id="textarea-input" name="textarea_input" class_="form-control"></%form:textarea>
        </div>

        <div class="form-group">
            <label for="password-input">${translate('Password')}</label>
            <%form:password id="password-input" name="password_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="search-input">${translate('Search')}</label>
            <%form:search id="search-input" name="search_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label>
                <%form:checkbox id="checkbox-input" name="checkbox_input" value="true" />
                ${translate('Checkbox')}
            </label>
        </div>

        <div class="form-group">
            <label>
                <%form:radio id="radio-input-1" name="radio_input" value="one" />
                ${translate('Radio (One)')}
            </label>
            <label>
                <%form:radio id="radio-input-2" name="radio_input" value="two" />
                ${translate('Radio (Two)')}
            </label>
            <label>
                <%form:radio id="radio-input-3" name="radio_input" value="three" />
                ${translate('Radio (Three)')}
            </label>
            <label>
                <%form:radio id="radio-input-4" name="radio_input" value="invalid" />
                ${translate('Radio (Invalid)')}
            </label>
        </div>

        <div class="form-group">
            <label for="select-input1">${translate('Select (Numbers)')}</label>
            <%form:select id="select-input1" name="select_input1" class_="form-control">
                <%form:option value="">--</%form:option>
                <%form:option value="one">${translate('One')}</%form:option>
                <%form:option value="two">${translate('Two')}</%form:option>
                <%form:option value="three">${translate('Three')}</%form:option>
                <%form:option value="invalid">${translate('Invalid')}</%form:option>
            </%form:select>
        </div>

        <div class="form-group">
            <label for="select-input2">${translate('Select (Fruits)')}</label>
            <%form:select id="select-input2" name="select_input2" class_="form-control">
                <%form:option value="">--</%form:option>
                <%form:optgroup label="${translate('Fruits')}">
                    <%form:option value="apple">${translate('Apple')}</%form:option>
                    <%form:option value="banana">${translate('Banana')}</%form:option>
                    <%form:option value="orange">${translate('Orange')}</%form:option>
                </%form:optgroup>
                <%form:optgroup label="${translate('Numbers')}">
                    <%form:option value="one">${translate('One')}</%form:option>
                    <%form:option value="two">${translate('Two')}</%form:option>
                    <%form:option value="three">${translate('Three')}</%form:option>
                </%form:optgroup>
            </%form:select>
        </div>

        <div class="form-group">
            <label for="upload-input">${translate('Upload')}</label>
            <%form:upload id="upload-input" name="upload_input" />
        </div>
    </fieldset>

    <fieldset>
        <legend>${translate('Number inputs')}</legend>

        <div class="form-group">
            <label for="number-input">${translate('Number')}</label>
            <%form:number id="number-input" name="number_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="range-input">${translate('Range')} (0-100)</label>
            <%form:range id="range-input" name="range_input" class_="form-control" />
        </div>
    </fieldset>

    <fieldset>
        <legend>${translate('Communication inputs')}</legend>

        <div class="form-group">
            <label for="url-input">${translate('Url')}</label>
            <%form:url id="url-input" name="url_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="email-input">${translate('Email')}</label>
            <%form:email id="email-input" name="email_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="tel-input">${translate('Tel')}</label>
            <%form:tel id="tel-input" name="tel_input" class_="form-control" />
        </div>
    </fieldset>

    <fieldset>
        <legend>${translate('Date/time inputs')}</legend>

        <div class="form-group">
            <label for="time-input">${translate('Time')}</label>
            <%form:time id="time-input" name="time_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="week-input">${translate('Week')}</label>
            <%form:week id="week-input" name="week_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="month-input">${translate('Month')}</label>
            <%form:month id="month-input" name="month_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="date-input">${translate('Date')}</label>
            <%form:date id="date-input" name="date_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="datetime-local-input">${translate('Datetime local')}</label>
            <%form:datetime_local id="datetime-local-input" name="datetime_local_input" class_="form-control" placeholder="YYYY-MM-DDTHH:MM"/>
        </div>

        <div class="form-group">
            <label for="datetime-naive-input">${translate('Datetime UTC (naive)')}</label>
            <%form:datetime_local id="datetime-naive-input" name="datetime_naive_input" class_="form-control" placeholder="YYYY-MM-DDTHH:MM"/>
        </div>
    </fieldset>

    <fieldset>
        <legend>${translate('Miscellaneous inputs')}</legend>

        <div class="form-group">
            <label for="color-input">${translate('Color')}</label>
            <%form:color id="color-input" name="color_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="list-input">${translate('List')}</label>
            <%form:text id="list-input" name="list_input" class_="form-control" />
        </div>
    </fieldset>

    <div class="form-group text-right">
        <input class="btn btn-primary" type="submit" name="submit_input" value="${translate('Submit')}" />
    </div>
</%form:form>

% if errors:
<h3>${translate('Errors')}</h3>
<pre>${pprint.pformat(errors)}</pre>
% elif result:
<h3>${translate('Result')}</h3>
<pre>${pprint.pformat(result)}</pre>
% endif
