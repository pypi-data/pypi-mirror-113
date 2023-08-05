Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("echarts/lib/chart/bar");
function barSeries(props) {
    if (props === void 0) { props = {}; }
    var data = props.data, rest = tslib_1.__rest(props, ["data"]);
    return tslib_1.__assign(tslib_1.__assign({}, rest), { data: data, type: 'bar' });
}
exports.default = barSeries;
//# sourceMappingURL=barSeries.jsx.map