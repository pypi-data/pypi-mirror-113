Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var areaSeries_1 = tslib_1.__importDefault(require("./series/areaSeries"));
var baseChart_1 = tslib_1.__importDefault(require("./baseChart"));
var AreaChart = /** @class */ (function (_super) {
    tslib_1.__extends(AreaChart, _super);
    function AreaChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AreaChart.prototype.render = function () {
        var _a = this.props, series = _a.series, stacked = _a.stacked, colors = _a.colors, props = tslib_1.__rest(_a, ["series", "stacked", "colors"]);
        return (<baseChart_1.default {...props} colors={colors} series={series.map(function (_a, i) {
                var seriesName = _a.seriesName, data = _a.data, otherSeriesProps = tslib_1.__rest(_a, ["seriesName", "data"]);
                return areaSeries_1.default(tslib_1.__assign({ stack: stacked ? 'area' : undefined, name: seriesName, data: data.map(function (_a) {
                        var name = _a.name, value = _a.value;
                        return [name, value];
                    }), lineStyle: {
                        color: colors === null || colors === void 0 ? void 0 : colors[i],
                        opacity: 1,
                        width: 0.4,
                    }, areaStyle: {
                        color: colors === null || colors === void 0 ? void 0 : colors[i],
                        opacity: 1.0,
                    }, animation: false, animationThreshold: 1, animationDuration: 0 }, otherSeriesProps));
            })}/>);
    };
    return AreaChart;
}(React.Component));
exports.default = AreaChart;
//# sourceMappingURL=areaChart.jsx.map