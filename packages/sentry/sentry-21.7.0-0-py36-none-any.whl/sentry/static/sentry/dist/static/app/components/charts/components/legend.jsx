Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("echarts/lib/component/legend");
require("echarts/lib/component/legendScroll");
var merge_1 = tslib_1.__importDefault(require("lodash/merge"));
var utils_1 = require("../utils");
function Legend(props) {
    var _a = props !== null && props !== void 0 ? props : {}, truncate = _a.truncate, theme = _a.theme, rest = tslib_1.__rest(_a, ["truncate", "theme"]);
    var formatter = function (value) { return utils_1.truncationFormatter(value, truncate !== null && truncate !== void 0 ? truncate : 0); };
    return merge_1.default({
        show: true,
        type: 'scroll',
        padding: 0,
        formatter: formatter,
        icon: 'circle',
        itemHeight: 14,
        itemWidth: 8,
        itemGap: 12,
        align: 'left',
        textStyle: {
            color: theme.textColor,
            verticalAlign: 'top',
            fontSize: 11,
            fontFamily: theme.text.family,
            lineHeight: 14,
        },
        inactiveColor: theme.inactive,
    }, rest);
}
exports.default = Legend;
//# sourceMappingURL=legend.jsx.map