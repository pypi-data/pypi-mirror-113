Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var barSeries_1 = tslib_1.__importDefault(require("./series/barSeries"));
var baseChart_1 = tslib_1.__importDefault(require("./baseChart"));
var BarChart = /** @class */ (function (_super) {
    tslib_1.__extends(BarChart, _super);
    function BarChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    BarChart.prototype.render = function () {
        var _a = this.props, series = _a.series, stacked = _a.stacked, xAxis = _a.xAxis, props = tslib_1.__rest(_a, ["series", "stacked", "xAxis"]);
        return (<baseChart_1.default {...props} xAxis={xAxis !== null ? tslib_1.__assign(tslib_1.__assign({}, (xAxis || {})), { boundaryGap: true }) : null} series={series.map(function (_a) {
                var seriesName = _a.seriesName, data = _a.data, options = tslib_1.__rest(_a, ["seriesName", "data"]);
                return barSeries_1.default(tslib_1.__assign({ name: seriesName, stack: stacked ? 'stack1' : undefined, data: data.map(function (_a) {
                        var value = _a.value, name = _a.name, itemStyle = _a.itemStyle;
                        if (itemStyle === undefined) {
                            return [name, value];
                        }
                        return { value: [name, value], itemStyle: itemStyle };
                    }) }, options));
            })}/>);
    };
    return BarChart;
}(React.Component));
exports.default = BarChart;
//# sourceMappingURL=barChart.jsx.map