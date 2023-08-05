Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var ReactRouter = tslib_1.__importStar(require("react-router"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var featureBadge_1 = tslib_1.__importDefault(require("app/components/featureBadge"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var localStorage_1 = tslib_1.__importDefault(require("app/utils/localStorage"));
var LabelHook = hookOrDefault_1.default({
    hookName: 'sidebar:item-label',
    defaultComponent: function (_a) {
        var children = _a.children;
        return <React.Fragment>{children}</React.Fragment>;
    },
});
var SidebarItem = function (_a) {
    var _b, _c;
    var router = _a.router, id = _a.id, href = _a.href, to = _a.to, icon = _a.icon, label = _a.label, badge = _a.badge, active = _a.active, hasPanel = _a.hasPanel, isNew = _a.isNew, isBeta = _a.isBeta, collapsed = _a.collapsed, className = _a.className, orientation = _a.orientation, isNewSeenKeySuffix = _a.isNewSeenKeySuffix, onClick = _a.onClick, props = tslib_1.__rest(_a, ["router", "id", "href", "to", "icon", "label", "badge", "active", "hasPanel", "isNew", "isBeta", "collapsed", "className", "orientation", "isNewSeenKeySuffix", "onClick"]);
    // label might be wrapped in a guideAnchor
    var labelString = label;
    if (React.isValidElement(label)) {
        labelString = (_c = (_b = label === null || label === void 0 ? void 0 : label.props) === null || _b === void 0 ? void 0 : _b.children) !== null && _c !== void 0 ? _c : label;
    }
    // If there is no active panel open and if path is active according to react-router
    var isActiveRouter = (!hasPanel && router && to && location.pathname.startsWith(to)) ||
        (labelString === 'Discover' && location.pathname.includes('/discover/')) ||
        (labelString === 'Dashboards' &&
            (location.pathname.includes('/dashboards/') ||
                location.pathname.includes('/dashboard/'))) ||
        // TODO: this won't be necessary once we remove settingsHome
        (labelString === 'Settings' && location.pathname.startsWith('/settings/')) ||
        (labelString === 'Alerts' &&
            location.pathname.includes('/alerts/') &&
            !location.pathname.startsWith('/settings/'));
    var isActive = active || isActiveRouter;
    var isTop = orientation === 'top';
    var placement = isTop ? 'bottom' : 'right';
    var seenSuffix = isNewSeenKeySuffix !== null && isNewSeenKeySuffix !== void 0 ? isNewSeenKeySuffix : '';
    var isNewSeenKey = "sidebar-new-seen:" + id + seenSuffix;
    var showIsNew = isNew && !localStorage_1.default.getItem(isNewSeenKey);
    return (<tooltip_1.default disabled={!collapsed} title={label} position={placement}>
      <StyledSidebarItem data-test-id={props['data-test-id']} active={isActive ? 'true' : undefined} to={(to ? to : href) || '#'} className={className} onClick={function (event) {
            !(to || href) && event.preventDefault();
            typeof onClick === 'function' && onClick(id, event);
            showIsNew && localStorage_1.default.setItem(isNewSeenKey, 'true');
        }}>
        <SidebarItemWrapper>
          <SidebarItemIcon>{icon}</SidebarItemIcon>
          {!collapsed && !isTop && (<SidebarItemLabel>
              <LabelHook id={id}>
                <textOverflow_1.default>{label}</textOverflow_1.default>
                {showIsNew && <featureBadge_1.default type="new" noTooltip/>}
                {isBeta && <featureBadge_1.default type="beta" noTooltip/>}
              </LabelHook>
            </SidebarItemLabel>)}
          {collapsed && showIsNew && <CollapsedFeatureBadge type="new"/>}
          {collapsed && isBeta && <CollapsedFeatureBadge type="beta"/>}
          {badge !== undefined && badge > 0 && (<SidebarItemBadge collapsed={collapsed}>{badge}</SidebarItemBadge>)}
        </SidebarItemWrapper>
      </StyledSidebarItem>
    </tooltip_1.default>);
};
exports.default = ReactRouter.withRouter(SidebarItem);
var getActiveStyle = function (_a) {
    var active = _a.active, theme = _a.theme;
    if (!active) {
        return '';
    }
    return react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n    color: ", ";\n\n    &:active,\n    &:focus,\n    &:hover {\n      color: ", ";\n    }\n\n    &:before {\n      background-color: ", ";\n    }\n  "], ["\n    color: ", ";\n\n    &:active,\n    &:focus,\n    &:hover {\n      color: ", ";\n    }\n\n    &:before {\n      background-color: ", ";\n    }\n  "])), theme === null || theme === void 0 ? void 0 : theme.white, theme === null || theme === void 0 ? void 0 : theme.white, theme === null || theme === void 0 ? void 0 : theme.active);
};
var StyledSidebarItem = styled_1.default(link_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  color: inherit;\n  position: relative;\n  cursor: pointer;\n  font-size: 15px;\n  line-height: 32px;\n  height: 34px;\n  flex-shrink: 0;\n\n  transition: 0.15s color linear;\n\n  &:before {\n    display: block;\n    content: '';\n    position: absolute;\n    top: 4px;\n    left: -20px;\n    bottom: 6px;\n    width: 5px;\n    border-radius: 0 3px 3px 0;\n    background-color: transparent;\n    transition: 0.15s background-color linear;\n  }\n\n  @media (max-width: ", ") {\n    margin: 0 4px;\n\n    &:before {\n      top: auto;\n      left: 5px;\n      bottom: -10px;\n      height: 5px;\n      width: auto;\n      right: 5px;\n      border-radius: 3px 3px 0 0;\n    }\n  }\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n\n  &.focus-visible {\n    outline: none;\n    background: #584c66;\n    padding: 0 19px;\n    margin: 0 -19px;\n\n    &:before {\n      left: 0;\n    }\n  }\n\n  ", ";\n"], ["\n  display: flex;\n  color: inherit;\n  position: relative;\n  cursor: pointer;\n  font-size: 15px;\n  line-height: 32px;\n  height: 34px;\n  flex-shrink: 0;\n\n  transition: 0.15s color linear;\n\n  &:before {\n    display: block;\n    content: '';\n    position: absolute;\n    top: 4px;\n    left: -20px;\n    bottom: 6px;\n    width: 5px;\n    border-radius: 0 3px 3px 0;\n    background-color: transparent;\n    transition: 0.15s background-color linear;\n  }\n\n  @media (max-width: ", ") {\n    margin: 0 4px;\n\n    &:before {\n      top: auto;\n      left: 5px;\n      bottom: -10px;\n      height: 5px;\n      width: auto;\n      right: 5px;\n      border-radius: 3px 3px 0 0;\n    }\n  }\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n\n  &.focus-visible {\n    outline: none;\n    background: #584c66;\n    padding: 0 19px;\n    margin: 0 -19px;\n\n    &:before {\n      left: 0;\n    }\n  }\n\n  ", ";\n"])), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.gray200; }, getActiveStyle);
var SidebarItemWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  width: 100%;\n"], ["\n  display: flex;\n  align-items: center;\n  width: 100%;\n"])));
var SidebarItemIcon = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  content: '';\n  display: inline-flex;\n  width: 32px;\n  height: 22px;\n  font-size: 20px;\n  align-items: center;\n  flex-shrink: 0;\n\n  svg {\n    display: block;\n    margin: 0 auto;\n  }\n"], ["\n  content: '';\n  display: inline-flex;\n  width: 32px;\n  height: 22px;\n  font-size: 20px;\n  align-items: center;\n  flex-shrink: 0;\n\n  svg {\n    display: block;\n    margin: 0 auto;\n  }\n"])));
var SidebarItemLabel = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-left: 12px;\n  white-space: nowrap;\n  opacity: 1;\n  flex: 1;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  margin-left: 12px;\n  white-space: nowrap;\n  opacity: 1;\n  flex: 1;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"])));
var getCollapsedBadgeStyle = function (_a) {
    var collapsed = _a.collapsed, theme = _a.theme;
    if (!collapsed) {
        return '';
    }
    return react_1.css(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n    text-indent: -99999em;\n    position: absolute;\n    right: 0;\n    top: 1px;\n    background: ", ";\n    width: ", ";\n    height: ", ";\n    border-radius: ", ";\n    line-height: ", ";\n    box-shadow: 0 3px 3px ", ";\n  "], ["\n    text-indent: -99999em;\n    position: absolute;\n    right: 0;\n    top: 1px;\n    background: ", ";\n    width: ", ";\n    height: ", ";\n    border-radius: ", ";\n    line-height: ", ";\n    box-shadow: 0 3px 3px ", ";\n  "])), theme.red300, theme.sidebar.smallBadgeSize, theme.sidebar.smallBadgeSize, theme.sidebar.smallBadgeSize, theme.sidebar.smallBadgeSize, theme.sidebar.background);
};
var SidebarItemBadge = styled_1.default(function (_a) {
    var _ = _a.collapsed, props = tslib_1.__rest(_a, ["collapsed"]);
    return <span {...props}/>;
})(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: block;\n  text-align: center;\n  color: ", ";\n  font-size: 12px;\n  background: ", ";\n  width: ", ";\n  height: ", ";\n  border-radius: ", ";\n  line-height: ", ";\n\n  ", ";\n"], ["\n  display: block;\n  text-align: center;\n  color: ", ";\n  font-size: 12px;\n  background: ", ";\n  width: ", ";\n  height: ", ";\n  border-radius: ", ";\n  line-height: ", ";\n\n  ", ";\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.red300; }, function (p) { return p.theme.sidebar.badgeSize; }, function (p) { return p.theme.sidebar.badgeSize; }, function (p) { return p.theme.sidebar.badgeSize; }, function (p) { return p.theme.sidebar.badgeSize; }, getCollapsedBadgeStyle);
var CollapsedFeatureBadge = styled_1.default(featureBadge_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  right: 0;\n"], ["\n  position: absolute;\n  top: 0;\n  right: 0;\n"])));
CollapsedFeatureBadge.defaultProps = {
    variant: 'indicator',
    noTooltip: true,
};
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=sidebarItem.jsx.map