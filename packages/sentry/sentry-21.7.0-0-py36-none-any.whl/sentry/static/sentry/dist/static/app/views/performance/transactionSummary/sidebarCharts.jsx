Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var ReactRouter = tslib_1.__importStar(require("react-router"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var eventsRequest_1 = tslib_1.__importDefault(require("app/components/charts/eventsRequest"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var styles_1 = require("app/components/charts/styles");
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var utils_1 = require("app/components/charts/utils");
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var dates_1 = require("app/utils/dates");
var charts_1 = require("app/utils/discover/charts");
var formatters_1 = require("app/utils/formatters");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var data_1 = require("app/views/performance/data");
function SidebarCharts(_a) {
    var theme = _a.theme, api = _a.api, location = _a.location, eventView = _a.eventView, organization = _a.organization, router = _a.router, isLoading = _a.isLoading, error = _a.error, totals = _a.totals;
    var statsPeriod = eventView.statsPeriod;
    var start = eventView.start ? dates_1.getUtcToLocalDateObject(eventView.start) : undefined;
    var end = eventView.end ? dates_1.getUtcToLocalDateObject(eventView.end) : undefined;
    var utc = getParams_1.getParams(location.query).utc;
    var colors = theme.charts.getColorPalette(3);
    var axisLineConfig = {
        scale: true,
        axisLine: {
            show: false,
        },
        axisTick: {
            show: false,
        },
        splitLine: {
            show: false,
        },
    };
    var chartOptions = {
        height: 480,
        grid: [
            {
                top: '60px',
                left: '10px',
                right: '10px',
                height: '100px',
            },
            {
                top: '220px',
                left: '10px',
                right: '10px',
                height: '100px',
            },
            {
                top: '380px',
                left: '10px',
                right: '10px',
                height: '120px',
            },
        ],
        axisPointer: {
            // Link each x-axis together.
            link: [{ xAxisIndex: [0, 1, 2] }],
        },
        xAxes: Array.from(new Array(3)).map(function (_i, index) { return ({
            gridIndex: index,
            type: 'time',
            show: false,
        }); }),
        yAxes: [
            tslib_1.__assign({ 
                // apdex
                gridIndex: 0, interval: 0.2, axisLabel: {
                    formatter: function (value) { return formatters_1.formatFloat(value, 1); },
                    color: theme.chartLabel,
                } }, axisLineConfig),
            tslib_1.__assign({ 
                // failure rate
                gridIndex: 1, splitNumber: 4, interval: 0.5, max: 1.0, axisLabel: {
                    formatter: function (value) { return formatters_1.formatPercentage(value, 0); },
                    color: theme.chartLabel,
                } }, axisLineConfig),
            tslib_1.__assign({ 
                // throughput
                gridIndex: 2, splitNumber: 4, axisLabel: {
                    formatter: formatters_1.formatAbbreviatedNumber,
                    color: theme.chartLabel,
                } }, axisLineConfig),
        ],
        utc: utc === 'true',
        isGroupedByDate: true,
        showTimeInTooltip: true,
        colors: [colors[0], colors[1], colors[2]],
        tooltip: {
            trigger: 'axis',
            truncate: 80,
            valueFormatter: charts_1.tooltipFormatter,
            nameFormatter: function (value) {
                return value === 'epm()' ? 'tpm()' : value;
            },
        },
    };
    var datetimeSelection = {
        start: start || null,
        end: end || null,
        period: statsPeriod,
    };
    var project = eventView.project;
    var environment = eventView.environment;
    var threshold = organization.apdexThreshold;
    var apdexKey, apdexYAxis;
    var apdexPerformanceTerm;
    if (organization.features.includes('project-transaction-threshold')) {
        apdexKey = 'apdex';
        apdexPerformanceTerm = data_1.PERFORMANCE_TERM.APDEX_NEW;
        apdexYAxis = 'apdex()';
    }
    else {
        apdexKey = "apdex_" + threshold;
        apdexPerformanceTerm = data_1.PERFORMANCE_TERM.APDEX;
        apdexYAxis = "apdex(" + organization.apdexThreshold + ")";
    }
    return (<RelativeBox>
      <ChartLabel top="0px">
        <ChartTitle>
          {locale_1.t('Apdex')}
          <questionTooltip_1.default position="top" title={data_1.getTermHelp(organization, apdexPerformanceTerm)} size="sm"/>
        </ChartTitle>
        <ChartSummaryValue isLoading={isLoading} error={error} value={totals ? formatters_1.formatFloat(totals[apdexKey], 4) : null}/>
      </ChartLabel>

      <ChartLabel top="160px">
        <ChartTitle>
          {locale_1.t('Failure Rate')}
          <questionTooltip_1.default position="top" title={data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.FAILURE_RATE)} size="sm"/>
        </ChartTitle>
        <ChartSummaryValue isLoading={isLoading} error={error} value={totals ? formatters_1.formatPercentage(totals.failure_rate) : null}/>
      </ChartLabel>

      <ChartLabel top="320px">
        <ChartTitle>
          {locale_1.t('TPM')}
          <questionTooltip_1.default position="top" title={data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.TPM)} size="sm"/>
        </ChartTitle>
        <ChartSummaryValue isLoading={isLoading} error={error} value={totals ? locale_1.tct('[tpm] tpm', { tpm: formatters_1.formatFloat(totals.tpm, 4) }) : null}/>
      </ChartLabel>

      <chartZoom_1.default router={router} period={statsPeriod} start={start} end={end} utc={utc === 'true'} xAxisIndex={[0, 1, 2]}>
        {function (zoomRenderProps) { return (<eventsRequest_1.default api={api} organization={organization} period={statsPeriod} project={project} environment={environment} start={start} end={end} interval={utils_1.getInterval(datetimeSelection)} showLoading={false} query={eventView.query} includePrevious={false} yAxis={[apdexYAxis, 'failure_rate()', 'epm()']} partial>
            {function (_a) {
                var results = _a.results, errored = _a.errored, loading = _a.loading, reloading = _a.reloading;
                if (errored) {
                    return (<errorPanel_1.default height="580px">
                    <icons_1.IconWarning color="gray300" size="lg"/>
                  </errorPanel_1.default>);
                }
                var series = results
                    ? results.map(function (values, i) { return (tslib_1.__assign(tslib_1.__assign({}, values), { yAxisIndex: i, xAxisIndex: i })); })
                    : [];
                return (<transitionChart_1.default loading={loading} reloading={reloading} height="580px">
                  <transparentLoadingMask_1.default visible={reloading}/>
                  <lineChart_1.default {...zoomRenderProps} {...chartOptions} series={series}/>
                </transitionChart_1.default>);
            }}
          </eventsRequest_1.default>); }}
      </chartZoom_1.default>
    </RelativeBox>);
}
function ChartSummaryValue(_a) {
    var error = _a.error, isLoading = _a.isLoading, value = _a.value;
    if (error) {
        return <div>{'\u2014'}</div>;
    }
    else if (isLoading) {
        return <placeholder_1.default height="24px"/>;
    }
    else {
        return <ChartValue>{value}</ChartValue>;
    }
}
var RelativeBox = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var ChartTitle = styled_1.default(styles_1.SectionHeading)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var ChartLabel = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  z-index: 1;\n"], ["\n  position: absolute;\n  top: ", ";\n  z-index: 1;\n"])), function (p) { return p.top; });
var ChartValue = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
exports.default = withApi_1.default(react_1.withTheme(ReactRouter.withRouter(SidebarCharts)));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=sidebarCharts.jsx.map