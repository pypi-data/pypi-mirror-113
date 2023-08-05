Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var relativeSelector_1 = tslib_1.__importDefault(require("app/components/organizations/timeRangeSelector/dateRange/relativeSelector"));
var selectorItem_1 = tslib_1.__importDefault(require("app/components/organizations/timeRangeSelector/dateRange/selectorItem"));
var locale_1 = require("app/locale");
var SelectorItems = function (_a) {
    var shouldShowRelative = _a.shouldShowRelative, shouldShowAbsolute = _a.shouldShowAbsolute, handleSelectRelative = _a.handleSelectRelative, handleAbsoluteClick = _a.handleAbsoluteClick, relativeSelected = _a.relativeSelected, relativePeriods = _a.relativePeriods, isAbsoluteSelected = _a.isAbsoluteSelected;
    return (<React.Fragment>
    {shouldShowRelative && (<relativeSelector_1.default onClick={handleSelectRelative} selected={relativeSelected} relativePeriods={relativePeriods}/>)}
    {shouldShowAbsolute && (<selectorItem_1.default onClick={handleAbsoluteClick} value="absolute" label={locale_1.t('Absolute date')} selected={isAbsoluteSelected} last/>)}
  </React.Fragment>);
};
exports.default = SelectorItems;
//# sourceMappingURL=selectorItems.jsx.map