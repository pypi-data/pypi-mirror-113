Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var tags_1 = require("app/actionCreators/tags");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var globalSdkUpdateAlert_1 = tslib_1.__importDefault(require("app/components/globalSdkUpdateAlert"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var pageHeading_1 = tslib_1.__importDefault(require("app/components/pageHeading"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var globalSelectionHeader_2 = require("app/constants/globalSelectionHeader");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var analytics_1 = require("app/utils/analytics");
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var content_1 = tslib_1.__importDefault(require("./landing/content"));
var utils_1 = require("./trends/utils");
var data_1 = require("./data");
var onboarding_1 = tslib_1.__importDefault(require("./onboarding"));
var utils_2 = require("./utils");
var PerformanceContent = /** @class */ (function (_super) {
    tslib_1.__extends(PerformanceContent, _super);
    function PerformanceContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: data_1.generatePerformanceEventView(_this.props.organization, _this.props.location, _this.props.projects),
            error: undefined,
        };
        _this.setError = function (error) {
            _this.setState({ error: error });
        };
        _this.handleSearch = function (searchQuery) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.overview.search',
                eventName: 'Performance Views: Transaction overview search',
                organization_id: parseInt(organization.id, 10),
            });
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, query: String(searchQuery).trim() || undefined }),
            });
        };
        return _this;
    }
    PerformanceContent.getDerivedStateFromProps = function (nextProps, prevState) {
        return tslib_1.__assign(tslib_1.__assign({}, prevState), { eventView: data_1.generatePerformanceEventView(nextProps.organization, nextProps.location, nextProps.projects) });
    };
    PerformanceContent.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        tags_1.loadOrganizationTags(api, organization.slug, selection);
        utils_2.addRoutePerformanceContext(selection);
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance_views.overview.view',
            eventName: 'Performance Views: Transaction overview view',
            organization_id: parseInt(organization.id, 10),
        });
    };
    PerformanceContent.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        if (!isEqual_1.default(prevProps.selection.projects, selection.projects) ||
            !isEqual_1.default(prevProps.selection.datetime, selection.datetime)) {
            tags_1.loadOrganizationTags(api, organization.slug, selection);
            utils_2.addRoutePerformanceContext(selection);
        }
    };
    PerformanceContent.prototype.renderError = function () {
        var error = this.state.error;
        if (!error) {
            return null;
        }
        return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
        {error}
      </alert_1.default>);
    };
    PerformanceContent.prototype.handleTrendsClick = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var newQuery = tslib_1.__assign({}, location.query);
        var query = queryString_1.decodeScalar(location.query.query, '');
        var conditions = tokenizeSearch_1.tokenizeSearch(query);
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance_views.change_view',
            eventName: 'Performance Views: Change View',
            organization_id: parseInt(organization.id, 10),
            view_name: 'TRENDS',
        });
        var modifiedConditions = new tokenizeSearch_1.QueryResults([]);
        if (conditions.hasTag('tpm()')) {
            modifiedConditions.setTagValues('tpm()', conditions.getTagValues('tpm()'));
        }
        else {
            modifiedConditions.setTagValues('tpm()', ['>0.01']);
        }
        if (conditions.hasTag('transaction.duration')) {
            modifiedConditions.setTagValues('transaction.duration', conditions.getTagValues('transaction.duration'));
        }
        else {
            modifiedConditions.setTagValues('transaction.duration', [
                '>0',
                "<" + utils_1.DEFAULT_MAX_DURATION,
            ]);
        }
        newQuery.query = modifiedConditions.formatString();
        react_router_1.browserHistory.push({
            pathname: utils_2.getPerformanceTrendsUrl(organization),
            query: tslib_1.__assign({}, newQuery),
        });
    };
    PerformanceContent.prototype.shouldShowOnboarding = function () {
        var _a = this.props, projects = _a.projects, demoMode = _a.demoMode;
        var eventView = this.state.eventView;
        // XXX used by getsentry to bypass onboarding for the upsell demo state.
        if (demoMode) {
            return false;
        }
        if (projects.length === 0) {
            return false;
        }
        // Current selection is 'my projects' or 'all projects'
        if (eventView.project.length === 0 || eventView.project === [globalSelectionHeader_2.ALL_ACCESS_PROJECTS]) {
            return (projects.filter(function (p) { return p.firstTransactionEvent === false; }).length === projects.length);
        }
        // Any other subset of projects.
        return (projects.filter(function (p) {
            return eventView.project.includes(parseInt(p.id, 10)) &&
                p.firstTransactionEvent === false;
        }).length === eventView.project.length);
    };
    PerformanceContent.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, projects = _a.projects;
        var eventView = this.state.eventView;
        var showOnboarding = this.shouldShowOnboarding();
        return (<organization_1.PageContent>
        <lightWeightNoProjectMessage_1.default organization={organization}>
          <organization_1.PageHeader>
            <pageHeading_1.default>{locale_1.t('Performance')}</pageHeading_1.default>
            {!showOnboarding && (<button_1.default priority="primary" data-test-id="landing-header-trends" onClick={function () { return _this.handleTrendsClick(); }}>
                {locale_1.t('View Trends')}
              </button_1.default>)}
          </organization_1.PageHeader>
          <globalSdkUpdateAlert_1.default />
          {this.renderError()}
          {showOnboarding ? (<onboarding_1.default organization={organization}/>) : (<content_1.default eventView={eventView} projects={projects} organization={organization} setError={this.setError} handleSearch={this.handleSearch}/>)}
        </lightWeightNoProjectMessage_1.default>
      </organization_1.PageContent>);
    };
    PerformanceContent.prototype.render = function () {
        var organization = this.props.organization;
        return (<sentryDocumentTitle_1.default title={locale_1.t('Performance')} orgSlug={organization.slug}>
        <globalSelectionHeader_1.default defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: data_1.DEFAULT_STATS_PERIOD,
                },
            }}>
          {this.renderBody()}
        </globalSelectionHeader_1.default>
      </sentryDocumentTitle_1.default>);
    };
    return PerformanceContent;
}(react_1.Component));
exports.default = withApi_1.default(withOrganization_1.default(withProjects_1.default(withGlobalSelection_1.default(PerformanceContent))));
//# sourceMappingURL=content.jsx.map