Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pluginIcon_1 = tslib_1.__importStar(require("app/plugins/components/pluginIcon"));
var StyledIcon = styled_1.default('img')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  height: ", "px;\n  width: ", "px;\n  border-radius: 2px;\n  display: block;\n"], ["\n  height: ", "px;\n  width: ", "px;\n  border-radius: 2px;\n  display: block;\n"])), function (p) { return p.size; }, function (p) { return p.size; });
var Icon = /** @class */ (function (_super) {
    tslib_1.__extends(Icon, _super);
    function Icon() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            imgSrc: _this.props.integration.icon,
        };
        return _this;
    }
    Icon.prototype.render = function () {
        var _this = this;
        var _a = this.props, integration = _a.integration, size = _a.size;
        return (<StyledIcon size={size} src={this.state.imgSrc} onError={function () {
                _this.setState({ imgSrc: pluginIcon_1.ICON_PATHS[integration.provider.key] || pluginIcon_1.DEFAULT_ICON });
            }}/>);
    };
    return Icon;
}(react_1.Component));
var IntegrationIcon = function (_a) {
    var integration = _a.integration, _b = _a.size, size = _b === void 0 ? 32 : _b;
    return integration.icon ? (<Icon size={size} integration={integration}/>) : (<pluginIcon_1.default size={size} pluginId={integration.provider.key}/>);
};
exports.default = IntegrationIcon;
var templateObject_1;
//# sourceMappingURL=integrationIcon.jsx.map