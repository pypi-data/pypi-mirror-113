Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var merge_1 = tslib_1.__importDefault(require("lodash/merge"));
function YAxis(_a) {
    var theme = _a.theme, props = tslib_1.__rest(_a, ["theme"]);
    return merge_1.default({
        axisLine: {
            show: false,
        },
        axisTick: {
            show: false,
        },
        axisLabel: {
            color: theme.chartLabel,
            fontFamily: theme.text.family,
        },
        splitLine: {
            lineStyle: {
                color: theme.chartLineColor,
                opacity: 0.3,
            },
        },
    }, props);
}
exports.default = YAxis;
//# sourceMappingURL=yAxis.jsx.map