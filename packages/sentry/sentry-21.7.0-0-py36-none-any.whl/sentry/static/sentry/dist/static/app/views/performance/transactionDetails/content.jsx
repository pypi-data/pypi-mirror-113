Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var notFound_1 = tslib_1.__importDefault(require("app/components/errors/notFound"));
var eventEntries_1 = require("app/components/events/eventEntries");
var eventMetadata_1 = tslib_1.__importDefault(require("app/components/events/eventMetadata"));
var eventVitals_1 = tslib_1.__importDefault(require("app/components/events/eventVitals"));
var SpanEntryContext = tslib_1.__importStar(require("app/components/events/interfaces/spans/context"));
var rootSpanStatus_1 = tslib_1.__importDefault(require("app/components/events/rootSpanStatus"));
var fileSize_1 = tslib_1.__importDefault(require("app/components/fileSize"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var tagsTable_1 = tslib_1.__importDefault(require("app/components/tagsTable"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var QuickTraceContext = tslib_1.__importStar(require("app/utils/performance/quickTrace/quickTraceContext"));
var quickTraceQuery_1 = tslib_1.__importDefault(require("app/utils/performance/quickTrace/quickTraceQuery"));
var traceMetaQuery_1 = tslib_1.__importDefault(require("app/utils/performance/quickTrace/traceMetaQuery"));
var utils_1 = require("app/utils/performance/quickTrace/utils");
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var queryString_1 = require("app/utils/queryString");
var breadcrumb_1 = tslib_1.__importDefault(require("app/views/performance/breadcrumb"));
var utils_2 = require("../transactionSummary/utils");
var utils_3 = require("../utils");
var eventMetas_1 = tslib_1.__importDefault(require("./eventMetas"));
var EventDetailsContent = /** @class */ (function (_super) {
    tslib_1.__extends(EventDetailsContent, _super);
    function EventDetailsContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            // AsyncComponent state
            loading: true,
            reloading: false,
            error: false,
            errors: {},
            event: undefined,
            // local state
            isSidebarVisible: true,
        };
        _this.toggleSidebar = function () {
            _this.setState({ isSidebarVisible: !_this.state.isSidebarVisible });
        };
        _this.generateTagUrl = function (tag) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            var event = _this.state.event;
            if (!event) {
                return '';
            }
            var query = queryString_1.decodeScalar(location.query.query, '');
            var newQuery = tslib_1.__assign(tslib_1.__assign({}, location.query), { query: queryString_1.appendTagCondition(query, tag.key, tag.value) });
            return utils_2.transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: event.title,
                projectID: queryString_1.decodeScalar(location.query.project),
                query: newQuery,
            });
        };
        return _this;
    }
    EventDetailsContent.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        var eventSlug = params.eventSlug;
        var url = "/organizations/" + organization.slug + "/events/" + eventSlug + "/";
        return [['event', url]];
    };
    Object.defineProperty(EventDetailsContent.prototype, "projectId", {
        get: function () {
            return this.props.eventSlug.split(':')[0];
        },
        enumerable: false,
        configurable: true
    });
    EventDetailsContent.prototype.renderBody = function () {
        var event = this.state.event;
        if (!event) {
            return <notFound_1.default />;
        }
        return this.renderContent(event);
    };
    EventDetailsContent.prototype.renderContent = function (event) {
        var _this = this;
        var _a, _b, _c;
        var _d = this.props, organization = _d.organization, location = _d.location, eventSlug = _d.eventSlug;
        // metrics
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance.event_details',
            eventName: 'Performance: Opened Event Details',
            event_type: event.type,
            organization_id: parseInt(organization.id, 10),
        });
        var isSidebarVisible = this.state.isSidebarVisible;
        var transactionName = event.title;
        var query = queryString_1.decodeScalar(location.query.query, '');
        var eventJsonUrl = "/api/0/projects/" + organization.slug + "/" + this.projectId + "/events/" + event.eventID + "/json/";
        var traceId = (_c = (_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.trace_id) !== null && _c !== void 0 ? _c : '';
        var _e = utils_1.getTraceTimeRangeFromEvent(event), start = _e.start, end = _e.end;
        return (<traceMetaQuery_1.default location={location} orgSlug={organization.slug} traceId={traceId} start={start} end={end}>
        {function (metaResults) { return (<quickTraceQuery_1.default event={event} location={location} orgSlug={organization.slug}>
            {function (results) {
                    var _a;
                    return (<react_1.Fragment>
                <Layout.Header>
                  <Layout.HeaderContent>
                    <breadcrumb_1.default organization={organization} location={location} transactionName={transactionName} eventSlug={eventSlug}/>
                    <Layout.Title data-test-id="event-header">{event.title}</Layout.Title>
                  </Layout.HeaderContent>
                  <Layout.HeaderActions>
                    <buttonBar_1.default gap={1}>
                      <button_1.default onClick={_this.toggleSidebar}>
                        {isSidebarVisible ? 'Hide Details' : 'Show Details'}
                      </button_1.default>
                      {results && (<button_1.default icon={<icons_1.IconOpen />} href={eventJsonUrl} external>
                          {locale_1.t('JSON')} (<fileSize_1.default bytes={event.size}/>)
                        </button_1.default>)}
                    </buttonBar_1.default>
                  </Layout.HeaderActions>
                </Layout.Header>
                <Layout.Body>
                  {results && (<Layout.Main fullWidth>
                      <eventMetas_1.default quickTrace={results} meta={(_a = metaResults === null || metaResults === void 0 ? void 0 : metaResults.meta) !== null && _a !== void 0 ? _a : null} event={event} organization={organization} projectId={_this.projectId} location={location} errorDest="issue" transactionDest="performance"/>
                    </Layout.Main>)}
                  <Layout.Main fullWidth={!isSidebarVisible}>
                    <projects_1.default orgId={organization.slug} slugs={[_this.projectId]}>
                      {function (_a) {
                            var projects = _a.projects;
                            return (<SpanEntryContext.Provider value={{
                                    getViewChildTransactionTarget: function (childTransactionProps) {
                                        return utils_3.getTransactionDetailsUrl(organization, childTransactionProps.eventSlug, childTransactionProps.transaction, location.query);
                                    },
                                }}>
                          <QuickTraceContext.Provider value={results}>
                            <eventEntries_1.BorderlessEventEntries organization={organization} event={event} project={projects[0]} showExampleCommit={false} showTagSummary={false} location={location} api={_this.api} isBorderless/>
                          </QuickTraceContext.Provider>
                        </SpanEntryContext.Provider>);
                        }}
                    </projects_1.default>
                  </Layout.Main>
                  {isSidebarVisible && (<Layout.Side>
                      {results === undefined && (<react_1.Fragment>
                          <eventMetadata_1.default event={event} organization={organization} projectId={_this.projectId}/>
                          <rootSpanStatus_1.default event={event}/>
                        </react_1.Fragment>)}
                      <eventVitals_1.default event={event}/>
                      <tagsTable_1.default event={event} query={query} generateUrl={_this.generateTagUrl}/>
                    </Layout.Side>)}
                </Layout.Body>
              </react_1.Fragment>);
                }}
          </quickTraceQuery_1.default>); }}
      </traceMetaQuery_1.default>);
    };
    EventDetailsContent.prototype.renderError = function (error) {
        var notFound = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 404; });
        var permissionDenied = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 403; });
        if (notFound) {
            return <notFound_1.default />;
        }
        if (permissionDenied) {
            return (<loadingError_1.default message={locale_1.t('You do not have permission to view that event.')}/>);
        }
        return _super.prototype.renderError.call(this, error, true, true);
    };
    EventDetailsContent.prototype.renderComponent = function () {
        var organization = this.props.organization;
        return (<sentryDocumentTitle_1.default title={locale_1.t('Performance - Event Details')} orgSlug={organization.slug}>
        {_super.prototype.renderComponent.call(this)}
      </sentryDocumentTitle_1.default>);
    };
    return EventDetailsContent;
}(asyncComponent_1.default));
exports.default = EventDetailsContent;
//# sourceMappingURL=content.jsx.map