Object.defineProperty(exports, "__esModule", { value: true });
exports.TimeRangeRoot = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var ReactRouter = tslib_1.__importStar(require("react-router"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_timezone_1 = tslib_1.__importDefault(require("moment-timezone"));
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
var headerItem_1 = tslib_1.__importDefault(require("app/components/organizations/headerItem"));
var multipleSelectorSubmitRow_1 = tslib_1.__importDefault(require("app/components/organizations/multipleSelectorSubmitRow"));
var dateRange_1 = tslib_1.__importDefault(require("app/components/organizations/timeRangeSelector/dateRange"));
var selectorItems_1 = tslib_1.__importDefault(require("app/components/organizations/timeRangeSelector/dateRange/selectorItems"));
var dateSummary_1 = tslib_1.__importDefault(require("app/components/organizations/timeRangeSelector/dateSummary"));
var utils_1 = require("app/components/organizations/timeRangeSelector/utils");
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_2 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var dates_1 = require("app/utils/dates");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var getRouteStringFromRoutes_1 = tslib_1.__importDefault(require("app/utils/getRouteStringFromRoutes"));
// Strips timezone from local date, creates a new moment date object with timezone
// Then returns as a Date object
var getDateWithTimezoneInUtc = function (date, utc) {
    return moment_timezone_1.default
        .tz(moment_timezone_1.default(date).local().format('YYYY-MM-DD HH:mm:ss'), utc ? 'UTC' : dates_1.getUserTimezone())
        .utc()
        .toDate();
};
var getInternalDate = function (date, utc) {
    if (utc) {
        return dates_1.getUtcToSystem(date);
    }
    else {
        return new Date(moment_timezone_1.default.tz(moment_timezone_1.default.utc(date), dates_1.getUserTimezone()).format('YYYY/MM/DD HH:mm:ss'));
    }
};
var DateRangeHook = hookOrDefault_1.default({
    hookName: 'component:header-date-range',
    defaultComponent: dateRange_1.default,
});
var SelectorItemsHook = hookOrDefault_1.default({
    hookName: 'component:header-selector-items',
    defaultComponent: selectorItems_1.default,
});
var defaultProps = {
    /**
     * Show absolute date selectors
     */
    showAbsolute: true,
    /**
     * Show relative date selectors
     */
    showRelative: true,
    /**
     * When the default period is selected, it is visually dimmed and
     * makes the selector unclearable.
     */
    defaultPeriod: constants_1.DEFAULT_STATS_PERIOD,
    /**
     * Callback when value changes
     */
    onChange: (function () { }),
};
var TimeRangeSelector = /** @class */ (function (_super) {
    tslib_1.__extends(TimeRangeSelector, _super);
    function TimeRangeSelector(props) {
        var _this = _super.call(this, props) || this;
        _this.callCallback = function (callback, datetime) {
            if (typeof callback !== 'function') {
                return;
            }
            if (!datetime.start && !datetime.end) {
                callback(datetime);
                return;
            }
            // Change local date into either UTC or local time (local time defined by user preference)
            callback(tslib_1.__assign(tslib_1.__assign({}, datetime), { start: getDateWithTimezoneInUtc(datetime.start, _this.state.utc), end: getDateWithTimezoneInUtc(datetime.end, _this.state.utc) }));
        };
        _this.handleCloseMenu = function () {
            var _a = _this.state, relative = _a.relative, start = _a.start, end = _a.end, utc = _a.utc;
            if (_this.state.hasChanges) {
                // Only call update if we close when absolute date is selected
                _this.handleUpdate({ relative: relative, start: start, end: end, utc: utc });
            }
            else {
                _this.setState({ isOpen: false });
            }
        };
        _this.handleUpdate = function (datetime) {
            var onUpdate = _this.props.onUpdate;
            _this.setState({
                isOpen: false,
                hasChanges: false,
            }, function () {
                _this.callCallback(onUpdate, datetime);
            });
        };
        _this.handleAbsoluteClick = function () {
            var _a = _this.props, relative = _a.relative, onChange = _a.onChange, defaultPeriod = _a.defaultPeriod;
            // Set default range to equivalent of last relative period,
            // or use default stats period
            var newDateTime = {
                relative: null,
                start: dates_1.getPeriodAgo('hours', dates_1.parsePeriodToHours(relative || defaultPeriod || constants_1.DEFAULT_STATS_PERIOD)).toDate(),
                end: new Date(),
            };
            if (utils_2.defined(_this.props.utc)) {
                newDateTime.utc = _this.state.utc;
            }
            _this.setState(tslib_1.__assign(tslib_1.__assign({ hasChanges: true }, newDateTime), { start: newDateTime.start, end: newDateTime.end }));
            _this.callCallback(onChange, newDateTime);
        };
        _this.handleSelectRelative = function (value) {
            var onChange = _this.props.onChange;
            var newDateTime = {
                relative: value,
                start: undefined,
                end: undefined,
            };
            _this.setState(newDateTime);
            _this.callCallback(onChange, newDateTime);
            _this.handleUpdate(newDateTime);
        };
        _this.handleClear = function () {
            var _a = _this.props, onChange = _a.onChange, defaultPeriod = _a.defaultPeriod;
            var newDateTime = {
                relative: defaultPeriod || constants_1.DEFAULT_STATS_PERIOD,
                start: undefined,
                end: undefined,
                utc: null,
            };
            _this.setState(newDateTime);
            _this.callCallback(onChange, newDateTime);
            _this.handleUpdate(newDateTime);
        };
        _this.handleSelectDateRange = function (_a) {
            var start = _a.start, end = _a.end, _b = _a.hasDateRangeErrors, hasDateRangeErrors = _b === void 0 ? false : _b;
            if (hasDateRangeErrors) {
                _this.setState({ hasDateRangeErrors: hasDateRangeErrors });
                return;
            }
            var onChange = _this.props.onChange;
            var newDateTime = {
                relative: null,
                start: start,
                end: end,
            };
            if (utils_2.defined(_this.props.utc)) {
                newDateTime.utc = _this.state.utc;
            }
            _this.setState(tslib_1.__assign({ hasChanges: true, hasDateRangeErrors: hasDateRangeErrors }, newDateTime));
            _this.callCallback(onChange, newDateTime);
        };
        _this.handleUseUtc = function () {
            var _a = _this.props, onChange = _a.onChange, router = _a.router;
            var _b = _this.props, start = _b.start, end = _b.end;
            _this.setState(function (state) {
                var utc = !state.utc;
                if (!start) {
                    start = getDateWithTimezoneInUtc(state.start, state.utc);
                }
                if (!end) {
                    end = getDateWithTimezoneInUtc(state.end, state.utc);
                }
                analytics_1.analytics('dateselector.utc_changed', {
                    utc: utc,
                    path: getRouteStringFromRoutes_1.default(router.routes),
                    org_id: parseInt(_this.props.organization.id, 10),
                });
                var newDateTime = {
                    relative: null,
                    start: utc ? dates_1.getLocalToSystem(start) : dates_1.getUtcToSystem(start),
                    end: utc ? dates_1.getLocalToSystem(end) : dates_1.getUtcToSystem(end),
                    utc: utc,
                };
                _this.callCallback(onChange, newDateTime);
                return tslib_1.__assign({ hasChanges: true }, newDateTime);
            });
        };
        _this.handleOpen = function () {
            _this.setState({ isOpen: true });
            // Start loading react-date-picker
            Promise.resolve().then(function () { return tslib_1.__importStar(require('../timeRangeSelector/dateRange/index')); });
        };
        var start = undefined;
        var end = undefined;
        if (props.start && props.end) {
            start = getInternalDate(props.start, props.utc);
            end = getInternalDate(props.end, props.utc);
        }
        _this.state = {
            // if utc is not null and not undefined, then use value of `props.utc` (it can be false)
            // otherwise if no value is supplied, the default should be the user's timezone preference
            utc: utils_2.defined(props.utc) ? props.utc : dates_1.getUserTimezone() === 'UTC',
            isOpen: false,
            hasChanges: false,
            hasDateRangeErrors: false,
            start: start,
            end: end,
            relative: props.relative,
        };
        return _this;
    }
    TimeRangeSelector.prototype.componentDidUpdate = function (_prevProps, prevState) {
        var onToggleSelector = this.props.onToggleSelector;
        var currState = this.state;
        if (onToggleSelector && prevState.isOpen !== currState.isOpen) {
            onToggleSelector(currState.isOpen);
        }
    };
    TimeRangeSelector.prototype.render = function () {
        var _this = this;
        var _a = this.props, defaultPeriod = _a.defaultPeriod, showAbsolute = _a.showAbsolute, showRelative = _a.showRelative, organization = _a.organization, hint = _a.hint, label = _a.label, relativeOptions = _a.relativeOptions;
        var _b = this.state, start = _b.start, end = _b.end, relative = _b.relative;
        var shouldShowAbsolute = showAbsolute;
        var shouldShowRelative = showRelative;
        var isAbsoluteSelected = !!start && !!end;
        var summary = isAbsoluteSelected && start && end ? (<dateSummary_1.default start={start} end={end}/>) : (utils_1.getRelativeSummary(relative || defaultPeriod || constants_1.DEFAULT_STATS_PERIOD, relativeOptions));
        var relativeSelected = isAbsoluteSelected
            ? ''
            : relative || defaultPeriod || constants_1.DEFAULT_STATS_PERIOD;
        return (<dropdownMenu_1.default isOpen={this.state.isOpen} onOpen={this.handleOpen} onClose={this.handleCloseMenu} keepMenuOpen>
        {function (_a) {
                var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
                return (<TimeRangeRoot {...getRootProps()}>
            <StyledHeaderItem data-test-id="global-header-timerange-selector" icon={label !== null && label !== void 0 ? label : <icons_1.IconCalendar />} isOpen={isOpen} hasSelected={(!!_this.props.relative && _this.props.relative !== defaultPeriod) ||
                        isAbsoluteSelected} hasChanges={_this.state.hasChanges} onClear={_this.handleClear} allowClear hint={hint} {...getActorProps()}>
              {getDynamicText_1.default({ value: summary, fixed: 'start to end' })}
            </StyledHeaderItem>
            {isOpen && (<Menu {...getMenuProps()} isAbsoluteSelected={isAbsoluteSelected}>
                <SelectorList isAbsoluteSelected={isAbsoluteSelected}>
                  <SelectorItemsHook handleSelectRelative={_this.handleSelectRelative} handleAbsoluteClick={_this.handleAbsoluteClick} isAbsoluteSelected={isAbsoluteSelected} relativeSelected={relativeSelected} relativePeriods={relativeOptions} shouldShowAbsolute={shouldShowAbsolute} shouldShowRelative={shouldShowRelative}/>
                </SelectorList>
                {isAbsoluteSelected && (<div>
                    <DateRangeHook start={start !== null && start !== void 0 ? start : null} end={end !== null && end !== void 0 ? end : null} organization={organization} showTimePicker utc={_this.state.utc} onChange={_this.handleSelectDateRange} onChangeUtc={_this.handleUseUtc}/>
                    <SubmitRow>
                      <multipleSelectorSubmitRow_1.default onSubmit={_this.handleCloseMenu} disabled={!_this.state.hasChanges || _this.state.hasDateRangeErrors}/>
                    </SubmitRow>
                  </div>)}
              </Menu>)}
          </TimeRangeRoot>);
            }}
      </dropdownMenu_1.default>);
    };
    TimeRangeSelector.defaultProps = defaultProps;
    return TimeRangeSelector;
}(React.PureComponent));
var TimeRangeRoot = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
exports.TimeRangeRoot = TimeRangeRoot;
var StyledHeaderItem = styled_1.default(headerItem_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: 100%;\n"], ["\n  height: 100%;\n"])));
var Menu = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", ";\n  ", ";\n\n  display: flex;\n  background: ", ";\n  border: 1px solid ", ";\n  position: absolute;\n  top: 100%;\n  min-width: 100%;\n  z-index: ", ";\n  box-shadow: ", ";\n  border-radius: ", ";\n  font-size: 0.8em;\n  overflow: hidden;\n"], ["\n  ", ";\n  ", ";\n\n  display: flex;\n  background: ", ";\n  border: 1px solid ", ";\n  position: absolute;\n  top: 100%;\n  min-width: 100%;\n  z-index: ", ";\n  box-shadow: ", ";\n  border-radius: ", ";\n  font-size: 0.8em;\n  overflow: hidden;\n"])), function (p) { return !p.isAbsoluteSelected && 'left: -1px'; }, function (p) { return p.isAbsoluteSelected && 'right: -1px'; }, function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.zIndex.dropdown; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.borderRadiusBottom; });
var SelectorList = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  flex-shrink: 0;\n  min-width: ", ";\n  min-height: 305px;\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  flex-shrink: 0;\n  min-width: ", ";\n  min-height: 305px;\n"])), function (p) { return (p.isAbsoluteSelected ? '160px' : '220px'); });
var SubmitRow = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  border-top: 1px solid ", ";\n  border-left: 1px solid ", ";\n"], ["\n  padding: ", " ", ";\n  border-top: 1px solid ", ";\n  border-left: 1px solid ", ";\n"])), space_1.default(0.5), space_1.default(1), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.border; });
exports.default = ReactRouter.withRouter(TimeRangeSelector);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map