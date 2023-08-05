Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("./components/visualMap");
var React = tslib_1.__importStar(require("react"));
var heatMapSeries_1 = tslib_1.__importDefault(require("./series/heatMapSeries"));
var baseChart_1 = tslib_1.__importDefault(require("./baseChart"));
exports.default = React.forwardRef(function (props, ref) {
    var series = props.series, seriesOptions = props.seriesOptions, visualMaps = props.visualMaps, otherProps = tslib_1.__rest(props, ["series", "seriesOptions", "visualMaps"]);
    return (<baseChart_1.default ref={ref} options={{
            visualMap: visualMaps,
        }} {...otherProps} series={series.map(function (_a) {
            var seriesName = _a.seriesName, data = _a.data, dataArray = _a.dataArray, options = tslib_1.__rest(_a, ["seriesName", "data", "dataArray"]);
            return heatMapSeries_1.default(tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, seriesOptions), options), { name: seriesName, data: dataArray || data.map(function (_a) {
                    var value = _a.value, name = _a.name;
                    return [name, value];
                }) }));
        })}/>);
});
//# sourceMappingURL=heatMapChart.jsx.map