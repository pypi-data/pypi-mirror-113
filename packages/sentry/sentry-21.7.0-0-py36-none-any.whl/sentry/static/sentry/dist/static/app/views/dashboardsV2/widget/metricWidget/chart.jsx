Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var areaChart_1 = tslib_1.__importDefault(require("app/components/charts/areaChart"));
var barChart_1 = tslib_1.__importDefault(require("app/components/charts/barChart"));
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var utils_1 = require("app/components/charts/utils");
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var icons_1 = require("app/icons");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
var utils_2 = require("../utils");
function Chart(_a) {
    var timeseriesResults = _a.series, displayType = _a.displayType, location = _a.location, errored = _a.errored, isLoading = _a.isLoading, selection = _a.selection, router = _a.router, theme = _a.theme, platform = _a.platform;
    var datetime = selection.datetime;
    var utc = datetime.utc, period = datetime.period, start = datetime.start, end = datetime.end;
    var filteredTimeseriesResults = timeseriesResults.filter(function (_a) {
        var seriesName = _a.seriesName;
        // There is no concept of Abnormal sessions in javascript
        if ((seriesName === sessionTerm_1.sessionTerm.abnormal || seriesName === sessionTerm_1.sessionTerm.otherAbnormal) &&
            platform &&
            ['javascript', 'node'].includes(platform)) {
            return false;
        }
        return true;
    });
    var colors = timeseriesResults
        ? theme.charts.getColorPalette(timeseriesResults.length - 2)
        : [];
    // Create a list of series based on the order of the fields,
    var series = filteredTimeseriesResults
        ? filteredTimeseriesResults.map(function (values, index) { return (tslib_1.__assign(tslib_1.__assign({}, values), { color: colors[index] })); })
        : [];
    var chartProps = {
        series: series,
        legend: {
            right: 10,
            top: 0,
            selected: utils_1.getSeriesSelection(location),
        },
        grid: {
            left: '0px',
            right: '10px',
            top: '30px',
            bottom: '0px',
        },
    };
    function renderChart(zoomRenderProps) {
        switch (displayType) {
            case utils_2.DisplayType.BAR:
                return <barChart_1.default {...zoomRenderProps} {...chartProps}/>;
            case utils_2.DisplayType.AREA:
                return <areaChart_1.default {...zoomRenderProps} stacked {...chartProps}/>;
            case utils_2.DisplayType.LINE:
            default:
                return <lineChart_1.default {...zoomRenderProps} {...chartProps}/>;
        }
    }
    return (<chartZoom_1.default router={router} period={period} utc={utc} start={start} end={end}>
      {function (zoomRenderProps) {
            if (errored) {
                return (<errorPanel_1.default>
              <icons_1.IconWarning color="gray300" size="lg"/>
            </errorPanel_1.default>);
            }
            return (<transitionChart_1.default loading={isLoading} reloading={isLoading}>
            <LoadingScreen loading={isLoading}/>
            {getDynamicText_1.default({
                    value: renderChart(zoomRenderProps),
                    fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
                })}
          </transitionChart_1.default>);
        }}
    </chartZoom_1.default>);
}
exports.default = react_1.withTheme(Chart);
var LoadingScreen = function (_a) {
    var loading = _a.loading;
    if (!loading) {
        return null;
    }
    return (<StyledTransparentLoadingMask visible={loading}>
      <loadingIndicator_1.default mini/>
    </StyledTransparentLoadingMask>);
};
var StyledTransparentLoadingMask = styled_1.default(function (props) { return (<transparentLoadingMask_1.default {...props} maskBackgroundColor="transparent"/>); })(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"])));
var templateObject_1;
//# sourceMappingURL=chart.jsx.map