Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var badge_1 = tslib_1.__importDefault(require("app/components/badge"));
var featureBadge_1 = tslib_1.__importDefault(require("app/components/featureBadge"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var SettingsNavItem = function (_a) {
    var badge = _a.badge, label = _a.label, index = _a.index, id = _a.id, props = tslib_1.__rest(_a, ["badge", "label", "index", "id"]);
    var LabelHook = hookOrDefault_1.default({
        hookName: 'sidebar:item-label',
        defaultComponent: function (_a) {
            var children = _a.children;
            return <React.Fragment>{children}</React.Fragment>;
        },
    });
    var renderedBadge;
    if (badge === 'new') {
        renderedBadge = <featureBadge_1.default type="new"/>;
    }
    else if (badge === 'beta') {
        renderedBadge = <featureBadge_1.default type="beta"/>;
    }
    else if (badge === 'warning') {
        renderedBadge = (<tooltip_1.default title={locale_1.t('This settings needs review')} position="right">
        <StyledBadge text={badge} type="warning"/>
      </tooltip_1.default>);
    }
    else {
        renderedBadge = <StyledBadge text={badge}/>;
    }
    return (<StyledNavItem onlyActiveOnIndex={index} activeClassName="active" {...props}>
      <LabelHook id={id}>{label}</LabelHook>
      {badge ? renderedBadge : null}
    </StyledNavItem>);
};
var StyledNavItem = styled_1.default(react_router_1.Link)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: block;\n  color: ", ";\n  font-size: 14px;\n  line-height: 30px;\n  position: relative;\n\n  &.active {\n    color: ", ";\n\n    &:before {\n      background: ", ";\n    }\n  }\n\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n    outline: none;\n  }\n\n  &.focus-visible {\n    outline: none;\n    background: ", ";\n    padding-left: 15px;\n    margin-left: -15px;\n    border-radius: 3px;\n\n    &:before {\n      left: -15px;\n    }\n  }\n\n  &:before {\n    position: absolute;\n    content: '';\n    display: block;\n    top: 4px;\n    left: -30px;\n    height: 20px;\n    width: 4px;\n    background: transparent;\n    border-radius: 0 2px 2px 0;\n  }\n"], ["\n  display: block;\n  color: ", ";\n  font-size: 14px;\n  line-height: 30px;\n  position: relative;\n\n  &.active {\n    color: ", ";\n\n    &:before {\n      background: ", ";\n    }\n  }\n\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n    outline: none;\n  }\n\n  &.focus-visible {\n    outline: none;\n    background: ", ";\n    padding-left: 15px;\n    margin-left: -15px;\n    border-radius: 3px;\n\n    &:before {\n      left: -15px;\n    }\n  }\n\n  &:before {\n    position: absolute;\n    content: '';\n    display: block;\n    top: 4px;\n    left: -30px;\n    height: 20px;\n    width: 4px;\n    background: transparent;\n    border-radius: 0 2px 2px 0;\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.active; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.backgroundSecondary; });
var StyledBadge = styled_1.default(badge_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-weight: 400;\n  height: auto;\n  line-height: 1;\n  font-size: ", ";\n  padding: 3px ", ";\n"], ["\n  font-weight: 400;\n  height: auto;\n  line-height: 1;\n  font-size: ", ";\n  padding: 3px ", ";\n"])), function (p) { return p.theme.fontSizeExtraSmall; }, space_1.default(0.75));
exports.default = SettingsNavItem;
var templateObject_1, templateObject_2;
//# sourceMappingURL=settingsNavItem.jsx.map