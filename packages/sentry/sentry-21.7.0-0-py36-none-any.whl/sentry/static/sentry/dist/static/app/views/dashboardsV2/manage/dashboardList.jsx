Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var widget_area_svg_1 = tslib_1.__importDefault(require("sentry-images/dashboard/widget-area.svg"));
var widget_bar_svg_1 = tslib_1.__importDefault(require("sentry-images/dashboard/widget-bar.svg"));
var widget_big_number_svg_1 = tslib_1.__importDefault(require("sentry-images/dashboard/widget-big-number.svg"));
var widget_line_1_svg_1 = tslib_1.__importDefault(require("sentry-images/dashboard/widget-line-1.svg"));
var widget_table_svg_1 = tslib_1.__importDefault(require("sentry-images/dashboard/widget-table.svg"));
var widget_world_map_svg_1 = tslib_1.__importDefault(require("sentry-images/dashboard/widget-world-map.svg"));
var dashboards_1 = require("app/actionCreators/dashboards");
var indicator_1 = require("app/actionCreators/indicator");
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var types_1 = require("app/views/dashboardsV2/types");
var contextMenu_1 = tslib_1.__importDefault(require("../contextMenu"));
var utils_1 = require("../utils");
var dashboardCard_1 = tslib_1.__importDefault(require("./dashboardCard"));
function DashboardList(_a) {
    var api = _a.api, organization = _a.organization, location = _a.location, dashboards = _a.dashboards, pageLinks = _a.pageLinks, onDashboardsChange = _a.onDashboardsChange;
    function miniWidget(displayType) {
        switch (displayType) {
            case types_1.DisplayType.BAR:
                return widget_bar_svg_1.default;
            case types_1.DisplayType.AREA:
                return widget_area_svg_1.default;
            case types_1.DisplayType.BIG_NUMBER:
                return widget_big_number_svg_1.default;
            case types_1.DisplayType.TABLE:
                return widget_table_svg_1.default;
            case types_1.DisplayType.WORLD_MAP:
                return widget_world_map_svg_1.default;
            case types_1.DisplayType.LINE:
            default:
                return widget_line_1_svg_1.default;
        }
    }
    function handleDelete(dashboard) {
        dashboards_1.deleteDashboard(api, organization.slug, dashboard.id)
            .then(function () {
            analytics_1.trackAnalyticsEvent({
                eventKey: 'dashboards_manage.delete',
                eventName: 'Dashboards Manager: Dashboard Deleted',
                organization_id: parseInt(organization.id, 10),
                dashboard_id: parseInt(dashboard.id, 10),
            });
            onDashboardsChange();
            indicator_1.addSuccessMessage(locale_1.t('Dashboard deleted'));
        })
            .catch(function () {
            indicator_1.addErrorMessage(locale_1.t('Error deleting Dashboard'));
        });
    }
    function handleDuplicate(dashboard) {
        dashboards_1.fetchDashboard(api, organization.slug, dashboard.id)
            .then(function (dashboardDetail) {
            var newDashboard = utils_1.cloneDashboard(dashboardDetail);
            newDashboard.widgets.map(function (widget) { return (widget.id = undefined); });
            dashboards_1.createDashboard(api, organization.slug, newDashboard, true).then(function () {
                analytics_1.trackAnalyticsEvent({
                    eventKey: 'dashboards_manage.duplicate',
                    eventName: 'Dashboards Manager: Dashboard Duplicated',
                    organization_id: parseInt(organization.id, 10),
                    dashboard_id: parseInt(dashboard.id, 10),
                });
                onDashboardsChange();
                indicator_1.addSuccessMessage(locale_1.t('Dashboard duplicated'));
            });
        })
            .catch(function () { return indicator_1.addErrorMessage(locale_1.t('Error duplicating Dashboard')); });
    }
    function renderMiniDashboards() {
        return dashboards === null || dashboards === void 0 ? void 0 : dashboards.map(function (dashboard, index) {
            return (<dashboardCard_1.default key={index + "-" + dashboard.id} title={dashboard.id === 'default-overview' ? 'Default Dashboard' : dashboard.title} to={{
                    pathname: "/organizations/" + organization.slug + "/dashboard/" + dashboard.id + "/",
                    query: tslib_1.__assign({}, location.query),
                }} detail={locale_1.tn('%s widget', '%s widgets', dashboard.widgetDisplay.length)} dateStatus={dashboard.dateCreated ? <timeSince_1.default date={dashboard.dateCreated}/> : undefined} createdBy={dashboard.createdBy} renderWidgets={function () { return (<WidgetGrid>
              {dashboard.widgetDisplay.map(function (displayType, i) {
                        return displayType === types_1.DisplayType.BIG_NUMBER ? (<BigNumberWidgetWrapper key={i + "-" + displayType}>
                    <WidgetImage src={miniWidget(displayType)}/>
                  </BigNumberWidgetWrapper>) : (<MiniWidgetWrapper key={i + "-" + displayType}>
                    <WidgetImage src={miniWidget(displayType)}/>
                  </MiniWidgetWrapper>);
                    })}
            </WidgetGrid>); }} renderContextMenu={function () { return (<contextMenu_1.default>
              <menuItem_1.default data-test-id="dashboard-delete" onClick={function (event) {
                        event.preventDefault();
                        handleDelete(dashboard);
                    }} disabled={dashboards.length <= 1}>
                {locale_1.t('Delete')}
              </menuItem_1.default>
              <menuItem_1.default data-test-id="dashboard-duplicate" onClick={function (event) {
                        event.preventDefault();
                        handleDuplicate(dashboard);
                    }}>
                {locale_1.t('Duplicate')}
              </menuItem_1.default>
            </contextMenu_1.default>); }}/>);
        });
    }
    function renderDashboardGrid() {
        if (!(dashboards === null || dashboards === void 0 ? void 0 : dashboards.length)) {
            return (<emptyStateWarning_1.default>
          <p>{locale_1.t('Sorry, no Dashboards match your filters.')}</p>
        </emptyStateWarning_1.default>);
        }
        return <DashboardGrid>{renderMiniDashboards()}</DashboardGrid>;
    }
    return (<react_1.Fragment>
      {renderDashboardGrid()}
      <PaginationRow pageLinks={pageLinks} onCursor={function (cursor, path, query, direction) {
            var offset = Number(cursor.split(':')[1]);
            var newQuery = tslib_1.__assign(tslib_1.__assign({}, query), { cursor: cursor });
            var isPrevious = direction === -1;
            if (offset <= 0 && isPrevious) {
                delete newQuery.cursor;
            }
            analytics_1.trackAnalyticsEvent({
                eventKey: 'dashboards_manage.paginate',
                eventName: 'Dashboards Manager: Paginate',
                organization_id: parseInt(organization.id, 10),
            });
            react_router_1.browserHistory.push({
                pathname: path,
                query: newQuery,
            });
        }}/>
    </react_1.Fragment>);
}
var DashboardGrid = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-template-rows: repeat(3, max-content);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-template-rows: repeat(3, max-content);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; });
var WidgetGrid = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n  grid-auto-flow: row dense;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(6, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(8, minmax(0, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n  grid-auto-flow: row dense;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(6, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(8, minmax(0, 1fr));\n  }\n"])), space_1.default(0.25), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[3]; }, function (p) { return p.theme.breakpoints[4]; });
var BigNumberWidgetWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  width: 100%;\n  height: 100%;\n\n  /* 2 cols */\n  grid-area: span 1 / span 2;\n\n  @media (min-width: ", ") {\n    /* 4 cols */\n    grid-area: span 1 / span 1;\n  }\n\n  @media (min-width: ", ") {\n    /* 6 and 8 cols */\n    grid-area: span 1 / span 2;\n  }\n"], ["\n  display: flex;\n  align-items: flex-start;\n  width: 100%;\n  height: 100%;\n\n  /* 2 cols */\n  grid-area: span 1 / span 2;\n\n  @media (min-width: ", ") {\n    /* 4 cols */\n    grid-area: span 1 / span 1;\n  }\n\n  @media (min-width: ", ") {\n    /* 6 and 8 cols */\n    grid-area: span 1 / span 2;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[3]; });
var MiniWidgetWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  width: 100%;\n  height: 100%;\n  grid-area: span 2 / span 2;\n"], ["\n  display: flex;\n  align-items: flex-start;\n  width: 100%;\n  height: 100%;\n  grid-area: span 2 / span 2;\n"])));
var WidgetImage = styled_1.default('img')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  height: 100%;\n"], ["\n  width: 100%;\n  height: 100%;\n"])));
var PaginationRow = styled_1.default(pagination_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(3));
exports.default = withApi_1.default(DashboardList);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=dashboardList.jsx.map