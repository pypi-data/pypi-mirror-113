Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var lineSeries_1 = tslib_1.__importDefault(require("./series/lineSeries"));
var baseChart_1 = tslib_1.__importDefault(require("./baseChart"));
var LineChart = /** @class */ (function (_super) {
    tslib_1.__extends(LineChart, _super);
    function LineChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LineChart.prototype.render = function () {
        var _a = this.props, series = _a.series, seriesOptions = _a.seriesOptions, props = tslib_1.__rest(_a, ["series", "seriesOptions"]);
        return (<baseChart_1.default {...props} series={series.map(function (_a) {
                var seriesName = _a.seriesName, data = _a.data, dataArray = _a.dataArray, options = tslib_1.__rest(_a, ["seriesName", "data", "dataArray"]);
                return lineSeries_1.default(tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, seriesOptions), options), { name: seriesName, data: dataArray || data.map(function (_a) {
                        var value = _a.value, name = _a.name;
                        return [name, value];
                    }), animation: false, animationThreshold: 1, animationDuration: 0 }));
            })}/>);
    };
    return LineChart;
}(React.Component));
exports.default = LineChart;
//# sourceMappingURL=lineChart.jsx.map