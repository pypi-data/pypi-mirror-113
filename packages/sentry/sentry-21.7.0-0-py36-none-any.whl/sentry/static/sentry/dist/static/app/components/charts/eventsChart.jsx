Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var areaChart_1 = tslib_1.__importDefault(require("app/components/charts/areaChart"));
var barChart_1 = tslib_1.__importDefault(require("app/components/charts/barChart"));
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var releaseSeries_1 = tslib_1.__importDefault(require("app/components/charts/releaseSeries"));
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var utils_1 = require("app/components/charts/utils");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var utils_2 = require("app/utils");
var charts_1 = require("app/utils/discover/charts");
var fields_1 = require("app/utils/discover/fields");
var eventsRequest_1 = tslib_1.__importDefault(require("./eventsRequest"));
var Chart = /** @class */ (function (_super) {
    tslib_1.__extends(Chart, _super);
    function Chart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            seriesSelection: {},
            forceUpdate: false,
        };
        _this.handleLegendSelectChanged = function (legendChange) {
            var _a = _this.props.disableableSeries, disableableSeries = _a === void 0 ? [] : _a;
            var selected = legendChange.selected;
            var seriesSelection = Object.keys(selected).reduce(function (state, key) {
                // we only want them to be able to disable the Releases series,
                // and not any of the other possible series here
                var disableable = key === 'Releases' || disableableSeries.includes(key);
                state[key] = disableable ? selected[key] : true;
                return state;
            }, {});
            // we have to force an update here otherwise ECharts will
            // update its internal state and disable the series
            _this.setState({ seriesSelection: seriesSelection, forceUpdate: true }, function () {
                return _this.setState({ forceUpdate: false });
            });
        };
        return _this;
    }
    Chart.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (nextState.forceUpdate) {
            return true;
        }
        if (!isEqual_1.default(this.state.seriesSelection, nextState.seriesSelection)) {
            return true;
        }
        if (nextProps.reloading || !nextProps.timeseriesData) {
            return false;
        }
        if (isEqual_1.default(this.props.timeseriesData, nextProps.timeseriesData) &&
            isEqual_1.default(this.props.releaseSeries, nextProps.releaseSeries) &&
            isEqual_1.default(this.props.previousTimeseriesData, nextProps.previousTimeseriesData)) {
            return false;
        }
        return true;
    };
    Chart.prototype.getChartComponent = function () {
        var _a = this.props, showDaily = _a.showDaily, timeseriesData = _a.timeseriesData, yAxis = _a.yAxis, chartComponent = _a.chartComponent;
        if (utils_2.defined(chartComponent)) {
            return chartComponent;
        }
        if (showDaily) {
            return barChart_1.default;
        }
        if (timeseriesData.length > 1) {
            switch (fields_1.aggregateMultiPlotType(yAxis)) {
                case 'line':
                    return lineChart_1.default;
                case 'area':
                    return areaChart_1.default;
                default:
                    throw new Error("Unknown multi plot type for " + yAxis);
            }
        }
        return areaChart_1.default;
    };
    Chart.prototype.render = function () {
        var _a;
        var _b, _c, _d;
        var _e = this.props, theme = _e.theme, _loading = _e.loading, _reloading = _e.reloading, yAxis = _e.yAxis, releaseSeries = _e.releaseSeries, zoomRenderProps = _e.zoomRenderProps, timeseriesData = _e.timeseriesData, previousTimeseriesData = _e.previousTimeseriesData, showLegend = _e.showLegend, legendOptions = _e.legendOptions, chartOptionsProp = _e.chartOptions, currentSeriesName = _e.currentSeriesName, previousSeriesName = _e.previousSeriesName, seriesTransformer = _e.seriesTransformer, colors = _e.colors, height = _e.height, props = tslib_1.__rest(_e, ["theme", "loading", "reloading", "yAxis", "releaseSeries", "zoomRenderProps", "timeseriesData", "previousTimeseriesData", "showLegend", "legendOptions", "chartOptions", "currentSeriesName", "previousSeriesName", "seriesTransformer", "colors", "height"]);
        var seriesSelection = this.state.seriesSelection;
        var data = [currentSeriesName !== null && currentSeriesName !== void 0 ? currentSeriesName : locale_1.t('Current'), previousSeriesName !== null && previousSeriesName !== void 0 ? previousSeriesName : locale_1.t('Previous')];
        var releasesLegend = locale_1.t('Releases');
        if (Array.isArray(releaseSeries)) {
            data.push(releasesLegend);
        }
        // Temporary fix to improve performance on pages with a high number of releases.
        var releases = releaseSeries && releaseSeries[0];
        var hideReleasesByDefault = Array.isArray(releaseSeries) &&
            ((_c = (_b = releases) === null || _b === void 0 ? void 0 : _b.markLine) === null || _c === void 0 ? void 0 : _c.data) &&
            releases.markLine.data.length >= utils_1.RELEASE_LINES_THRESHOLD;
        var selected = !Array.isArray(releaseSeries)
            ? seriesSelection
            : Object.keys(seriesSelection).length === 0 && hideReleasesByDefault
                ? (_a = {}, _a[releasesLegend] = false, _a) : seriesSelection;
        var legend = showLegend
            ? tslib_1.__assign({ right: 16, top: 12, data: data, selected: selected }, (legendOptions !== null && legendOptions !== void 0 ? legendOptions : {})) : undefined;
        var series = Array.isArray(releaseSeries)
            ? tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(timeseriesData)), tslib_1.__read(releaseSeries)) : timeseriesData;
        if (seriesTransformer) {
            series = seriesTransformer(series);
        }
        var chartOptions = tslib_1.__assign({ colors: timeseriesData.length
                ? (_d = colors === null || colors === void 0 ? void 0 : colors.slice(0, series.length)) !== null && _d !== void 0 ? _d : tslib_1.__spreadArray([], tslib_1.__read(theme.charts.getColorPalette(timeseriesData.length - 2)))
                : undefined, grid: {
                left: '24px',
                right: '24px',
                top: '32px',
                bottom: '12px',
            }, seriesOptions: {
                showSymbol: false,
            }, tooltip: {
                trigger: 'axis',
                truncate: 80,
                valueFormatter: function (value) { return charts_1.tooltipFormatter(value, yAxis); },
            }, yAxis: {
                axisLabel: {
                    color: theme.chartLabel,
                    formatter: function (value) { return charts_1.axisLabelFormatter(value, yAxis); },
                },
            } }, (chartOptionsProp !== null && chartOptionsProp !== void 0 ? chartOptionsProp : {}));
        var Component = this.getChartComponent();
        return (<Component {...props} {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={this.handleLegendSelectChanged} series={series} previousPeriod={previousTimeseriesData ? [previousTimeseriesData] : undefined} height={height}/>);
    };
    return Chart;
}(React.Component));
var ThemedChart = react_1.withTheme(Chart);
var EventsChart = /** @class */ (function (_super) {
    tslib_1.__extends(EventsChart, _super);
    function EventsChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventsChart.prototype.render = function () {
        var _a = this.props, api = _a.api, period = _a.period, utc = _a.utc, query = _a.query, router = _a.router, start = _a.start, end = _a.end, projects = _a.projects, environments = _a.environments, showLegend = _a.showLegend, yAxis = _a.yAxis, disablePrevious = _a.disablePrevious, disableReleases = _a.disableReleases, emphasizeReleases = _a.emphasizeReleases, currentName = _a.currentSeriesName, previousName = _a.previousSeriesName, seriesTransformer = _a.seriesTransformer, field = _a.field, interval = _a.interval, showDaily = _a.showDaily, topEvents = _a.topEvents, orderby = _a.orderby, confirmedQuery = _a.confirmedQuery, colors = _a.colors, chartHeader = _a.chartHeader, legendOptions = _a.legendOptions, chartOptions = _a.chartOptions, preserveReleaseQueryParams = _a.preserveReleaseQueryParams, releaseQueryExtra = _a.releaseQueryExtra, disableableSeries = _a.disableableSeries, chartComponent = _a.chartComponent, usePageZoom = _a.usePageZoom, height = _a.height, props = tslib_1.__rest(_a, ["api", "period", "utc", "query", "router", "start", "end", "projects", "environments", "showLegend", "yAxis", "disablePrevious", "disableReleases", "emphasizeReleases", "currentSeriesName", "previousSeriesName", "seriesTransformer", "field", "interval", "showDaily", "topEvents", "orderby", "confirmedQuery", "colors", "chartHeader", "legendOptions", "chartOptions", "preserveReleaseQueryParams", "releaseQueryExtra", "disableableSeries", "chartComponent", "usePageZoom", "height"]);
        // Include previous only on relative dates (defaults to relative if no start and end)
        var includePrevious = !disablePrevious && !start && !end;
        var yAxisLabel = yAxis && fields_1.isEquation(yAxis) ? fields_1.getEquation(yAxis) : yAxis;
        if (yAxisLabel && yAxisLabel.length > 60) {
            yAxisLabel = yAxisLabel.substr(0, 60) + '...';
        }
        var previousSeriesName = previousName !== null && previousName !== void 0 ? previousName : (yAxisLabel ? locale_1.t('previous %s', yAxisLabel) : undefined);
        var currentSeriesName = currentName !== null && currentName !== void 0 ? currentName : yAxisLabel;
        var intervalVal = showDaily ? '1d' : interval || utils_1.getInterval(this.props, true);
        var chartImplementation = function (_a) {
            var zoomRenderProps = _a.zoomRenderProps, releaseSeries = _a.releaseSeries, errored = _a.errored, loading = _a.loading, reloading = _a.reloading, results = _a.results, timeseriesData = _a.timeseriesData, previousTimeseriesData = _a.previousTimeseriesData;
            if (errored) {
                return (<errorPanel_1.default>
            <icons_1.IconWarning color="gray300" size="lg"/>
          </errorPanel_1.default>);
            }
            var seriesData = results ? results : timeseriesData;
            return (<transitionChart_1.default loading={loading} reloading={reloading} height={height ? height + "px" : undefined}>
          <transparentLoadingMask_1.default visible={reloading}/>

          {React.isValidElement(chartHeader) && chartHeader}

          <ThemedChart zoomRenderProps={zoomRenderProps} loading={loading} reloading={reloading} showLegend={showLegend} releaseSeries={releaseSeries || []} timeseriesData={seriesData !== null && seriesData !== void 0 ? seriesData : []} previousTimeseriesData={previousTimeseriesData} currentSeriesName={currentSeriesName} previousSeriesName={previousSeriesName} seriesTransformer={seriesTransformer} stacked={typeof topEvents === 'number' && topEvents > 0} yAxis={yAxis} showDaily={showDaily} colors={colors} legendOptions={legendOptions} chartOptions={chartOptions} disableableSeries={disableableSeries} chartComponent={chartComponent} height={height}/>
        </transitionChart_1.default>);
        };
        if (!disableReleases) {
            var previousChart_1 = chartImplementation;
            chartImplementation = function (chartProps) { return (<releaseSeries_1.default utc={utc} period={period} start={start} end={end} projects={projects} environments={environments} emphasizeReleases={emphasizeReleases} preserveQueryParams={preserveReleaseQueryParams} queryExtra={releaseQueryExtra}>
          {function (_a) {
                var releaseSeries = _a.releaseSeries;
                return previousChart_1(tslib_1.__assign(tslib_1.__assign({}, chartProps), { releaseSeries: releaseSeries }));
            }}
        </releaseSeries_1.default>); };
        }
        return (<chartZoom_1.default router={router} period={period} start={start} end={end} utc={utc} usePageDate={usePageZoom} {...props}>
        {function (zoomRenderProps) { return (<eventsRequest_1.default {...props} api={api} period={period} project={projects} environment={environments} start={start} end={end} interval={intervalVal} query={query} includePrevious={includePrevious} currentSeriesName={currentSeriesName} previousSeriesName={previousSeriesName} yAxis={yAxis} field={field} orderby={orderby} topEvents={topEvents} confirmedQuery={confirmedQuery} partial>
            {function (eventData) {
                    return chartImplementation(tslib_1.__assign(tslib_1.__assign({}, eventData), { zoomRenderProps: zoomRenderProps }));
                }}
          </eventsRequest_1.default>); }}
      </chartZoom_1.default>);
    };
    return EventsChart;
}(React.Component));
exports.default = EventsChart;
//# sourceMappingURL=eventsChart.jsx.map