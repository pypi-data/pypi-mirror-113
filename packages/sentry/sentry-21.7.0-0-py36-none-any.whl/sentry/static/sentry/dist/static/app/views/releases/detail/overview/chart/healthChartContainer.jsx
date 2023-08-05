Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var icons_1 = require("app/icons");
var sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
var healthChart_1 = tslib_1.__importDefault(require("./healthChart"));
var utils_1 = require("./utils");
var ReleaseChartContainer = /** @class */ (function (_super) {
    tslib_1.__extends(ReleaseChartContainer, _super);
    function ReleaseChartContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            shouldRecalculateVisibleSeries: true,
        };
        _this.handleVisibleSeriesRecalculated = function () {
            _this.setState({ shouldRecalculateVisibleSeries: false });
        };
        return _this;
    }
    ReleaseChartContainer.prototype.render = function () {
        var _this = this;
        var _a = this.props, loading = _a.loading, errored = _a.errored, reloading = _a.reloading, chartData = _a.chartData, selection = _a.selection, yAxis = _a.yAxis, router = _a.router, platform = _a.platform, title = _a.title, help = _a.help;
        var shouldRecalculateVisibleSeries = this.state.shouldRecalculateVisibleSeries;
        var datetime = selection.datetime;
        var utc = datetime.utc, period = datetime.period, start = datetime.start, end = datetime.end;
        var timeseriesData = chartData.filter(function (_a) {
            var seriesName = _a.seriesName;
            // There is no concept of Abnormal sessions in javascript
            if ((seriesName === sessionTerm_1.sessionTerm.abnormal ||
                seriesName === sessionTerm_1.sessionTerm.otherAbnormal) &&
                ['javascript', 'node'].includes(platform)) {
                return false;
            }
            return true;
        });
        return (<chartZoom_1.default router={router} period={period} utc={utc} start={start} end={end}>
        {function (zoomRenderProps) {
                if (errored) {
                    return (<errorPanel_1.default>
                <icons_1.IconWarning color="gray300" size="lg"/>
              </errorPanel_1.default>);
                }
                return (<transitionChart_1.default loading={loading} reloading={reloading}>
              <transparentLoadingMask_1.default visible={reloading}/>
              <healthChart_1.default timeseriesData={timeseriesData.sort(utils_1.sortSessionSeries)} zoomRenderProps={zoomRenderProps} reloading={reloading} yAxis={yAxis} location={router.location} shouldRecalculateVisibleSeries={shouldRecalculateVisibleSeries} onVisibleSeriesRecalculated={_this.handleVisibleSeriesRecalculated} platform={platform} title={title} help={help}/>
            </transitionChart_1.default>);
            }}
      </chartZoom_1.default>);
    };
    return ReleaseChartContainer;
}(react_1.Component));
exports.default = ReleaseChartContainer;
//# sourceMappingURL=healthChartContainer.jsx.map