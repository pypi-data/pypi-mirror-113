Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var ReactRouter = tslib_1.__importStar(require("react-router"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var checkbox_1 = tslib_1.__importDefault(require("app/components/checkbox"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var timePicker_1 = tslib_1.__importDefault(require("app/components/organizations/timeRangeSelector/timePicker"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var dates_1 = require("app/utils/dates");
var getRouteStringFromRoutes_1 = tslib_1.__importDefault(require("app/utils/getRouteStringFromRoutes"));
var DateRangePicker = React.lazy(function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('./dateRangeWrapper')); }); });
var getTimeStringFromDate = function (date) { return moment_1.default(date).local().format('HH:mm'); };
function isRangeSelection(maybe) {
    return maybe.selection !== undefined;
}
var defaultProps = {
    showAbsolute: true,
    showRelative: false,
    /**
     * The maximum number of days in the past you can pick
     */
    maxPickableDays: constants_1.MAX_PICKABLE_DAYS,
};
var DateRange = /** @class */ (function (_super) {
    tslib_1.__extends(DateRange, _super);
    function DateRange() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            hasStartErrors: false,
            hasEndErrors: false,
        };
        _this.handleSelectDateRange = function (changeProps) {
            if (!isRangeSelection(changeProps)) {
                return;
            }
            var selection = changeProps.selection;
            var onChange = _this.props.onChange;
            var startDate = selection.startDate, endDate = selection.endDate;
            var end = endDate ? dates_1.getEndOfDay(endDate) : endDate;
            onChange({
                start: startDate,
                end: end,
            });
        };
        _this.handleChangeStart = function (e) {
            var _a, _b;
            // Safari does not support "time" inputs, so we don't have access to
            // `e.target.valueAsDate`, must parse as string
            //
            // Time will be in 24hr e.g. "21:00"
            var start = (_a = _this.props.start) !== null && _a !== void 0 ? _a : '';
            var end = (_b = _this.props.end) !== null && _b !== void 0 ? _b : undefined;
            var _c = _this.props, onChange = _c.onChange, organization = _c.organization, router = _c.router;
            var startTime = e.target.value;
            if (!startTime || !dates_1.isValidTime(startTime)) {
                _this.setState({ hasStartErrors: true });
                onChange({ hasDateRangeErrors: true });
                return;
            }
            var newTime = dates_1.setDateToTime(start, startTime, { local: true });
            analytics_1.analytics('dateselector.time_changed', {
                field_changed: 'start',
                time: startTime,
                path: getRouteStringFromRoutes_1.default(router.routes),
                org_id: parseInt(organization.id, 10),
            });
            onChange({
                start: newTime,
                end: end,
                hasDateRangeErrors: _this.state.hasEndErrors,
            });
            _this.setState({ hasStartErrors: false });
        };
        _this.handleChangeEnd = function (e) {
            var _a, _b;
            var start = (_a = _this.props.start) !== null && _a !== void 0 ? _a : undefined;
            var end = (_b = _this.props.end) !== null && _b !== void 0 ? _b : '';
            var _c = _this.props, organization = _c.organization, onChange = _c.onChange, router = _c.router;
            var endTime = e.target.value;
            if (!endTime || !dates_1.isValidTime(endTime)) {
                _this.setState({ hasEndErrors: true });
                onChange({ hasDateRangeErrors: true });
                return;
            }
            var newTime = dates_1.setDateToTime(end, endTime, { local: true });
            analytics_1.analytics('dateselector.time_changed', {
                field_changed: 'end',
                time: endTime,
                path: getRouteStringFromRoutes_1.default(router.routes),
                org_id: parseInt(organization.id, 10),
            });
            onChange({
                start: start,
                end: newTime,
                hasDateRangeErrors: _this.state.hasStartErrors,
            });
            _this.setState({ hasEndErrors: false });
        };
        return _this;
    }
    DateRange.prototype.render = function () {
        var _a, _b;
        var _c = this.props, className = _c.className, maxPickableDays = _c.maxPickableDays, utc = _c.utc, showTimePicker = _c.showTimePicker, onChangeUtc = _c.onChangeUtc, theme = _c.theme;
        var start = (_a = this.props.start) !== null && _a !== void 0 ? _a : '';
        var end = (_b = this.props.end) !== null && _b !== void 0 ? _b : '';
        var startTime = getTimeStringFromDate(new Date(start));
        var endTime = getTimeStringFromDate(new Date(end));
        // Restraints on the time range that you can select
        // Can't select dates in the future b/c we're not fortune tellers (yet)
        //
        // We want `maxPickableDays` - 1 (if today is Jan 5, max is 3 days, the minDate should be Jan 3)
        // Subtract additional day  because we force the end date to be inclusive,
        // so when you pick Jan 1 the time becomes Jan 1 @ 23:59:59,
        // (or really, Jan 2 @ 00:00:00 - 1 second), while the start time is at 00:00
        var minDate = dates_1.getStartOfPeriodAgo('days', (maxPickableDays !== null && maxPickableDays !== void 0 ? maxPickableDays : constants_1.MAX_PICKABLE_DAYS) - 2);
        var maxDate = new Date();
        return (<div className={className} data-test-id="date-range">
        <React.Suspense fallback={<placeholder_1.default width="342px" height="254px">
              <loadingIndicator_1.default />
            </placeholder_1.default>}>
          <DateRangePicker rangeColors={[theme.purple300]} ranges={[
                {
                    startDate: moment_1.default(start).local().toDate(),
                    endDate: moment_1.default(end).local().toDate(),
                    key: 'selection',
                },
            ]} minDate={minDate} maxDate={maxDate} onChange={this.handleSelectDateRange}/>
        </React.Suspense>
        {showTimePicker && (<TimeAndUtcPicker>
            <timePicker_1.default start={startTime} end={endTime} onChangeStart={this.handleChangeStart} onChangeEnd={this.handleChangeEnd}/>
            <UtcPicker>
              {locale_1.t('Use UTC')}
              <checkbox_1.default onChange={onChangeUtc} checked={utc || false} style={{
                    margin: '0 0 0 0.5em',
                }}/>
            </UtcPicker>
          </TimeAndUtcPicker>)}
      </div>);
    };
    DateRange.defaultProps = defaultProps;
    return DateRange;
}(React.Component));
var StyledDateRange = styled_1.default(react_1.withTheme(ReactRouter.withRouter(DateRange)))(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  border-left: 1px solid ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  border-left: 1px solid ", ";\n"])), function (p) { return p.theme.border; });
var TimeAndUtcPicker = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  border-top: 1px solid ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  border-top: 1px solid ", ";\n"])), space_1.default(2), function (p) { return p.theme.innerBorder; });
var UtcPicker = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  white-space: nowrap;\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n  flex: 1;\n"], ["\n  color: ", ";\n  white-space: nowrap;\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n  flex: 1;\n"])), function (p) { return p.theme.gray300; });
exports.default = StyledDateRange;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map