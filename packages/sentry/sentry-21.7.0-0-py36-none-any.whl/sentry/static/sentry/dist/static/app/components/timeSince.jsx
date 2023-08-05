Object.defineProperty(exports, "__esModule", { value: true });
exports.getRelativeDate = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var isNumber_1 = tslib_1.__importDefault(require("lodash/isNumber"));
var isString_1 = tslib_1.__importDefault(require("lodash/isString"));
var moment_timezone_1 = tslib_1.__importDefault(require("moment-timezone"));
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var formatters_1 = require("app/utils/formatters");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var tooltip_1 = tslib_1.__importDefault(require("./tooltip"));
var ONE_MINUTE_IN_MS = 60000;
var TimeSince = /** @class */ (function (_super) {
    tslib_1.__extends(TimeSince, _super);
    function TimeSince() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            relative: '',
        };
        _this.ticker = null;
        _this.setRelativeDateTicker = function () {
            _this.ticker = window.setTimeout(function () {
                _this.setState({
                    relative: getRelativeDate(_this.props.date, _this.props.suffix, _this.props.shorten, _this.props.extraShort),
                });
                _this.setRelativeDateTicker();
            }, ONE_MINUTE_IN_MS);
        };
        return _this;
    }
    // TODO(ts) TODO(emotion): defining the props type breaks emotion's typings
    // See: https://github.com/emotion-js/emotion/pull/1514
    TimeSince.getDerivedStateFromProps = function (props) {
        return {
            relative: getRelativeDate(props.date, props.suffix, props.shorten, props.extraShort),
        };
    };
    TimeSince.prototype.componentDidMount = function () {
        this.setRelativeDateTicker();
    };
    TimeSince.prototype.componentWillUnmount = function () {
        if (this.ticker) {
            window.clearTimeout(this.ticker);
            this.ticker = null;
        }
    };
    TimeSince.prototype.render = function () {
        var _a;
        var _b = this.props, date = _b.date, _suffix = _b.suffix, disabledAbsoluteTooltip = _b.disabledAbsoluteTooltip, className = _b.className, tooltipTitle = _b.tooltipTitle, _shorten = _b.shorten, _extraShort = _b.extraShort, props = tslib_1.__rest(_b, ["date", "suffix", "disabledAbsoluteTooltip", "className", "tooltipTitle", "shorten", "extraShort"]);
        var dateObj = getDateObj(date);
        var user = configStore_1.default.get('user');
        var options = user ? user.options : null;
        var format = (options === null || options === void 0 ? void 0 : options.clock24Hours) ? 'MMMM D, YYYY HH:mm z' : 'LLL z';
        var tooltip = getDynamicText_1.default({
            fixed: (options === null || options === void 0 ? void 0 : options.clock24Hours)
                ? 'November 3, 2020 08:57 UTC'
                : 'November 3, 2020 8:58 AM UTC',
            value: moment_timezone_1.default.tz(dateObj, (_a = options === null || options === void 0 ? void 0 : options.timezone) !== null && _a !== void 0 ? _a : '').format(format),
        });
        return (<tooltip_1.default disabled={disabledAbsoluteTooltip} title={<div>
            <div>{tooltipTitle}</div>
            {tooltip}
          </div>}>
        <time dateTime={dateObj.toISOString()} className={className} {...props}>
          {this.state.relative}
        </time>
      </tooltip_1.default>);
    };
    TimeSince.defaultProps = {
        suffix: 'ago',
    };
    return TimeSince;
}(React.PureComponent));
exports.default = TimeSince;
function getDateObj(date) {
    if (isString_1.default(date) || isNumber_1.default(date)) {
        date = new Date(date);
    }
    return date;
}
function getRelativeDate(currentDateTime, suffix, shorten, extraShort) {
    var date = getDateObj(currentDateTime);
    if ((shorten || extraShort) && suffix) {
        return locale_1.t('%(time)s %(suffix)s', {
            time: formatters_1.getDuration(moment_timezone_1.default().diff(moment_timezone_1.default(date), 'seconds'), 0, shorten, extraShort),
            suffix: suffix,
        });
    }
    else if ((shorten || extraShort) && !suffix) {
        return formatters_1.getDuration(moment_timezone_1.default().diff(moment_timezone_1.default(date), 'seconds'), 0, shorten, extraShort);
    }
    else if (!suffix) {
        return moment_timezone_1.default(date).fromNow(true);
    }
    else if (suffix === 'ago') {
        return moment_timezone_1.default(date).fromNow();
    }
    else if (suffix === 'old') {
        return locale_1.t('%(time)s old', { time: moment_timezone_1.default(date).fromNow(true) });
    }
    else {
        throw new Error('Unsupported time format suffix');
    }
}
exports.getRelativeDate = getRelativeDate;
//# sourceMappingURL=timeSince.jsx.map