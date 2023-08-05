Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var notFound_1 = tslib_1.__importDefault(require("app/components/errors/notFound"));
var eventOrGroupTitle_1 = tslib_1.__importDefault(require("app/components/eventOrGroupTitle"));
var eventEntries_1 = require("app/components/events/eventEntries");
var eventMessage_1 = tslib_1.__importDefault(require("app/components/events/eventMessage"));
var eventVitals_1 = tslib_1.__importDefault(require("app/components/events/eventVitals"));
var SpanEntryContext = tslib_1.__importStar(require("app/components/events/interfaces/spans/context"));
var fileSize_1 = tslib_1.__importDefault(require("app/components/fileSize"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var tagsTable_1 = tslib_1.__importDefault(require("app/components/tagsTable"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var fields_1 = require("app/utils/discover/fields");
var urls_1 = require("app/utils/discover/urls");
var events_1 = require("app/utils/events");
var QuickTraceContext = tslib_1.__importStar(require("app/utils/performance/quickTrace/quickTraceContext"));
var quickTraceQuery_1 = tslib_1.__importDefault(require("app/utils/performance/quickTrace/quickTraceQuery"));
var traceMetaQuery_1 = tslib_1.__importDefault(require("app/utils/performance/quickTrace/traceMetaQuery"));
var utils_1 = require("app/utils/performance/quickTrace/utils");
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var eventMetas_1 = tslib_1.__importDefault(require("app/views/performance/transactionDetails/eventMetas"));
var utils_2 = require("app/views/performance/transactionSummary/utils");
var breadcrumb_1 = tslib_1.__importDefault(require("../breadcrumb"));
var utils_3 = require("../utils");
var linkedIssue_1 = tslib_1.__importDefault(require("./linkedIssue"));
/**
 * Some tag keys should never be formatted as `tag[...]`
 * when used as a filter because they are predefined.
 */
var EXCLUDED_TAG_KEYS = new Set(['release']);
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
        _this.generateTagKey = function (tag) {
            // Some tags may be normalized from context, but not all of them are.
            // This supports a user making a custom tag with the same name as one
            // that comes from context as all of these are also tags.
            if (tag.key in fields_1.FIELD_TAGS && !EXCLUDED_TAG_KEYS.has(tag.key)) {
                return "tags[" + tag.key + "]";
            }
            return tag.key;
        };
        _this.generateTagUrl = function (tag) {
            var _a;
            var _b = _this.props, eventView = _b.eventView, organization = _b.organization;
            var event = _this.state.event;
            if (!event) {
                return '';
            }
            var eventReference = tslib_1.__assign({}, event);
            if (eventReference.id) {
                delete eventReference.id;
            }
            var tagKey = _this.generateTagKey(tag);
            var nextView = utils_3.getExpandedResults(eventView, (_a = {}, _a[tagKey] = tag.value, _a), eventReference);
            return nextView.getResultsViewUrlTarget(organization.slug);
        };
        _this.getEventSlug = function () {
            var eventSlug = _this.props.params.eventSlug;
            if (typeof eventSlug === 'string') {
                return eventSlug.trim();
            }
            return '';
        };
        return _this;
    }
    EventDetailsContent.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params, location = _a.location, eventView = _a.eventView;
        var eventSlug = params.eventSlug;
        var query = eventView.getEventsAPIPayload(location);
        // Fields aren't used, reduce complexity by omitting from query entirely
        query.field = [];
        var url = "/organizations/" + organization.slug + "/events/" + eventSlug + "/";
        // Get a specific event. This could be coming from
        // a paginated group or standalone event.
        return [['event', url, { query: query }]];
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
        var _a, _b, _c, _d;
        var _e = this.props, organization = _e.organization, location = _e.location, eventView = _e.eventView;
        var isSidebarVisible = this.state.isSidebarVisible;
        // metrics
        analytics_1.trackAnalyticsEvent({
            eventKey: 'discover_v2.event_details',
            eventName: 'Discoverv2: Opened Event Details',
            event_type: event.type,
            organization_id: parseInt(organization.id, 10),
        });
        var transactionName = (_a = event.tags.find(function (tag) { return tag.key === 'transaction'; })) === null || _a === void 0 ? void 0 : _a.value;
        var transactionSummaryTarget = event.type === 'transaction' && transactionName
            ? utils_2.transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: transactionName,
                projectID: event.projectID,
                query: location.query,
            })
            : null;
        var eventJsonUrl = "/api/0/projects/" + organization.slug + "/" + this.projectId + "/events/" + event.eventID + "/json/";
        var renderContent = function (results, metaResults) {
            var _a;
            return (<react_1.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <breadcrumb_1.default eventView={eventView} event={event} organization={organization} location={location}/>
            <EventHeader event={event}/>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <buttonBar_1.default gap={1}>
              <button_1.default onClick={_this.toggleSidebar}>
                {isSidebarVisible ? 'Hide Details' : 'Show Details'}
              </button_1.default>
              <button_1.default icon={<icons_1.IconOpen />} href={eventJsonUrl} external>
                {locale_1.t('JSON')} (<fileSize_1.default bytes={event.size}/>)
              </button_1.default>
              {transactionSummaryTarget && (<feature_1.default organization={organization} features={['performance-view']}>
                  {function (_a) {
                        var hasFeature = _a.hasFeature;
                        return (<button_1.default disabled={!hasFeature} priority="primary" to={transactionSummaryTarget}>
                      {locale_1.t('Go to Summary')}
                    </button_1.default>);
                    }}
                </feature_1.default>)}
            </buttonBar_1.default>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          <Layout.Main fullWidth>
            <eventMetas_1.default quickTrace={results !== null && results !== void 0 ? results : null} meta={(_a = metaResults === null || metaResults === void 0 ? void 0 : metaResults.meta) !== null && _a !== void 0 ? _a : null} event={event} organization={organization} projectId={_this.projectId} location={location} errorDest="discover" transactionDest="discover"/>
          </Layout.Main>
          <Layout.Main fullWidth={!isSidebarVisible}>
            <projects_1.default orgId={organization.slug} slugs={[_this.projectId]}>
              {function (_a) {
                    var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded;
                    return initiallyLoaded ? (<SpanEntryContext.Provider value={{
                            getViewChildTransactionTarget: function (childTransactionProps) {
                                var childTransactionLink = urls_1.eventDetailsRoute({
                                    eventSlug: childTransactionProps.eventSlug,
                                    orgSlug: organization.slug,
                                });
                                return {
                                    pathname: childTransactionLink,
                                    query: eventView.generateQueryStringObject(),
                                };
                            },
                        }}>
                    <QuickTraceContext.Provider value={results}>
                      <eventEntries_1.BorderlessEventEntries organization={organization} event={event} project={projects[0]} location={location} showExampleCommit={false} showTagSummary={false} api={_this.api} isBorderless/>
                    </QuickTraceContext.Provider>
                  </SpanEntryContext.Provider>) : (<loadingIndicator_1.default />);
                }}
            </projects_1.default>
          </Layout.Main>
          {isSidebarVisible && (<Layout.Side>
              <eventVitals_1.default event={event}/>
              {event.groupID && (<linkedIssue_1.default groupId={event.groupID} eventId={event.eventID}/>)}
              <tagsTable_1.default generateUrl={_this.generateTagUrl} event={event} query={eventView.query}/>
            </Layout.Side>)}
        </Layout.Body>
      </react_1.Fragment>);
        };
        var hasQuickTraceView = organization.features.includes('performance-view');
        if (hasQuickTraceView) {
            var traceId = (_d = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id) !== null && _d !== void 0 ? _d : '';
            var _f = utils_1.getTraceTimeRangeFromEvent(event), start = _f.start, end = _f.end;
            return (<traceMetaQuery_1.default location={location} orgSlug={organization.slug} traceId={traceId} start={start} end={end}>
          {function (metaResults) { return (<quickTraceQuery_1.default event={event} location={location} orgSlug={organization.slug}>
              {function (results) { return renderContent(results, metaResults); }}
            </quickTraceQuery_1.default>); }}
        </traceMetaQuery_1.default>);
        }
        return renderContent();
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
        var _a = this.props, eventView = _a.eventView, organization = _a.organization;
        var event = this.state.event;
        var eventSlug = this.getEventSlug();
        var projectSlug = eventSlug.split(':')[0];
        var title = utils_3.generateTitle({ eventView: eventView, event: event, organization: organization });
        return (<sentryDocumentTitle_1.default title={title} orgSlug={organization.slug} projectSlug={projectSlug}>
        {_super.prototype.renderComponent.call(this)}
      </sentryDocumentTitle_1.default>);
    };
    return EventDetailsContent;
}(asyncComponent_1.default));
var EventHeader = function (_a) {
    var event = _a.event;
    var message = events_1.getMessage(event);
    return (<EventHeaderContainer data-test-id="event-header">
      <TitleWrapper>
        <eventOrGroupTitle_1.default data={event}/>
      </TitleWrapper>
      {message && (<MessageWrapper>
          <eventMessage_1.default message={message}/>
        </MessageWrapper>)}
    </EventHeaderContainer>);
};
var EventHeaderContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  max-width: ", ";\n"], ["\n  max-width: ", ";\n"])), function (p) { return p.theme.breakpoints[0]; });
var TitleWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-top: 20px;\n"], ["\n  font-size: ", ";\n  margin-top: 20px;\n"])), function (p) { return p.theme.headerFontSize; });
var MessageWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(1));
exports.default = EventDetailsContent;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=content.jsx.map