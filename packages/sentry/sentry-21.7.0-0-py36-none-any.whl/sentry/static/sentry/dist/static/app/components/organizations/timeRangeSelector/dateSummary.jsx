Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
/**
 * Displays and formats absolute DateTime ranges
 */
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var dates_1 = require("app/utils/dates");
var DateSummary = /** @class */ (function (_super) {
    tslib_1.__extends(DateSummary, _super);
    function DateSummary() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DateSummary.prototype.getFormattedDate = function (date, format) {
        return moment_1.default(date).local().format(format);
    };
    DateSummary.prototype.formatDate = function (date) {
        return this.getFormattedDate(date, 'll');
    };
    DateSummary.prototype.formatTime = function (date, withSeconds) {
        if (withSeconds === void 0) { withSeconds = false; }
        return this.getFormattedDate(date, "HH:mm" + (withSeconds ? ':ss' : ''));
    };
    DateSummary.prototype.render = function () {
        var _a = this.props, start = _a.start, end = _a.end;
        var startTimeFormatted = this.formatTime(start, true);
        var endTimeFormatted = this.formatTime(end, true);
        // Show times if either start or end date contain a time that is not midnight
        var shouldShowTimes = startTimeFormatted !== dates_1.DEFAULT_DAY_START_TIME ||
            endTimeFormatted !== dates_1.DEFAULT_DAY_END_TIME;
        return (<DateGroupWrapper hasTime={shouldShowTimes}>
        <DateGroup>
          <Date hasTime={shouldShowTimes}>
            {this.formatDate(start)}
            {shouldShowTimes && <Time>{this.formatTime(start)}</Time>}
          </Date>
        </DateGroup>
        <react_1.Fragment>
          <DateRangeDivider>{locale_1.t('to')}</DateRangeDivider>

          <DateGroup>
            <Date hasTime={shouldShowTimes}>
              {this.formatDate(end)}
              {shouldShowTimes && <Time>{this.formatTime(end)}</Time>}
            </Date>
          </DateGroup>
        </react_1.Fragment>
      </DateGroupWrapper>);
    };
    return DateSummary;
}(react_1.Component));
var DateGroupWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  transform: translateY(", ");\n"], ["\n  display: flex;\n  align-items: center;\n  transform: translateY(", ");\n"])), function (p) { return (p.hasTime ? '-5px' : '0'); });
var DateGroup = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  min-width: 110px;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  min-width: 110px;\n"])));
var Date = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", ";\n  display: flex;\n  flex-direction: column;\n  align-items: flex-end;\n"], ["\n  ", ";\n  display: flex;\n  flex-direction: column;\n  align-items: flex-end;\n"])), function (p) { return p.hasTime && 'margin-top: 9px'; });
var Time = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: 0.7em;\n  line-height: 0.7em;\n  opacity: 0.5;\n"], ["\n  font-size: 0.7em;\n  line-height: 0.7em;\n  opacity: 0.5;\n"])));
var DateRangeDivider = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin: 0 ", ";\n"], ["\n  margin: 0 ", ";\n"])), space_1.default(0.5));
exports.default = DateSummary;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=dateSummary.jsx.map