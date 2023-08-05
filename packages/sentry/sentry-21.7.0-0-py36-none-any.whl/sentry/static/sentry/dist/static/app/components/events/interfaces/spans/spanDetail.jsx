Object.defineProperty(exports, "__esModule", { value: true });
exports.Tags = exports.Row = exports.SpanDetails = exports.SpanDetailContainer = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var map_1 = tslib_1.__importDefault(require("lodash/map"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var discoverButton_1 = tslib_1.__importDefault(require("app/components/discoverButton"));
var fileSize_1 = tslib_1.__importDefault(require("app/components/fileSize"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var rowDetails_1 = require("app/components/performance/waterfall/rowDetails");
var pill_1 = tslib_1.__importDefault(require("app/components/pill"));
var pills_1 = tslib_1.__importDefault(require("app/components/pills"));
var utils_1 = require("app/components/quickTrace/utils");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_2 = require("app/types/utils");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var urls_1 = require("app/utils/discover/urls");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var SpanEntryContext = tslib_1.__importStar(require("./context"));
var inlineDocs_1 = tslib_1.__importDefault(require("./inlineDocs"));
var types_1 = require("./types");
var utils_3 = require("./utils");
var DEFAULT_ERRORS_VISIBLE = 5;
var SIZE_DATA_KEYS = ['Encoded Body Size', 'Decoded Body Size', 'Transfer Size'];
var SpanDetail = /** @class */ (function (_super) {
    tslib_1.__extends(SpanDetail, _super);
    function SpanDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            errorsOpened: false,
        };
        _this.toggleErrors = function () {
            _this.setState(function (_a) {
                var errorsOpened = _a.errorsOpened;
                return ({ errorsOpened: !errorsOpened });
            });
        };
        return _this;
    }
    SpanDetail.prototype.renderTraversalButton = function () {
        if (!this.props.childTransactions) {
            // TODO: Amend size to use theme when we eventually refactor LoadingIndicator
            // 12px is consistent with theme.iconSizes['xs'] but theme returns a string.
            return (<StyledDiscoverButton size="xsmall" disabled>
          <StyledLoadingIndicator size={12}/>
        </StyledDiscoverButton>);
        }
        if (this.props.childTransactions.length <= 0) {
            return (<StyledDiscoverButton size="xsmall" disabled>
          {locale_1.t('No Children')}
        </StyledDiscoverButton>);
        }
        var _a = this.props, span = _a.span, trace = _a.trace, event = _a.event, organization = _a.organization;
        utils_2.assert(!utils_3.isGapSpan(span));
        if (this.props.childTransactions.length === 1) {
            // Note: This is rendered by this.renderSpanChild() as a dedicated row
            return null;
        }
        var orgFeatures = new Set(organization.features);
        var _b = utils_3.getTraceDateTimeRange({
            start: trace.traceStartTimestamp,
            end: trace.traceEndTimestamp,
        }), start = _b.start, end = _b.end;
        var childrenEventView = eventView_1.default.fromSavedQuery({
            id: undefined,
            name: "Children from Span ID " + span.span_id,
            fields: [
                'transaction',
                'project',
                'trace.span',
                'transaction.duration',
                'timestamp',
            ],
            orderby: '-timestamp',
            query: "event.type:transaction trace:" + span.trace_id + " trace.parent_span:" + span.span_id,
            projects: orgFeatures.has('global-views')
                ? [globalSelectionHeader_1.ALL_ACCESS_PROJECTS]
                : [Number(event.projectID)],
            version: 2,
            start: start,
            end: end,
        });
        return (<StyledDiscoverButton data-test-id="view-child-transactions" size="xsmall" to={childrenEventView.getResultsViewUrlTarget(organization.slug)}>
        {locale_1.t('View Children')}
      </StyledDiscoverButton>);
    };
    SpanDetail.prototype.renderSpanChild = function () {
        var childTransactions = this.props.childTransactions;
        if (!childTransactions || childTransactions.length !== 1) {
            return null;
        }
        var childTransaction = childTransactions[0];
        var transactionResult = {
            'project.name': childTransaction.project_slug,
            transaction: childTransaction.transaction,
            'trace.span': childTransaction.span_id,
            id: childTransaction.event_id,
        };
        var eventSlug = generateSlug(transactionResult);
        var viewChildButton = (<SpanEntryContext.Consumer>
        {function (_a) {
                var getViewChildTransactionTarget = _a.getViewChildTransactionTarget;
                var to = getViewChildTransactionTarget(tslib_1.__assign(tslib_1.__assign({}, transactionResult), { eventSlug: eventSlug }));
                if (!to) {
                    return null;
                }
                return (<StyledButton data-test-id="view-child-transaction" size="xsmall" to={to}>
              {locale_1.t('View Transaction')}
            </StyledButton>);
            }}
      </SpanEntryContext.Consumer>);
        return (<exports.Row title="Child Transaction" extra={viewChildButton}>
        {transactionResult.transaction + " (" + transactionResult['project.name'] + ")"}
      </exports.Row>);
    };
    SpanDetail.prototype.renderTraceButton = function () {
        var _a = this.props, span = _a.span, organization = _a.organization, event = _a.event;
        if (utils_3.isGapSpan(span)) {
            return null;
        }
        return (<StyledButton size="xsmall" to={utils_1.generateTraceTarget(event, organization)}>
        {locale_1.t('View Trace')}
      </StyledButton>);
    };
    SpanDetail.prototype.renderOrphanSpanMessage = function () {
        var span = this.props.span;
        if (!utils_3.isOrphanSpan(span)) {
            return null;
        }
        return (<alert_1.default system type="info" icon={<icons_1.IconWarning size="md"/>}>
        {locale_1.t('This is a span that has no parent span within this transaction. It has been attached to the transaction root span by default.')}
      </alert_1.default>);
    };
    SpanDetail.prototype.renderSpanErrorMessage = function () {
        var _a = this.props, span = _a.span, organization = _a.organization, relatedErrors = _a.relatedErrors;
        var errorsOpened = this.state.errorsOpened;
        if (!relatedErrors || relatedErrors.length <= 0 || utils_3.isGapSpan(span)) {
            return null;
        }
        var visibleErrors = errorsOpened
            ? relatedErrors
            : relatedErrors.slice(0, DEFAULT_ERRORS_VISIBLE);
        return (<alert_1.default system type="error" icon={<icons_1.IconWarning size="md"/>}>
        <rowDetails_1.ErrorMessageTitle>
          {locale_1.tn('An error event occurred in this transaction.', '%s error events occurred in this transaction.', relatedErrors.length)}
        </rowDetails_1.ErrorMessageTitle>
        <rowDetails_1.ErrorMessageContent>
          {visibleErrors.map(function (error) { return (<React.Fragment key={error.event_id}>
              <rowDetails_1.ErrorDot level={error.level}/>
              <rowDetails_1.ErrorLevel>{error.level}</rowDetails_1.ErrorLevel>
              <rowDetails_1.ErrorTitle>
                <link_1.default to={utils_1.generateIssueEventTarget(error, organization)}>
                  {error.title}
                </link_1.default>
              </rowDetails_1.ErrorTitle>
            </React.Fragment>); })}
        </rowDetails_1.ErrorMessageContent>
        {relatedErrors.length > DEFAULT_ERRORS_VISIBLE && (<ErrorToggle size="xsmall" onClick={this.toggleErrors}>
            {errorsOpened ? locale_1.t('Show less') : locale_1.t('Show more')}
          </ErrorToggle>)}
      </alert_1.default>);
    };
    SpanDetail.prototype.partitionSizes = function (data) {
        var sizeKeys = SIZE_DATA_KEYS.reduce(function (keys, key) {
            if (data.hasOwnProperty(key)) {
                keys[key] = data[key];
            }
            return keys;
        }, {});
        var nonSizeKeys = tslib_1.__assign({}, data);
        SIZE_DATA_KEYS.forEach(function (key) { return delete nonSizeKeys[key]; });
        return {
            sizeKeys: sizeKeys,
            nonSizeKeys: nonSizeKeys,
        };
    };
    SpanDetail.prototype.renderSpanDetails = function () {
        var _a, _b, _c;
        var _d = this.props, span = _d.span, event = _d.event, location = _d.location, organization = _d.organization, scrollToHash = _d.scrollToHash;
        if (utils_3.isGapSpan(span)) {
            return (<exports.SpanDetails>
          <inlineDocs_1.default platform={((_a = event.sdk) === null || _a === void 0 ? void 0 : _a.name) || ''} orgSlug={organization.slug} projectSlug={event.projectSlug}/>
        </exports.SpanDetails>);
        }
        var startTimestamp = span.start_timestamp;
        var endTimestamp = span.timestamp;
        var duration = (endTimestamp - startTimestamp) * 1000;
        var durationString = Number(duration.toFixed(3)).toLocaleString() + "ms";
        var unknownKeys = Object.keys(span).filter(function (key) {
            return !types_1.rawSpanKeys.has(key);
        });
        var _e = this.partitionSizes((_b = span === null || span === void 0 ? void 0 : span.data) !== null && _b !== void 0 ? _b : {}), sizeKeys = _e.sizeKeys, nonSizeKeys = _e.nonSizeKeys;
        var allZeroSizes = SIZE_DATA_KEYS.map(function (key) { return sizeKeys[key]; }).every(function (value) { return value === 0; });
        return (<React.Fragment>
        {this.renderOrphanSpanMessage()}
        {this.renderSpanErrorMessage()}
        <exports.SpanDetails>
          <table className="table key-value">
            <tbody>
              <exports.Row title={utils_3.isGapSpan(span) ? (<SpanIdTitle>Span ID</SpanIdTitle>) : (<SpanIdTitle onClick={utils_3.scrollToSpan(span.span_id, scrollToHash, location)}>
                      Span ID
                      <StyledIconAnchor />
                    </SpanIdTitle>)} extra={this.renderTraversalButton()}>
                {span.span_id}
              </exports.Row>
              <exports.Row title="Parent Span ID">{span.parent_span_id || ''}</exports.Row>
              {this.renderSpanChild()}
              <exports.Row title="Trace ID" extra={this.renderTraceButton()}>
                {span.trace_id}
              </exports.Row>
              <exports.Row title="Description">{(_c = span === null || span === void 0 ? void 0 : span.description) !== null && _c !== void 0 ? _c : ''}</exports.Row>
              <exports.Row title="Status">{span.status || ''}</exports.Row>
              <exports.Row title="Start Date">
                {getDynamicText_1.default({
                fixed: 'Mar 16, 2020 9:10:12 AM UTC',
                value: (<React.Fragment>
                      <dateTime_1.default date={startTimestamp * 1000}/>
                      {" (" + startTimestamp + ")"}
                    </React.Fragment>),
            })}
              </exports.Row>
              <exports.Row title="End Date">
                {getDynamicText_1.default({
                fixed: 'Mar 16, 2020 9:10:13 AM UTC',
                value: (<React.Fragment>
                      <dateTime_1.default date={endTimestamp * 1000}/>
                      {" (" + endTimestamp + ")"}
                    </React.Fragment>),
            })}
              </exports.Row>
              <exports.Row title="Duration">{durationString}</exports.Row>
              <exports.Row title="Operation">{span.op || ''}</exports.Row>
              <exports.Row title="Same Process as Parent">
                {span.same_process_as_parent !== undefined
                ? String(span.same_process_as_parent)
                : null}
              </exports.Row>
              <exports.Tags span={span}/>
              {allZeroSizes && (<TextTr>
                  The following sizes were not collected for security reasons. Check if
                  the host serves the appropriate
                  <externalLink_1.default href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Timing-Allow-Origin">
                    <span className="val-string">Timing-Allow-Origin</span>
                  </externalLink_1.default>
                  header. You may have to enable this collection manually.
                </TextTr>)}
              {map_1.default(sizeKeys, function (value, key) { return (<exports.Row title={key} key={key}>
                  <React.Fragment>
                    <fileSize_1.default bytes={value}/>
                    {value >= 1024 && (<span>{" (" + (JSON.stringify(value, null, 4) || '') + " B)"}</span>)}
                  </React.Fragment>
                </exports.Row>); })}
              {map_1.default(nonSizeKeys, function (value, key) { return (<exports.Row title={key} key={key}>
                  {JSON.stringify(value, null, 4) || ''}
                </exports.Row>); })}
              {unknownKeys.map(function (key) { return (<exports.Row title={key} key={key}>
                  {JSON.stringify(span[key], null, 4) || ''}
                </exports.Row>); })}
            </tbody>
          </table>
        </exports.SpanDetails>
      </React.Fragment>);
    };
    SpanDetail.prototype.render = function () {
        return (<exports.SpanDetailContainer data-component="span-detail" onClick={function (event) {
                // prevent toggling the span detail
                event.stopPropagation();
            }}>
        {this.renderSpanDetails()}
      </exports.SpanDetailContainer>);
    };
    return SpanDetail;
}(React.Component));
var StyledDiscoverButton = styled_1.default(discoverButton_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"], ["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"])), space_1.default(0.75), space_1.default(0.5));
var StyledButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"], ["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"])), space_1.default(0.75), space_1.default(0.5));
exports.SpanDetailContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n  cursor: auto;\n"], ["\n  border-bottom: 1px solid ", ";\n  cursor: auto;\n"])), function (p) { return p.theme.border; });
exports.SpanDetails = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space_1.default(2));
var ValueTd = styled_1.default('td')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var StyledLoadingIndicator = styled_1.default(loadingIndicator_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: ", ";\n  margin: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  height: ", ";\n  margin: 0;\n"])), space_1.default(2));
var StyledText = styled_1.default('p')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin: ", " ", ";\n"], ["\n  font-size: ", ";\n  margin: ", " ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(2), space_1.default(0));
var TextTr = function (_a) {
    var children = _a.children;
    return (<tr>
    <td className="key"/>
    <ValueTd className="value">
      <StyledText>{children}</StyledText>
    </ValueTd>
  </tr>);
};
var ErrorToggle = styled_1.default(button_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(0.75));
var SpanIdTitle = styled_1.default('a')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"], ["\n  display: flex;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
var StyledIconAnchor = styled_1.default(icons_1.IconAnchor)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: block;\n  color: ", ";\n  margin-left: ", ";\n"], ["\n  display: block;\n  color: ", ";\n  margin-left: ", ";\n"])), function (p) { return p.theme.gray300; }, space_1.default(1));
var Row = function (_a) {
    var title = _a.title, keep = _a.keep, children = _a.children, _b = _a.extra, extra = _b === void 0 ? null : _b;
    if (!keep && !children) {
        return null;
    }
    return (<tr>
      <td className="key">{title}</td>
      <ValueTd className="value">
        <pre className="val">
          <span className="val-string">{children}</span>
        </pre>
        {extra}
      </ValueTd>
    </tr>);
};
exports.Row = Row;
var Tags = function (_a) {
    var span = _a.span;
    var tags = span === null || span === void 0 ? void 0 : span.tags;
    if (!tags) {
        return null;
    }
    var keys = Object.keys(tags);
    if (keys.length <= 0) {
        return null;
    }
    return (<tr>
      <td className="key">Tags</td>
      <td className="value">
        <pills_1.default style={{ padding: '8px' }}>
          {keys.map(function (key, index) { return (<pill_1.default key={index} name={key} value={String(tags[key]) || ''}/>); })}
        </pills_1.default>
      </td>
    </tr>);
};
exports.Tags = Tags;
function generateSlug(result) {
    return urls_1.generateEventSlug({
        id: result.id,
        'project.name': result['project.name'],
    });
}
exports.default = withApi_1.default(react_router_1.withRouter(SpanDetail));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=spanDetail.jsx.map