Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var icons_1 = require("app/icons");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var utils_2 = require("../utils");
var CRASH_FREE_DANGER_THRESHOLD = 98;
var CRASH_FREE_WARNING_THRESHOLD = 99.5;
var getIcon = function (percent, iconSize) {
    if (percent < CRASH_FREE_DANGER_THRESHOLD) {
        return <icons_1.IconFire color="red300" size={iconSize}/>;
    }
    if (percent < CRASH_FREE_WARNING_THRESHOLD) {
        return <icons_1.IconWarning color="yellow300" size={iconSize}/>;
    }
    return <icons_1.IconCheckmark isCircled color="green300" size={iconSize}/>;
};
var CrashFree = function (_a) {
    var percent = _a.percent, _b = _a.iconSize, iconSize = _b === void 0 ? 'sm' : _b, displayOption = _a.displayOption;
    return (<Wrapper>
      {getIcon(percent, iconSize)}
      <CrashFreePercent>
        {utils_2.displayCrashFreePercent(percent)}{' '}
        {utils_1.defined(displayOption) && utils_2.releaseDisplayLabel(displayOption, 2)}
      </CrashFreePercent>
    </Wrapper>);
};
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  align-items: center;\n  vertical-align: middle;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  align-items: center;\n  vertical-align: middle;\n"])), space_1.default(1));
var CrashFreePercent = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis_1.default);
exports.default = CrashFree;
var templateObject_1, templateObject_2;
//# sourceMappingURL=crashFree.jsx.map