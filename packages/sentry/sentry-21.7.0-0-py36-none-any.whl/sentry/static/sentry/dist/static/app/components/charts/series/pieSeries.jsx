Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("echarts/lib/chart/pie");
function PieSeries(props) {
    if (props === void 0) { props = {}; }
    var data = props.data, rest = tslib_1.__rest(props, ["data"]);
    return tslib_1.__assign(tslib_1.__assign({ radius: ['50%', '70%'], data: data }, rest), { type: 'pie' });
}
exports.default = PieSeries;
//# sourceMappingURL=pieSeries.jsx.map