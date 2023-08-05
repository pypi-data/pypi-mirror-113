Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var badge_1 = tslib_1.__importDefault(require("app/components/badge"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var queryCount_1 = tslib_1.__importDefault(require("app/components/queryCount"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var savedSearchTab_1 = tslib_1.__importDefault(require("./savedSearchTab"));
var utils_1 = require("./utils");
function WrapGuideTabs(_a) {
    var children = _a.children, tabQuery = _a.tabQuery, query = _a.query, to = _a.to;
    if (tabQuery === utils_1.Query.FOR_REVIEW) {
        return (<guideAnchor_1.default target="inbox_guide_tab" disabled={query === utils_1.Query.FOR_REVIEW} to={to}>
        <guideAnchor_1.default target="for_review_guide_tab">{children}</guideAnchor_1.default>
      </guideAnchor_1.default>);
    }
    return children;
}
function IssueListHeader(_a) {
    var _b, _c;
    var organization = _a.organization, query = _a.query, sort = _a.sort, queryCount = _a.queryCount, queryCounts = _a.queryCounts, realtimeActive = _a.realtimeActive, onRealtimeChange = _a.onRealtimeChange, onSavedSearchSelect = _a.onSavedSearchSelect, onSavedSearchDelete = _a.onSavedSearchDelete, savedSearchList = _a.savedSearchList, router = _a.router, displayReprocessingTab = _a.displayReprocessingTab;
    var tabs = utils_1.getTabs(organization);
    var visibleTabs = displayReprocessingTab
        ? tabs
        : tabs.filter(function (_a) {
            var _b = tslib_1.__read(_a, 1), tab = _b[0];
            return tab !== utils_1.Query.REPROCESSING;
        });
    var savedSearchTabActive = !visibleTabs.some(function (_a) {
        var _b = tslib_1.__read(_a, 1), tabQuery = _b[0];
        return tabQuery === query;
    });
    // Remove cursor and page when switching tabs
    var _d = (_c = (_b = router === null || router === void 0 ? void 0 : router.location) === null || _b === void 0 ? void 0 : _b.query) !== null && _c !== void 0 ? _c : {}, _ = _d.cursor, __ = _d.page, queryParms = tslib_1.__rest(_d, ["cursor", "page"]);
    var sortParam = queryParms.sort === utils_1.IssueSortOptions.INBOX ? undefined : queryParms.sort;
    function trackTabClick(tabQuery) {
        // Clicking on inbox tab and currently another tab is active
        if (tabQuery === utils_1.Query.FOR_REVIEW && query !== utils_1.Query.FOR_REVIEW) {
            analytics_1.trackAnalyticsEvent({
                eventKey: 'inbox_tab.clicked',
                eventName: 'Clicked Inbox Tab',
                organization_id: organization.id,
            });
        }
    }
    return (<React.Fragment>
      <BorderlessHeader>
        <StyledHeaderContent>
          <StyledLayoutTitle>{locale_1.t('Issues')}</StyledLayoutTitle>
        </StyledHeaderContent>
        <Layout.HeaderActions>
          <buttonBar_1.default gap={1}>
            <button_1.default size="small" data-test-id="real-time" title={locale_1.t('%s real-time updates', realtimeActive ? locale_1.t('Pause') : locale_1.t('Enable'))} onClick={function () { return onRealtimeChange(!realtimeActive); }}>
              {realtimeActive ? <icons_1.IconPause size="xs"/> : <icons_1.IconPlay size="xs"/>}
            </button_1.default>
          </buttonBar_1.default>
        </Layout.HeaderActions>
      </BorderlessHeader>
      <TabLayoutHeader>
        <Layout.HeaderNavTabs underlined>
          {visibleTabs.map(function (_a) {
            var _b;
            var _c = tslib_1.__read(_a, 2), tabQuery = _c[0], _d = _c[1], queryName = _d.name, tooltipTitle = _d.tooltipTitle, tooltipHoverable = _d.tooltipHoverable;
            var to = {
                query: tslib_1.__assign(tslib_1.__assign({}, queryParms), { query: tabQuery, sort: tabQuery === utils_1.Query.FOR_REVIEW ? utils_1.IssueSortOptions.INBOX : sortParam }),
                pathname: "/organizations/" + organization.slug + "/issues/",
            };
            return (<li key={tabQuery} className={query === tabQuery ? 'active' : ''}>
                  <react_router_1.Link to={to} onClick={function () { return trackTabClick(tabQuery); }}>
                    <WrapGuideTabs query={query} tabQuery={tabQuery} to={to}>
                      <tooltip_1.default title={tooltipTitle} position="bottom" isHoverable={tooltipHoverable} delay={1000}>
                        {queryName}{' '}
                        {((_b = queryCounts[tabQuery]) === null || _b === void 0 ? void 0 : _b.count) > 0 && (<badge_1.default type={tabQuery === utils_1.Query.FOR_REVIEW &&
                        queryCounts[tabQuery].count > 0
                        ? 'review'
                        : 'default'}>
                            <queryCount_1.default hideParens count={queryCounts[tabQuery].count} max={queryCounts[tabQuery].hasMore ? utils_1.TAB_MAX_COUNT : 1000}/>
                          </badge_1.default>)}
                      </tooltip_1.default>
                    </WrapGuideTabs>
                  </react_router_1.Link>
                </li>);
        })}
          <savedSearchTab_1.default organization={organization} query={query} sort={sort} savedSearchList={savedSearchList} onSavedSearchSelect={onSavedSearchSelect} onSavedSearchDelete={onSavedSearchDelete} isActive={savedSearchTabActive} queryCount={queryCount}/>
        </Layout.HeaderNavTabs>
      </TabLayoutHeader>
    </React.Fragment>);
}
exports.default = withProjects_1.default(IssueListHeader);
var StyledLayoutTitle = styled_1.default(Layout.Title)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(0.5));
var BorderlessHeader = styled_1.default(Layout.Header)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-bottom: 0;\n  /* Not enough buttons to change direction for mobile view */\n  grid-template-columns: 1fr auto;\n"], ["\n  border-bottom: 0;\n  /* Not enough buttons to change direction for mobile view */\n  grid-template-columns: 1fr auto;\n"])));
var TabLayoutHeader = styled_1.default(Layout.Header)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding-top: 0;\n\n  @media (max-width: ", ") {\n    padding-top: 0;\n  }\n"], ["\n  padding-top: 0;\n\n  @media (max-width: ", ") {\n    padding-top: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledHeaderContent = styled_1.default(Layout.HeaderContent)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  margin-right: ", ";\n"], ["\n  margin-bottom: 0;\n  margin-right: ", ";\n"])), space_1.default(2));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=header.jsx.map