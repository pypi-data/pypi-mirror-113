Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_lazyload_1 = tslib_1.__importDefault(require("react-lazyload"));
var react_2 = require("@emotion/react");
var miniBarChart_1 = tslib_1.__importDefault(require("app/components/charts/miniBarChart"));
var locale_1 = require("app/locale");
var utils_1 = require("./utils");
var HealthStatsChart = /** @class */ (function (_super) {
    tslib_1.__extends(HealthStatsChart, _super);
    function HealthStatsChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.formatTooltip = function (value) {
            var activeDisplay = _this.props.activeDisplay;
            var suffix = activeDisplay === utils_1.DisplayOption.USERS
                ? locale_1.tn('user', 'users', value)
                : locale_1.tn('session', 'sessions', value);
            return value.toLocaleString() + " " + suffix;
        };
        return _this;
    }
    HealthStatsChart.prototype.render = function () {
        var _a = this.props, height = _a.height, data = _a.data, theme = _a.theme;
        return (<react_lazyload_1.default debounce={50} height={height}>
        <miniBarChart_1.default series={data} height={height} isGroupedByDate showTimeInTooltip hideDelay={50} tooltipFormatter={this.formatTooltip} colors={[theme.purple300, theme.gray200]}/>
      </react_lazyload_1.default>);
    };
    HealthStatsChart.defaultProps = {
        height: 24,
    };
    return HealthStatsChart;
}(react_1.Component));
exports.default = react_2.withTheme(HealthStatsChart);
//# sourceMappingURL=healthStatsChart.jsx.map