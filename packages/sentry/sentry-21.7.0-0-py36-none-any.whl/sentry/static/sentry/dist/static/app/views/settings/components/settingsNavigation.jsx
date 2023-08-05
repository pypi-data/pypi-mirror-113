Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var settingsNavigationGroup_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsNavigationGroup"));
var SettingsNavigation = /** @class */ (function (_super) {
    tslib_1.__extends(SettingsNavigation, _super);
    function SettingsNavigation() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SettingsNavigation.prototype.componentDidCatch = function (error, errorInfo) {
        Sentry.withScope(function (scope) {
            Object.keys(errorInfo).forEach(function (key) {
                scope.setExtra(key, errorInfo[key]);
            });
            scope.setExtra('url', window.location.href);
            Sentry.captureException(error);
        });
    };
    SettingsNavigation.prototype.render = function () {
        var _a = this.props, navigationObjects = _a.navigationObjects, hooks = _a.hooks, hookConfigs = _a.hookConfigs, stickyTop = _a.stickyTop, otherProps = tslib_1.__rest(_a, ["navigationObjects", "hooks", "hookConfigs", "stickyTop"]);
        var navWithHooks = navigationObjects.concat(hookConfigs);
        return (<PositionStickyWrapper stickyTop={stickyTop}>
        {navWithHooks.map(function (config) { return (<settingsNavigationGroup_1.default key={config.name} {...otherProps} {...config}/>); })}
        {hooks.map(function (Hook, i) { return React.cloneElement(Hook, { key: "hook-" + i }); })}
      </PositionStickyWrapper>);
    };
    SettingsNavigation.defaultProps = {
        hooks: [],
        hookConfigs: [],
        stickyTop: '69px',
    };
    return SettingsNavigation;
}(React.Component));
var PositionStickyWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  padding-right: ", ";\n\n  @media (min-width: ", ") {\n    position: sticky;\n    top: ", ";\n    overflow: scroll;\n    -ms-overflow-style: none;\n    scrollbar-width: none;\n\n    &::-webkit-scrollbar {\n      display: none;\n    }\n  }\n"], ["\n  padding: ", ";\n  padding-right: ", ";\n\n  @media (min-width: ", ") {\n    position: sticky;\n    top: ", ";\n    overflow: scroll;\n    -ms-overflow-style: none;\n    scrollbar-width: none;\n\n    &::-webkit-scrollbar {\n      display: none;\n    }\n  }\n"])), space_1.default(4), space_1.default(2), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.stickyTop; });
exports.default = SettingsNavigation;
var templateObject_1;
//# sourceMappingURL=settingsNavigation.jsx.map