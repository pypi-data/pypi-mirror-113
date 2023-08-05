Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("echarts/lib/component/markLine");
/**
 * eCharts markLine
 *
 * See https://echarts.apache.org/en/option.html#series-line.markLine
 */
function MarkLine(props) {
    return tslib_1.__assign({ 
        // The second symbol is a very ugly arrow, we don't want it
        symbol: ['none', 'none'] }, props);
}
exports.default = MarkLine;
//# sourceMappingURL=markLine.jsx.map