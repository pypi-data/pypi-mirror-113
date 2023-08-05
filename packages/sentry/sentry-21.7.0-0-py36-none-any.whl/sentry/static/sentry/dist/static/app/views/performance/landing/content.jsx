Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var searchBar_1 = tslib_1.__importDefault(require("app/components/events/searchBar"));
var featureBadge_1 = tslib_1.__importDefault(require("app/components/featureBadge"));
var TeamKeyTransactionManager = tslib_1.__importStar(require("app/components/performance/teamKeyTransactionsManager"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var fields_1 = require("app/utils/discover/fields");
var isActiveSuperuser_1 = require("app/utils/isActiveSuperuser");
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var index_1 = tslib_1.__importDefault(require("../charts/index"));
var data_1 = require("../data");
var table_1 = tslib_1.__importDefault(require("../table"));
var utils_1 = require("../utils");
var doubleAxisDisplay_1 = tslib_1.__importDefault(require("./display/doubleAxisDisplay"));
var data_2 = require("./data");
var utils_2 = require("./utils");
var vitalsCards_1 = require("./vitalsCards");
var LandingContent = /** @class */ (function (_super) {
    tslib_1.__extends(LandingContent, _super);
    function LandingContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLandingDisplayChange = function (field) {
            var _a = _this.props, location = _a.location, organization = _a.organization, eventView = _a.eventView, projects = _a.projects;
            var newQuery = tslib_1.__assign({}, location.query);
            delete newQuery[utils_2.LEFT_AXIS_QUERY_KEY];
            delete newQuery[utils_2.RIGHT_AXIS_QUERY_KEY];
            var defaultDisplay = utils_2.getDefaultDisplayFieldForPlatform(projects, eventView);
            var currentDisplay = queryString_1.decodeScalar(location.query.landingDisplay);
            // Transaction op can affect the display and show no results if it is explicitly set.
            var query = queryString_1.decodeScalar(location.query.query, '');
            var searchConditions = tokenizeSearch_1.tokenizeSearch(query);
            searchConditions.removeTag('transaction.op');
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.landingv2.display_change',
                eventName: 'Performance Views: Landing v2 Display Change',
                organization_id: parseInt(organization.id, 10),
                change_to_display: field,
                default_display: defaultDisplay,
                current_display: currentDisplay,
                is_default: defaultDisplay === currentDisplay,
            });
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, newQuery), { query: searchConditions.formatString(), landingDisplay: field }),
            });
        };
        _this.renderLandingFrontend = function (isPageload) {
            var _a = _this.props, organization = _a.organization, location = _a.location, projects = _a.projects, eventView = _a.eventView, setError = _a.setError;
            var columnTitles = isPageload
                ? data_2.FRONTEND_PAGELOAD_COLUMN_TITLES
                : data_2.FRONTEND_OTHER_COLUMN_TITLES;
            var axisOptions = isPageload
                ? data_1.getFrontendAxisOptions(organization)
                : data_1.getFrontendOtherAxisOptions(organization);
            var _b = utils_2.getDisplayAxes(axisOptions, location), leftAxis = _b.leftAxis, rightAxis = _b.rightAxis;
            return (<react_1.Fragment>
        {isPageload && (<vitalsCards_1.FrontendCards eventView={eventView} organization={organization} location={location} projects={projects}/>)}
        <doubleAxisDisplay_1.default eventView={eventView} organization={organization} location={location} axisOptions={axisOptions} leftAxis={leftAxis} rightAxis={rightAxis}/>
        <table_1.default eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()} columnTitles={columnTitles}/>
      </react_1.Fragment>);
        };
        _this.renderLandingBackend = function () {
            var _a = _this.props, organization = _a.organization, location = _a.location, projects = _a.projects, eventView = _a.eventView, setError = _a.setError;
            var axisOptions = data_1.getBackendAxisOptions(organization);
            var _b = utils_2.getDisplayAxes(axisOptions, location), leftAxis = _b.leftAxis, rightAxis = _b.rightAxis;
            var columnTitles = data_2.BACKEND_COLUMN_TITLES;
            return (<react_1.Fragment>
        <vitalsCards_1.BackendCards eventView={eventView} organization={organization} location={location}/>
        <doubleAxisDisplay_1.default eventView={eventView} organization={organization} location={location} axisOptions={axisOptions} leftAxis={leftAxis} rightAxis={rightAxis}/>
        <table_1.default eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()} columnTitles={columnTitles}/>
      </react_1.Fragment>);
        };
        _this.renderLandingMobile = function () {
            var _a = _this.props, organization = _a.organization, location = _a.location, projects = _a.projects, eventView = _a.eventView, setError = _a.setError;
            var axisOptions = data_1.getMobileAxisOptions(organization);
            var _b = utils_2.getDisplayAxes(axisOptions, location), leftAxis = _b.leftAxis, rightAxis = _b.rightAxis;
            var columnTitles = data_2.MOBILE_COLUMN_TITLES;
            return (<react_1.Fragment>
        <doubleAxisDisplay_1.default eventView={eventView} organization={organization} location={location} axisOptions={axisOptions} leftAxis={leftAxis} rightAxis={rightAxis}/>
        <table_1.default eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()} columnTitles={columnTitles}/>
      </react_1.Fragment>);
        };
        _this.renderLandingAll = function () {
            var _a = _this.props, organization = _a.organization, location = _a.location, router = _a.router, projects = _a.projects, eventView = _a.eventView, setError = _a.setError;
            return (<react_1.Fragment>
        <index_1.default eventView={eventView} organization={organization} location={location} router={router}/>
        <table_1.default eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()}/>
      </react_1.Fragment>);
        };
        return _this;
    }
    LandingContent.prototype.getSummaryConditions = function (query) {
        var parsed = tokenizeSearch_1.tokenizeSearch(query);
        parsed.query = [];
        return parsed.formatString();
    };
    LandingContent.prototype.renderSelectedDisplay = function (display) {
        switch (display) {
            case utils_2.LandingDisplayField.ALL:
                return this.renderLandingAll();
            case utils_2.LandingDisplayField.FRONTEND_PAGELOAD:
                return this.renderLandingFrontend(true);
            case utils_2.LandingDisplayField.FRONTEND_OTHER:
                return this.renderLandingFrontend(false);
            case utils_2.LandingDisplayField.BACKEND:
                return this.renderLandingBackend();
            case utils_2.LandingDisplayField.MOBILE:
                return this.renderLandingMobile();
            default:
                throw new Error("Unknown display: " + display);
        }
    };
    LandingContent.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, location = _a.location, eventView = _a.eventView, projects = _a.projects, teams = _a.teams, handleSearch = _a.handleSearch;
        var currentLandingDisplay = utils_2.getCurrentLandingDisplay(location, projects, eventView);
        var filterString = utils_1.getTransactionSearchQuery(location, eventView.query);
        var isSuperuser = isActiveSuperuser_1.isActiveSuperuser();
        var userTeams = teams.filter(function (_a) {
            var isMember = _a.isMember;
            return isMember || isSuperuser;
        });
        return (<react_1.Fragment>
        <SearchContainer>
          <searchBar_1.default searchSource="performance_landing" organization={organization} projectIds={eventView.project} query={filterString} fields={fields_1.generateAggregateFields(organization, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(eventView.fields)), [{ field: 'tps()' }]), ['epm()', 'eps()'])} onSearch={handleSearch} maxQueryLength={constants_1.MAX_QUERY_LENGTH}/>
          <dropdownControl_1.default buttonProps={{ prefix: locale_1.t('Display') }} label={currentLandingDisplay.label}>
            {utils_2.LANDING_DISPLAYS.filter(function (_a) {
                var isShown = _a.isShown;
                return !isShown || isShown(organization);
            }).map(function (_a) {
                var alpha = _a.alpha, label = _a.label, field = _a.field;
                return (<dropdownControl_1.DropdownItem key={field} onSelect={_this.handleLandingDisplayChange} eventKey={field} data-test-id={field} isActive={field === currentLandingDisplay.field}>
                {label}
                {alpha && <featureBadge_1.default type="alpha" noTooltip/>}
              </dropdownControl_1.DropdownItem>);
            })}
          </dropdownControl_1.default>
        </SearchContainer>
        <feature_1.default organization={organization} features={['team-key-transactions']}>
          {function (_a) {
                var hasFeature = _a.hasFeature;
                return hasFeature ? (<TeamKeyTransactionManager.Provider organization={organization} teams={userTeams} selectedTeams={['myteams']} selectedProjects={eventView.project.map(String)}>
                {_this.renderSelectedDisplay(currentLandingDisplay.field)}
              </TeamKeyTransactionManager.Provider>) : (_this.renderSelectedDisplay(currentLandingDisplay.field));
            }}
        </feature_1.default>
      </react_1.Fragment>);
    };
    return LandingContent;
}(react_1.Component));
var SearchContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr min-content;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr min-content;\n  }\n"])), space_1.default(2), space_1.default(2), function (p) { return p.theme.breakpoints[0]; });
exports.default = react_router_1.withRouter(withTeams_1.default(LandingContent));
var templateObject_1;
//# sourceMappingURL=content.jsx.map