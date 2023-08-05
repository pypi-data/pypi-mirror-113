Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var traceFullQuery_1 = require("app/utils/performance/quickTrace/traceFullQuery");
var traceMetaQuery_1 = tslib_1.__importDefault(require("app/utils/performance/quickTrace/traceMetaQuery"));
var queryString_1 = require("app/utils/queryString");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var content_1 = tslib_1.__importDefault(require("./content"));
var TraceSummary = /** @class */ (function (_super) {
    tslib_1.__extends(TraceSummary, _super);
    function TraceSummary() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TraceSummary.prototype.getDocumentTitle = function () {
        return [locale_1.t('Trace Details'), locale_1.t('Performance')].join(' - ');
    };
    TraceSummary.prototype.getTraceSlug = function () {
        var traceSlug = this.props.params.traceSlug;
        return typeof traceSlug === 'string' ? traceSlug.trim() : '';
    };
    TraceSummary.prototype.getDateSelection = function () {
        var location = this.props.location;
        var queryParams = getParams_1.getParams(location.query, {
            allowAbsolutePageDatetime: true,
        });
        var start = queryString_1.decodeScalar(queryParams.start);
        var end = queryString_1.decodeScalar(queryParams.end);
        var statsPeriod = queryString_1.decodeScalar(queryParams.statsPeriod);
        return { start: start, end: end, statsPeriod: statsPeriod };
    };
    TraceSummary.prototype.getTraceEventView = function () {
        var traceSlug = this.getTraceSlug();
        var _a = this.getDateSelection(), start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod;
        return eventView_1.default.fromSavedQuery({
            id: undefined,
            name: "Events with Trace ID " + traceSlug,
            fields: ['title', 'event.type', 'project', 'timestamp'],
            orderby: '-timestamp',
            query: "trace:" + traceSlug,
            projects: [globalSelectionHeader_1.ALL_ACCESS_PROJECTS],
            version: 2,
            start: start,
            end: end,
            range: statsPeriod,
        });
    };
    TraceSummary.prototype.renderContent = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, params = _a.params;
        var traceSlug = this.getTraceSlug();
        var _b = this.getDateSelection(), start = _b.start, end = _b.end, statsPeriod = _b.statsPeriod;
        var dateSelected = Boolean(statsPeriod || (start && end));
        var content = function (_a) {
            var isLoading = _a.isLoading, error = _a.error, traces = _a.traces, meta = _a.meta;
            return (<content_1.default location={location} organization={organization} params={params} traceSlug={traceSlug} traceEventView={_this.getTraceEventView()} dateSelected={dateSelected} isLoading={isLoading} error={error} traces={traces} meta={meta}/>);
        };
        if (!dateSelected) {
            return content({
                isLoading: false,
                error: 'date selection not specified',
                traces: null,
                meta: null,
            });
        }
        return (<traceFullQuery_1.TraceFullDetailedQuery location={location} orgSlug={organization.slug} traceId={traceSlug} start={start} end={end} statsPeriod={statsPeriod}>
        {function (traceResults) { return (<traceMetaQuery_1.default location={location} orgSlug={organization.slug} traceId={traceSlug} start={start} end={end} statsPeriod={statsPeriod}>
            {function (metaResults) {
                    return content({
                        isLoading: traceResults.isLoading || metaResults.isLoading,
                        error: traceResults.error || metaResults.error,
                        traces: traceResults.traces,
                        meta: metaResults.meta,
                    });
                }}
          </traceMetaQuery_1.default>); }}
      </traceFullQuery_1.TraceFullDetailedQuery>);
    };
    TraceSummary.prototype.render = function () {
        var organization = this.props.organization;
        return (<sentryDocumentTitle_1.default title={this.getDocumentTitle()} orgSlug={organization.slug}>
        <StyledPageContent>
          <lightWeightNoProjectMessage_1.default organization={organization}>
            {this.renderContent()}
          </lightWeightNoProjectMessage_1.default>
        </StyledPageContent>
      </sentryDocumentTitle_1.default>);
    };
    return TraceSummary;
}(react_1.Component));
exports.default = withOrganization_1.default(withApi_1.default(TraceSummary));
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map