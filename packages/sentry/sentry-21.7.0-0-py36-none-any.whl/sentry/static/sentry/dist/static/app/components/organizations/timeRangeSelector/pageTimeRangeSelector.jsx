Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var timeRangeSelector_1 = tslib_1.__importDefault(require("app/components/organizations/timeRangeSelector"));
var panels_1 = require("app/components/panels");
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function PageTimeRangeSelector(_a) {
    var className = _a.className, props = tslib_1.__rest(_a, ["className"]);
    var _b = tslib_1.__read(react_1.useState(false), 2), isCalendarOpen = _b[0], setIsCalendarOpen = _b[1];
    return (<DropdownDate className={className} isCalendarOpen={isCalendarOpen}>
      <timeRangeSelector_1.default key={"period:" + props.relative + "-start:" + props.start + "-end:" + props.end + "-utc:" + props.utc + "-defaultPeriod:" + props.defaultPeriod} label={<DropdownLabel>{locale_1.t('Date Range:')}</DropdownLabel>} onToggleSelector={function (isOpen) { return setIsCalendarOpen(isOpen); }} relativeOptions={constants_1.DEFAULT_RELATIVE_PERIODS} {...props}/>
    </DropdownDate>);
}
var DropdownDate = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  height: 42px;\n\n  background: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  padding: 0;\n  margin: 0;\n  font-size: ", ";\n  color: ", ";\n\n  /* TimeRangeRoot in TimeRangeSelector */\n  > div {\n    width: 100%;\n    align-self: stretch;\n  }\n\n  /* StyledItemHeader used to show selected value of TimeRangeSelector */\n  > div > div:first-child {\n    padding: 0 ", ";\n  }\n\n  /* Menu that dropdowns from TimeRangeSelector */\n  > div > div:last-child {\n    /* Remove awkward 1px width difference on dropdown due to border */\n    box-sizing: content-box;\n    font-size: 1em;\n  }\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  height: 42px;\n\n  background: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  padding: 0;\n  margin: 0;\n  font-size: ", ";\n  color: ", ";\n\n  /* TimeRangeRoot in TimeRangeSelector */\n  > div {\n    width: 100%;\n    align-self: stretch;\n  }\n\n  /* StyledItemHeader used to show selected value of TimeRangeSelector */\n  > div > div:first-child {\n    padding: 0 ", ";\n  }\n\n  /* Menu that dropdowns from TimeRangeSelector */\n  > div > div:last-child {\n    /* Remove awkward 1px width difference on dropdown due to border */\n    box-sizing: content-box;\n    font-size: 1em;\n  }\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) {
    return p.isCalendarOpen
        ? p.theme.borderRadius + " " + p.theme.borderRadius + " 0 0"
        : p.theme.borderRadius;
}, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.textColor; }, space_1.default(2));
var DropdownLabel = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  text-align: left;\n  font-weight: 600;\n  color: ", ";\n\n  > span:last-child {\n    font-weight: 400;\n  }\n"], ["\n  text-align: left;\n  font-weight: 600;\n  color: ", ";\n\n  > span:last-child {\n    font-weight: 400;\n  }\n"])), function (p) { return p.theme.textColor; });
exports.default = PageTimeRangeSelector;
var templateObject_1, templateObject_2;
//# sourceMappingURL=pageTimeRangeSelector.jsx.map