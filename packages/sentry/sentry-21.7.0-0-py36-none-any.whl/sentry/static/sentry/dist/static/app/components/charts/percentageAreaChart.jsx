Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var areaSeries_1 = tslib_1.__importDefault(require("./series/areaSeries"));
var baseChart_1 = tslib_1.__importDefault(require("./baseChart"));
var FILLER_NAME = '__filler';
/**
 * A stacked 100% column chart over time
 *
 * See https://exceljet.net/chart-type/100-stacked-bar-chart
 */
var PercentageAreaChart = /** @class */ (function (_super) {
    tslib_1.__extends(PercentageAreaChart, _super);
    function PercentageAreaChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PercentageAreaChart.prototype.getSeries = function () {
        var _a = this.props, series = _a.series, getDataItemName = _a.getDataItemName, getValue = _a.getValue;
        var totalsArray = series.length
            ? series[0].data.map(function (_a, i) {
                var name = _a.name;
                return [
                    name,
                    series.reduce(function (sum, _a) {
                        var data = _a.data;
                        return sum + data[i].value;
                    }, 0),
                ];
            })
            : [];
        var totals = new Map(totalsArray);
        return tslib_1.__spreadArray([], tslib_1.__read(series.map(function (_a) {
            var seriesName = _a.seriesName, data = _a.data;
            return areaSeries_1.default({
                name: seriesName,
                lineStyle: { width: 1 },
                areaStyle: { opacity: 1 },
                smooth: true,
                stack: 'percentageAreaChartStack',
                data: data.map(function (dataObj) { return [
                    getDataItemName(dataObj),
                    getValue(dataObj, totals.get(dataObj.name)),
                ]; }),
            });
        })));
    };
    PercentageAreaChart.prototype.render = function () {
        return (<baseChart_1.default {...this.props} tooltip={{
                formatter: function (seriesParams) {
                    // `seriesParams` can be an array or an object :/
                    var series = Array.isArray(seriesParams) ? seriesParams : [seriesParams];
                    // Filter series that have 0 counts
                    var date = (series.length && moment_1.default(series[0].axisValue).format('MMM D, YYYY')) + "<br />" || '';
                    return [
                        '<div class="tooltip-series">',
                        series
                            .filter(function (_a) {
                            var seriesName = _a.seriesName, data = _a.data;
                            return data[1] > 0.001 && seriesName !== FILLER_NAME;
                        })
                            .map(function (_a) {
                            var marker = _a.marker, seriesName = _a.seriesName, data = _a.data;
                            return "<div><span class=\"tooltip-label\">" + marker + " <strong>" + seriesName + "</strong></span> " + data[1] + "%</div>";
                        })
                            .join(''),
                        '</div>',
                        "<div class=\"tooltip-date\">" + date + "</div>",
                        '<div class="tooltip-arrow"></div>',
                    ].join('');
                },
            }} xAxis={{ boundaryGap: true }} yAxis={{
                min: 0,
                max: 100,
                type: 'value',
                interval: 25,
                splitNumber: 4,
                data: [0, 25, 50, 100],
                axisLabel: {
                    formatter: '{value}%',
                },
            }} series={this.getSeries()}/>);
    };
    PercentageAreaChart.defaultProps = {
        // TODO(billyvg): Move these into BaseChart? or get rid completely
        getDataItemName: function (_a) {
            var name = _a.name;
            return name;
        },
        getValue: function (_a, total) {
            var value = _a.value;
            return (!total ? 0 : Math.round((value / total) * 1000) / 10);
        },
    };
    return PercentageAreaChart;
}(React.Component));
exports.default = PercentageAreaChart;
//# sourceMappingURL=percentageAreaChart.jsx.map