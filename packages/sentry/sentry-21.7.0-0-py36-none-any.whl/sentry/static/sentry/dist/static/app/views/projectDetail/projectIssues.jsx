Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var styles_1 = require("app/components/charts/styles");
var discoverButton_1 = tslib_1.__importDefault(require("app/components/discoverButton"));
var groupList_1 = tslib_1.__importDefault(require("app/components/issues/groupList"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var constants_1 = require("app/constants");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var queryString_1 = require("app/utils/queryString");
var noGroupsHandler_1 = tslib_1.__importDefault(require("../issueList/noGroupsHandler"));
function ProjectIssues(_a) {
    var organization = _a.organization, location = _a.location, projectId = _a.projectId, query = _a.query, api = _a.api;
    var _b = tslib_1.__read(react_1.useState(), 2), pageLinks = _b[0], setPageLinks = _b[1];
    var _c = tslib_1.__read(react_1.useState(), 2), onCursor = _c[0], setOnCursor = _c[1];
    function handleOpenInIssuesClick() {
        analytics_1.trackAnalyticsEvent({
            eventKey: 'project_detail.open_issues',
            eventName: 'Project Detail: Open issues from project detail',
            organization_id: parseInt(organization.id, 10),
        });
    }
    function handleOpenInDiscoverClick() {
        analytics_1.trackAnalyticsEvent({
            eventKey: 'project_detail.open_discover',
            eventName: 'Project Detail: Open discover from project detail',
            organization_id: parseInt(organization.id, 10),
        });
    }
    function handleFetchSuccess(groupListState, cursorHandler) {
        setPageLinks(groupListState.pageLinks);
        setOnCursor(function () { return cursorHandler; });
    }
    function getDiscoverUrl() {
        return {
            pathname: "/organizations/" + organization.slug + "/discover/results/",
            query: tslib_1.__assign({ name: locale_1.t('Frequent Unhandled Issues'), field: ['issue', 'title', 'count()', 'count_unique(user)', 'project'], sort: ['-count'], query: ['event.type:error error.unhandled:true', query].join(' ').trim(), display: 'top5' }, getParams_1.getParams(pick_1.default(location.query, tslib_1.__spreadArray([], tslib_1.__read(Object.values(globalSelectionHeader_1.URL_PARAM)))))),
        };
    }
    var endpointPath = "/organizations/" + organization.slug + "/issues/";
    var issueQuery = ['is:unresolved error.unhandled:true ', query].join(' ').trim();
    var queryParams = tslib_1.__assign(tslib_1.__assign({ limit: 5 }, getParams_1.getParams(pick_1.default(location.query, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(Object.values(globalSelectionHeader_1.URL_PARAM))), ['cursor'])))), { query: issueQuery, sort: 'freq' });
    var issueSearch = {
        pathname: endpointPath,
        query: queryParams,
    };
    function renderEmptyMessage() {
        var selectedTimePeriod = location.query.start
            ? null
            : constants_1.DEFAULT_RELATIVE_PERIODS[queryString_1.decodeScalar(location.query.statsPeriod, constants_1.DEFAULT_STATS_PERIOD)];
        var displayedPeriod = selectedTimePeriod
            ? selectedTimePeriod.toLowerCase()
            : locale_1.t('given timeframe');
        return (<panels_1.Panel>
        <panels_1.PanelBody>
          <noGroupsHandler_1.default api={api} organization={organization} query={issueQuery} selectedProjectIds={[projectId]} groupIds={[]} emptyMessage={locale_1.tct('No unhandled issues for the [timePeriod].', {
                timePeriod: displayedPeriod,
            })}/>
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
    return (<react_1.Fragment>
      <ControlsWrapper>
        <styles_1.SectionHeading>{locale_1.t('Frequent Unhandled Issues')}</styles_1.SectionHeading>
        <buttonBar_1.default gap={1}>
          <button_1.default data-test-id="issues-open" size="small" to={issueSearch} onClick={handleOpenInIssuesClick}>
            {locale_1.t('Open in Issues')}
          </button_1.default>
          <discoverButton_1.default onClick={handleOpenInDiscoverClick} to={getDiscoverUrl()} size="small">
            {locale_1.t('Open in Discover')}
          </discoverButton_1.default>
          <StyledPagination pageLinks={pageLinks} onCursor={onCursor}/>
        </buttonBar_1.default>
      </ControlsWrapper>

      <groupList_1.default orgId={organization.slug} endpointPath={endpointPath} queryParams={queryParams} query="" canSelectGroups={false} renderEmptyMessage={renderEmptyMessage} withChart={false} withPagination={false} onFetchSuccess={handleFetchSuccess}/>
    </react_1.Fragment>);
}
var ControlsWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  flex-wrap: wrap;\n  @media (max-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  flex-wrap: wrap;\n  @media (max-width: ", ") {\n    display: block;\n  }\n"])), space_1.default(1), function (p) { return p.theme.breakpoints[0]; });
var StyledPagination = styled_1.default(pagination_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
exports.default = ProjectIssues;
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectIssues.jsx.map