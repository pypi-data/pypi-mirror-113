Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var FEATURE_TOOLTIPS = {
    symtab: locale_1.t('Symbol tables are used as a fallback when full debug information is not available'),
    debug: locale_1.t('Debug information provides function names and resolves inlined frames during symbolication'),
    unwind: locale_1.t('Stack unwinding information improves the quality of stack traces extracted from minidumps'),
    sources: locale_1.t('Source code information allows Sentry to display source code context for stack frames'),
};
var DebugFileFeature = function (_a) {
    var _b = _a.available, available = _b === void 0 ? true : _b, feature = _a.feature;
    var tooltipText = FEATURE_TOOLTIPS[feature];
    if (available === true) {
        return (<StyledTag type="success" tooltipText={tooltipText} icon={<icons_1.IconCheckmark />}>
        {feature}
      </StyledTag>);
    }
    return (<StyledTag type="error" tooltipText={tooltipText} icon={<icons_1.IconClose />}>
      {feature}
    </StyledTag>);
};
exports.default = DebugFileFeature;
var StyledTag = styled_1.default(tag_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var templateObject_1;
//# sourceMappingURL=debugFileFeature.jsx.map