Object.defineProperty(exports, "__esModule", { value: true });
exports.PackageStatusIcon = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var PackageStatus = function (_a) {
    var status = _a.status, tooltip = _a.tooltip;
    var getIcon = function () {
        switch (status) {
            case 'success':
                return <icons_1.IconCheckmark isCircled color="green300" size="xs"/>;
            case 'empty':
                return <icons_1.IconCircle size="xs"/>;
            case 'error':
            default:
                return <icons_1.IconFlag color="red300" size="xs"/>;
        }
    };
    var icon = getIcon();
    if (status === 'empty') {
        return null;
    }
    return (<StyledTooltip title={tooltip} disabled={!(tooltip && tooltip.length)} containerDisplayMode="inline-flex">
      <exports.PackageStatusIcon>{icon}</exports.PackageStatusIcon>
    </StyledTooltip>);
};
var StyledTooltip = styled_1.default(tooltip_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(0.75));
exports.PackageStatusIcon = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: 12px;\n  align-items: center;\n  cursor: pointer;\n  visibility: hidden;\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n"], ["\n  height: 12px;\n  align-items: center;\n  cursor: pointer;\n  visibility: hidden;\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
exports.default = PackageStatus;
var templateObject_1, templateObject_2;
//# sourceMappingURL=packageStatus.jsx.map