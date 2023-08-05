Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_lazyload_1 = tslib_1.__importDefault(require("react-lazyload"));
var miniBarChart_1 = tslib_1.__importDefault(require("app/components/charts/miniBarChart"));
var locale_1 = require("app/locale");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
function GroupChart(_a) {
    var data = _a.data, statsPeriod = _a.statsPeriod, _b = _a.showSecondaryPoints, showSecondaryPoints = _b === void 0 ? false : _b, _c = _a.height, height = _c === void 0 ? 24 : _c;
    var stats = statsPeriod
        ? data.filtered
            ? data.filtered.stats[statsPeriod]
            : data.stats[statsPeriod]
        : [];
    var secondaryStats = statsPeriod && data.filtered ? data.stats[statsPeriod] : null;
    if (!stats || !stats.length) {
        return null;
    }
    var colors = undefined;
    var emphasisColors = undefined;
    var series = [];
    if (showSecondaryPoints && secondaryStats && secondaryStats.length) {
        series.push({
            seriesName: locale_1.t('Total Events'),
            data: secondaryStats.map(function (point) { return ({ name: point[0] * 1000, value: point[1] }); }),
        });
        series.push({
            seriesName: locale_1.t('Matching Events'),
            data: stats.map(function (point) { return ({ name: point[0] * 1000, value: point[1] }); }),
        });
    }
    else {
        // Colors are custom to preserve historical appearance where the single series is
        // considerably darker than the two series results.
        colors = [theme_1.default.gray300];
        emphasisColors = [theme_1.default.purple300];
        series.push({
            seriesName: locale_1.t('Events'),
            data: stats.map(function (point) { return ({ name: point[0] * 1000, value: point[1] }); }),
        });
    }
    return (<react_lazyload_1.default debounce={50} height={height}>
      <miniBarChart_1.default height={height} isGroupedByDate showTimeInTooltip series={series} colors={colors} emphasisColors={emphasisColors} hideDelay={50}/>
    </react_lazyload_1.default>);
}
exports.default = GroupChart;
//# sourceMappingURL=groupChart.jsx.map