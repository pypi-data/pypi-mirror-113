Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("echarts/lib/chart/heatmap");
require("echarts/lib/component/visualMap");
function HeatMapSeries(props) {
    if (props === void 0) { props = {}; }
    var data = props.data, rest = tslib_1.__rest(props, ["data"]);
    return tslib_1.__assign(tslib_1.__assign({ data: data }, rest), { type: 'heatmap' });
}
exports.default = HeatMapSeries;
//# sourceMappingURL=heatMapSeries.jsx.map