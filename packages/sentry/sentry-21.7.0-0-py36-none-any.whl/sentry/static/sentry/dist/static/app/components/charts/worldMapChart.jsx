Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var echarts_1 = tslib_1.__importDefault(require("echarts"));
var max_1 = tslib_1.__importDefault(require("lodash/max"));
var visualMap_1 = tslib_1.__importDefault(require("./components/visualMap"));
var mapSeries_1 = tslib_1.__importDefault(require("./series/mapSeries"));
var baseChart_1 = tslib_1.__importDefault(require("./baseChart"));
var WorldMapChart = /** @class */ (function (_super) {
    tslib_1.__extends(WorldMapChart, _super);
    function WorldMapChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            countryToCodeMap: null,
            map: null,
            codeToCountryMap: null,
        };
        return _this;
    }
    WorldMapChart.prototype.componentDidMount = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, countryToCodeMap, worldMap;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0: return [4 /*yield*/, Promise.all([
                            Promise.resolve().then(function () { return tslib_1.__importStar(require('app/data/countryCodesMap')); }),
                            Promise.resolve().then(function () { return tslib_1.__importStar(require('app/data/world.json')); }),
                        ])];
                    case 1:
                        _a = tslib_1.__read.apply(void 0, [_b.sent(), 2]), countryToCodeMap = _a[0], worldMap = _a[1];
                        echarts_1.default.registerMap('sentryWorld', worldMap.default);
                        // eslint-disable-next-line
                        this.setState({
                            countryToCodeMap: countryToCodeMap.default,
                            map: worldMap.default,
                            codeToCountryMap: Object.fromEntries(Object.entries(countryToCodeMap.default).map(function (_a) {
                                var _b = tslib_1.__read(_a, 2), country = _b[0], code = _b[1];
                                return [code, country];
                            })),
                        });
                        return [2 /*return*/];
                }
            });
        });
    };
    WorldMapChart.prototype.render = function () {
        var _this = this;
        var _a = this.state, countryToCodeMap = _a.countryToCodeMap, map = _a.map;
        if (countryToCodeMap === null || map === null) {
            return null;
        }
        var _b = this.props, series = _b.series, seriesOptions = _b.seriesOptions, theme = _b.theme, props = tslib_1.__rest(_b, ["series", "seriesOptions", "theme"]);
        var processedSeries = series.map(function (_a) {
            var _b;
            var seriesName = _a.seriesName, data = _a.data, options = tslib_1.__rest(_a, ["seriesName", "data"]);
            return mapSeries_1.default(tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, seriesOptions), options), { map: 'sentryWorld', name: seriesName, nameMap: (_b = _this.state.countryToCodeMap) !== null && _b !== void 0 ? _b : undefined, aspectScale: 0.85, zoom: 1.3, center: [10.97, 9.71], itemStyle: {
                    areaColor: theme.gray200,
                    borderColor: theme.backgroundSecondary,
                    emphasis: {
                        areaColor: theme.orange300,
                    },
                }, label: {
                    emphasis: {
                        show: false,
                    },
                }, data: data }));
        });
        // TODO(billy):
        // For absolute values, we want min/max to based on min/max of series
        // Otherwise it should be 0-100
        var maxValue = max_1.default(series.map(function (_a) {
            var data = _a.data;
            return max_1.default(data.map(function (_a) {
                var value = _a.value;
                return value;
            }));
        })) || 1;
        var tooltipFormatter = function (format) {
            var _a;
            var _b = Array.isArray(format) ? format[0] : format, marker = _b.marker, name = _b.name, value = _b.value;
            // If value is NaN, don't show anything because we won't have a country code either
            if (isNaN(value)) {
                return '';
            }
            // `value` should be a number
            var formattedValue = typeof value === 'number' ? value.toLocaleString() : '';
            var countryOrCode = ((_a = _this.state.codeToCountryMap) === null || _a === void 0 ? void 0 : _a[name]) || name;
            return [
                "<div class=\"tooltip-series tooltip-series-solo\">\n                 <div><span class=\"tooltip-label\">" + marker + " <strong>" + countryOrCode + "</strong></span> " + formattedValue + "</div>\n              </div>",
                '<div class="tooltip-arrow"></div>',
            ].join('');
        };
        return (<baseChart_1.default options={{
                backgroundColor: theme.background,
                visualMap: [
                    visualMap_1.default({
                        left: 'right',
                        min: 0,
                        max: maxValue,
                        inRange: {
                            color: [theme.purple200, theme.purple300],
                        },
                        text: ['High', 'Low'],
                        textStyle: {
                            color: theme.textColor,
                        },
                        // Whether show handles, which can be dragged to adjust "selected range".
                        // False because the handles are pretty ugly
                        calculable: false,
                    }),
                ],
            }} {...props} yAxis={null} xAxis={null} series={processedSeries} tooltip={{
                formatter: tooltipFormatter,
            }}/>);
    };
    return WorldMapChart;
}(React.Component));
exports.default = react_1.withTheme(WorldMapChart);
//# sourceMappingURL=worldMapChart.jsx.map