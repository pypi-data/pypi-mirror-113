Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var areaChart_1 = tslib_1.__importDefault(require("app/components/charts/areaChart"));
var StackedAreaChart = /** @class */ (function (_super) {
    tslib_1.__extends(StackedAreaChart, _super);
    function StackedAreaChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    StackedAreaChart.prototype.render = function () {
        return <areaChart_1.default tooltip={{ filter: function (val) { return val > 0; } }} {...this.props} stacked/>;
    };
    return StackedAreaChart;
}(React.Component));
exports.default = StackedAreaChart;
//# sourceMappingURL=stackedAreaChart.jsx.map