Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var analytics_1 = require("app/utils/analytics");
var replaceRouterParams_1 = tslib_1.__importDefault(require("app/utils/replaceRouterParams"));
var settingsNavItem_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsNavItem"));
var SettingsNavigationGroup = function (props) {
    var organization = props.organization, project = props.project, name = props.name, items = props.items;
    var navLinks = items.map(function (_a) {
        var path = _a.path, title = _a.title, index = _a.index, show = _a.show, badge = _a.badge, id = _a.id, recordAnalytics = _a.recordAnalytics;
        if (typeof show === 'function' && !show(props)) {
            return null;
        }
        if (typeof show !== 'undefined' && !show) {
            return null;
        }
        var badgeResult = typeof badge === 'function' ? badge(props) : null;
        var to = replaceRouterParams_1.default(path, tslib_1.__assign(tslib_1.__assign({}, (organization ? { orgId: organization.slug } : {})), (project ? { projectId: project.slug } : {})));
        var handleClick = function () {
            // only call the analytics event if the URL is changing
            if (recordAnalytics && to !== window.location.pathname) {
                analytics_1.trackAnalyticsEvent({
                    organization_id: organization ? organization.id : null,
                    project_id: project && project.id,
                    eventName: 'Sidebar Item Clicked',
                    eventKey: 'sidebar.item_clicked',
                    sidebar_item_id: id,
                    dest: path,
                });
            }
        };
        return (<settingsNavItem_1.default key={title} to={to} label={title} index={index} badge={badgeResult} id={id} onClick={handleClick}/>);
    });
    if (!navLinks.some(function (link) { return link !== null; })) {
        return null;
    }
    return (<NavSection data-test-id={name}>
      <SettingsHeading>{name}</SettingsHeading>
      {navLinks}
    </NavSection>);
};
var NavSection = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 20px;\n"], ["\n  margin-bottom: 20px;\n"])));
var SettingsHeading = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: 12px;\n  font-weight: 600;\n  text-transform: uppercase;\n  margin-bottom: 20px;\n"], ["\n  color: ", ";\n  font-size: 12px;\n  font-weight: 600;\n  text-transform: uppercase;\n  margin-bottom: 20px;\n"])), function (p) { return p.theme.subText; });
exports.default = SettingsNavigationGroup;
var templateObject_1, templateObject_2;
//# sourceMappingURL=settingsNavigationGroup.jsx.map