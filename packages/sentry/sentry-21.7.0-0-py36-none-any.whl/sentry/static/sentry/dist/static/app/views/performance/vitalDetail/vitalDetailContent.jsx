Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var createAlertButton_1 = require("app/components/createAlertButton");
var searchBar_1 = tslib_1.__importDefault(require("app/components/events/searchBar"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var TeamKeyTransactionManager = tslib_1.__importStar(require("app/components/performance/teamKeyTransactionsManager"));
var icons_1 = require("app/icons");
var iconFlag_1 = require("app/icons/iconFlag");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var fields_1 = require("app/utils/discover/fields");
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var breadcrumb_1 = tslib_1.__importDefault(require("../breadcrumb"));
var utils_2 = require("../utils");
var table_1 = tslib_1.__importDefault(require("./table"));
var utils_3 = require("./utils");
var vitalChart_1 = tslib_1.__importDefault(require("./vitalChart"));
var vitalInfo_1 = tslib_1.__importDefault(require("./vitalInfo"));
var FRONTEND_VITALS = [fields_1.WebVital.FCP, fields_1.WebVital.LCP, fields_1.WebVital.FID, fields_1.WebVital.CLS];
function getSummaryConditions(query) {
    var parsed = tokenizeSearch_1.tokenizeSearch(query);
    parsed.query = [];
    return parsed.formatString();
}
var VitalDetailContent = /** @class */ (function (_super) {
    tslib_1.__extends(VitalDetailContent, _super);
    function VitalDetailContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            incompatibleAlertNotice: null,
            error: undefined,
        };
        _this.handleSearch = function (query) {
            var location = _this.props.location;
            var queryParams = getParams_1.getParams(tslib_1.__assign(tslib_1.__assign({}, (location.query || {})), { query: query }));
            // do not propagate pagination when making a new search
            var searchQueryParams = omit_1.default(queryParams, 'cursor');
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: searchQueryParams,
            });
        };
        _this.generateTagUrl = function (key, value) {
            var location = _this.props.location;
            var query = utils_1.generateQueryWithTag(location.query, { key: key, value: value });
            return tslib_1.__assign(tslib_1.__assign({}, location), { query: query });
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, _errors) {
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        _this.setError = function (error) {
            _this.setState({ error: error });
        };
        return _this;
    }
    VitalDetailContent.prototype.renderCreateAlertButton = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects;
        return (<createAlertButton_1.CreateAlertFromViewButton eventView={eventView} organization={organization} projects={projects} onIncompatibleQuery={this.handleIncompatibleQuery} onSuccess={function () { }} referrer="performance"/>);
    };
    VitalDetailContent.prototype.renderVitalSwitcher = function () {
        var _a = this.props, vitalName = _a.vitalName, location = _a.location;
        var position = FRONTEND_VITALS.indexOf(vitalName);
        if (position < 0) {
            return null;
        }
        var previousDisabled = position === 0;
        var nextDisabled = position === FRONTEND_VITALS.length - 1;
        var switchVital = function (newVitalName) {
            return function () {
                react_router_1.browserHistory.push({
                    pathname: location.pathname,
                    query: tslib_1.__assign(tslib_1.__assign({}, location.query), { vitalName: newVitalName }),
                });
            };
        };
        return (<buttonBar_1.default merged>
        <button_1.default icon={<icons_1.IconChevron direction="left" size="sm"/>} aria-label={locale_1.t('Previous')} disabled={previousDisabled} onClick={switchVital(FRONTEND_VITALS[position - 1])}/>
        <button_1.default icon={<icons_1.IconChevron direction="right" size="sm"/>} aria-label={locale_1.t('Next')} disabled={nextDisabled} onClick={switchVital(FRONTEND_VITALS[position + 1])}/>
      </buttonBar_1.default>);
    };
    VitalDetailContent.prototype.renderError = function () {
        var error = this.state.error;
        if (!error) {
            return null;
        }
        return (<alert_1.default type="error" icon={<iconFlag_1.IconFlag size="md"/>}>
        {error}
      </alert_1.default>);
    };
    VitalDetailContent.prototype.render = function () {
        var _this = this;
        var _a = this.props, location = _a.location, eventView = _a.eventView, organization = _a.organization, vitalName = _a.vitalName, projects = _a.projects, teams = _a.teams;
        var incompatibleAlertNotice = this.state.incompatibleAlertNotice;
        var query = queryString_1.decodeScalar(location.query.query, '');
        var vital = vitalName || fields_1.WebVital.LCP;
        var filterString = utils_2.getTransactionSearchQuery(location);
        var summaryConditions = getSummaryConditions(filterString);
        var description = utils_3.vitalDescription[vitalName];
        var userTeams = teams.filter(function (_a) {
            var isMember = _a.isMember;
            return isMember;
        });
        return (<React.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <breadcrumb_1.default organization={organization} location={location} vitalName={vital}/>
            <Layout.Title>{utils_3.vitalMap[vital]}</Layout.Title>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <buttonBar_1.default gap={1}>
              <feature_1.default organization={organization} features={['incidents']}>
                {function (_a) {
            var hasFeature = _a.hasFeature;
            return hasFeature && _this.renderCreateAlertButton();
        }}
              </feature_1.default>
              {this.renderVitalSwitcher()}
            </buttonBar_1.default>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          {this.renderError()}
          {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
          <Layout.Main fullWidth>
            <StyledDescription>{description}</StyledDescription>
            <StyledSearchBar searchSource="performance_vitals" organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={this.handleSearch}/>
            <vitalChart_1.default organization={organization} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>
            <StyledVitalInfo>
              <vitalInfo_1.default eventView={eventView} organization={organization} location={location} vital={vital}/>
            </StyledVitalInfo>
            <feature_1.default organization={organization} features={['team-key-transactions']}>
              {function (_a) {
                var hasFeature = _a.hasFeature;
                return hasFeature ? (<TeamKeyTransactionManager.Provider organization={organization} teams={userTeams} selectedTeams={['myteams']} selectedProjects={eventView.project.map(String)}>
                    <table_1.default eventView={eventView} projects={projects} organization={organization} location={location} setError={_this.setError} summaryConditions={summaryConditions}/>
                  </TeamKeyTransactionManager.Provider>) : (<table_1.default eventView={eventView} projects={projects} organization={organization} location={location} setError={_this.setError} summaryConditions={summaryConditions}/>);
            }}
            </feature_1.default>
          </Layout.Main>
        </Layout.Body>
      </React.Fragment>);
    };
    return VitalDetailContent;
}(React.Component));
var StyledDescription = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(3));
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
var StyledVitalInfo = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(3));
exports.default = withTeams_1.default(withProjects_1.default(VitalDetailContent));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=vitalDetailContent.jsx.map