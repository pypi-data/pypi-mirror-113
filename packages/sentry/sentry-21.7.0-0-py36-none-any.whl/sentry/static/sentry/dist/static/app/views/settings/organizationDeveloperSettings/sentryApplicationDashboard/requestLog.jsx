Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var memoize_1 = tslib_1.__importDefault(require("lodash/memoize"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var checkbox_1 = tslib_1.__importDefault(require("app/components/checkbox"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var ALL_EVENTS = locale_1.t('All Events');
var MAX_PER_PAGE = 10;
var componentHasSelectUri = function (issueLinkComponent) {
    var hasSelectUri = function (fields) {
        return fields.some(function (field) { return field.type === 'select' && 'uri' in field; });
    };
    var createHasSelectUri = hasSelectUri(issueLinkComponent.create.required_fields) ||
        hasSelectUri(issueLinkComponent.create.optional_fields || []);
    var linkHasSelectUri = hasSelectUri(issueLinkComponent.link.required_fields) ||
        hasSelectUri(issueLinkComponent.link.optional_fields || []);
    return createHasSelectUri || linkHasSelectUri;
};
var getEventTypes = memoize_1.default(function (app) {
    // TODO(nola): ideally this would be kept in sync with EXTENDED_VALID_EVENTS on the backend
    var issueLinkEvents = [];
    var issueLinkComponent = (app.schema.elements || []).find(function (element) { return element.type === 'issue-link'; });
    if (issueLinkComponent) {
        issueLinkEvents = ['external_issue.created', 'external_issue.linked'];
        if (componentHasSelectUri(issueLinkComponent)) {
            issueLinkEvents.push('select_options.requested');
        }
    }
    var events = tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([
        ALL_EVENTS
    ], tslib_1.__read((app.status !== 'internal'
        ? ['installation.created', 'installation.deleted']
        : []))), tslib_1.__read((app.events.includes('error') ? ['error.created'] : []))), tslib_1.__read((app.events.includes('issue')
        ? ['issue.created', 'issue.resolved', 'issue.ignored', 'issue.assigned']
        : []))), tslib_1.__read((app.isAlertable
        ? [
            'event_alert.triggered',
            'metric_alert.open',
            'metric_alert.resolved',
            'metric_alert.critical',
            'metric_alert.warning',
        ]
        : []))), tslib_1.__read(issueLinkEvents));
    return events;
});
var ResponseCode = function (_a) {
    var code = _a.code;
    var type = 'error';
    if (code <= 399 && code >= 300) {
        type = 'warning';
    }
    else if (code <= 299 && code >= 100) {
        type = 'success';
    }
    return (<Tags>
      <StyledTag type={type}>{code === 0 ? 'timeout' : code}</StyledTag>
    </Tags>);
};
var TimestampLink = function (_a) {
    var date = _a.date, link = _a.link;
    return link ? (<externalLink_1.default href={link}>
      <dateTime_1.default date={date}/>
      <StyledIconOpen size="12px"/>
    </externalLink_1.default>) : (<dateTime_1.default date={date}/>);
};
var RequestLog = /** @class */ (function (_super) {
    tslib_1.__extends(RequestLog, _super);
    function RequestLog() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        _this.handleChangeEventType = function (eventType) {
            _this.setState({
                eventType: eventType,
                currentPage: 0,
            }, _this.remountComponent);
        };
        _this.handleChangeErrorsOnly = function () {
            _this.setState({
                errorsOnly: !_this.state.errorsOnly,
                currentPage: 0,
            }, _this.remountComponent);
        };
        _this.handleNextPage = function () {
            _this.setState({
                currentPage: _this.state.currentPage + 1,
            });
        };
        _this.handlePrevPage = function () {
            _this.setState({
                currentPage: _this.state.currentPage - 1,
            });
        };
        return _this;
    }
    Object.defineProperty(RequestLog.prototype, "hasNextPage", {
        get: function () {
            return (this.state.currentPage + 1) * MAX_PER_PAGE < this.state.requests.length;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(RequestLog.prototype, "hasPrevPage", {
        get: function () {
            return this.state.currentPage > 0;
        },
        enumerable: false,
        configurable: true
    });
    RequestLog.prototype.getEndpoints = function () {
        var slug = this.props.app.slug;
        var query = {};
        if (this.state) {
            if (this.state.eventType !== ALL_EVENTS) {
                query.eventType = this.state.eventType;
            }
            if (this.state.errorsOnly) {
                query.errorsOnly = true;
            }
        }
        return [['requests', "/sentry-apps/" + slug + "/requests/", { query: query }]];
    };
    RequestLog.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { requests: [], eventType: ALL_EVENTS, errorsOnly: false, currentPage: 0 });
    };
    RequestLog.prototype.renderLoading = function () {
        return this.renderBody();
    };
    RequestLog.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, requests = _a.requests, eventType = _a.eventType, errorsOnly = _a.errorsOnly, currentPage = _a.currentPage;
        var app = this.props.app;
        var currentRequests = requests.slice(currentPage * MAX_PER_PAGE, (currentPage + 1) * MAX_PER_PAGE);
        return (<React.Fragment>
        <h5>{locale_1.t('Request Log')}</h5>

        <div>
          <p>
            {locale_1.t('This log shows the status of any outgoing webhook requests from Sentry to your integration.')}
          </p>

          <RequestLogFilters>
            <dropdownControl_1.default label={eventType} menuWidth="220px" button={function (_a) {
                var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
                return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen}>
                  {eventType}
                </StyledDropdownButton>);
            }}>
              {getEventTypes(app).map(function (type) { return (<dropdownControl_1.DropdownItem key={type} onSelect={_this.handleChangeEventType} eventKey={type} isActive={eventType === type}>
                  {type}
                </dropdownControl_1.DropdownItem>); })}
            </dropdownControl_1.default>

            <StyledErrorsOnlyButton onClick={this.handleChangeErrorsOnly}>
              <ErrorsOnlyCheckbox>
                <checkbox_1.default checked={errorsOnly} onChange={function () { }}/>
                {locale_1.t('Errors Only')}
              </ErrorsOnlyCheckbox>
            </StyledErrorsOnlyButton>
          </RequestLogFilters>
        </div>

        <panels_1.Panel>
          <panels_1.PanelHeader>
            <TableLayout hasOrganization={app.status !== 'internal'}>
              <div>{locale_1.t('Time')}</div>
              <div>{locale_1.t('Status Code')}</div>
              {app.status !== 'internal' && <div>{locale_1.t('Organization')}</div>}
              <div>{locale_1.t('Event Type')}</div>
              <div>{locale_1.t('Webhook URL')}</div>
            </TableLayout>
          </panels_1.PanelHeader>

          {!this.state.loading ? (<panels_1.PanelBody>
              {currentRequests.length > 0 ? (currentRequests.map(function (request, idx) { return (<panels_1.PanelItem key={idx}>
                    <TableLayout hasOrganization={app.status !== 'internal'}>
                      <TimestampLink date={request.date} link={request.errorUrl}/>
                      <ResponseCode code={request.responseCode}/>
                      {app.status !== 'internal' && (<div>
                          {request.organization ? request.organization.name : null}
                        </div>)}
                      <div>{request.eventType}</div>
                      <OverflowBox>{request.webhookUrl}</OverflowBox>
                    </TableLayout>
                  </panels_1.PanelItem>); })) : (<emptyMessage_1.default icon={<icons_1.IconFlag size="xl"/>}>
                  {locale_1.t('No requests found in the last 30 days.')}
                </emptyMessage_1.default>)}
            </panels_1.PanelBody>) : (<loadingIndicator_1.default />)}
        </panels_1.Panel>

        <PaginationButtons>
          <button_1.default icon={<icons_1.IconChevron direction="left" size="sm"/>} onClick={this.handlePrevPage} disabled={!this.hasPrevPage} label={locale_1.t('Previous page')}/>
          <button_1.default icon={<icons_1.IconChevron direction="right" size="sm"/>} onClick={this.handleNextPage} disabled={!this.hasNextPage} label={locale_1.t('Next page')}/>
        </PaginationButtons>
      </React.Fragment>);
    };
    return RequestLog;
}(asyncComponent_1.default));
exports.default = RequestLog;
var TableLayout = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 0.5fr ", " 1fr 1fr;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 0.5fr ", " 1fr 1fr;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n"])), function (p) { return (p.hasOrganization ? '1fr' : ''); }, space_1.default(1.5));
var OverflowBox = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  word-break: break-word;\n"], ["\n  word-break: break-word;\n"])));
var PaginationButtons = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n\n  > :first-child {\n    border-top-right-radius: 0;\n    border-bottom-right-radius: 0;\n  }\n\n  > :nth-child(2) {\n    margin-left: -1px;\n    border-top-left-radius: 0;\n    border-bottom-left-radius: 0;\n  }\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n\n  > :first-child {\n    border-top-right-radius: 0;\n    border-bottom-right-radius: 0;\n  }\n\n  > :nth-child(2) {\n    margin-left: -1px;\n    border-top-left-radius: 0;\n    border-bottom-left-radius: 0;\n  }\n"])));
var RequestLogFilters = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding-bottom: ", ";\n"])), space_1.default(1));
var ErrorsOnlyCheckbox = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  input {\n    margin: 0 ", " 0 0;\n  }\n\n  display: flex;\n  align-items: center;\n"], ["\n  input {\n    margin: 0 ", " 0 0;\n  }\n\n  display: flex;\n  align-items: center;\n"])), space_1.default(1));
var StyledDropdownButton = styled_1.default(dropdownButton_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  z-index: ", ";\n  white-space: nowrap;\n\n  border-top-right-radius: 0;\n  border-bottom-right-radius: 0;\n"], ["\n  z-index: ", ";\n  white-space: nowrap;\n\n  border-top-right-radius: 0;\n  border-bottom-right-radius: 0;\n"])), function (p) { return p.theme.zIndex.header - 1; });
var StyledErrorsOnlyButton = styled_1.default(button_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-left: -1px;\n  border-top-left-radius: 0;\n  border-bottom-left-radius: 0;\n"], ["\n  margin-left: -1px;\n  border-top-left-radius: 0;\n  border-bottom-left-radius: 0;\n"])));
var StyledIconOpen = styled_1.default(icons_1.IconOpen)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin-left: 6px;\n  color: ", ";\n"], ["\n  margin-left: 6px;\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var Tags = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  margin: -", ";\n"], ["\n  margin: -", ";\n"])), space_1.default(0.5));
var StyledTag = styled_1.default(tag_1.default)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  display: inline-flex;\n"], ["\n  padding: ", ";\n  display: inline-flex;\n"])), space_1.default(0.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=requestLog.jsx.map