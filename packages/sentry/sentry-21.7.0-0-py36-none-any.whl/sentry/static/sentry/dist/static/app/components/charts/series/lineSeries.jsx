Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("echarts/lib/chart/line");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
function LineSeries(props) {
    return tslib_1.__assign(tslib_1.__assign({ showSymbol: false, symbolSize: theme_1.default.charts.symbolSize }, props), { type: 'line' });
}
exports.default = LineSeries;
//# sourceMappingURL=lineSeries.jsx.map