Object.defineProperty(exports, "__esModule", { value: true });
exports.HistogramChart = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var barChart_1 = tslib_1.__importDefault(require("app/components/charts/barChart"));
var barChartZoom_1 = tslib_1.__importDefault(require("app/components/charts/barChartZoom"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var styles_1 = require("app/components/charts/styles");
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var iconWarning_1 = require("app/icons/iconWarning");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var histogramQuery_1 = tslib_1.__importDefault(require("app/utils/performance/histogram/histogramQuery"));
var utils_1 = require("app/utils/performance/histogram/utils");
var styles_2 = require("../../styles");
var utils_2 = require("../display/utils");
var NUM_BUCKETS = 50;
var PRECISION = 0;
function HistogramChart(props) {
    var theme = props.theme, location = props.location, onFilterChange = props.onFilterChange, organization = props.organization, eventView = props.eventView, field = props.field, title = props.title, titleTooltip = props.titleTooltip, didReceiveMultiAxis = props.didReceiveMultiAxis, backupField = props.backupField, usingBackupAxis = props.usingBackupAxis;
    var _backupField = backupField ? [backupField] : [];
    var xAxis = {
        type: 'category',
        truncate: true,
        boundaryGap: false,
        axisTick: {
            alignWithLabel: true,
        },
    };
    return (<div>
      <styles_2.DoubleHeaderContainer>
        <styles_1.HeaderTitleLegend>
          {title}
          <questionTooltip_1.default position="top" size="sm" title={titleTooltip}/>
        </styles_1.HeaderTitleLegend>
      </styles_2.DoubleHeaderContainer>
      <histogramQuery_1.default location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={NUM_BUCKETS} precision={PRECISION} fields={tslib_1.__spreadArray([field], tslib_1.__read(_backupField))} dataFilter="exclude_outliers" didReceiveMultiAxis={didReceiveMultiAxis}>
        {function (results) {
            var _a;
            var _field = usingBackupAxis ? utils_2.getFieldOrBackup(field, backupField) : field;
            var loading = results.isLoading;
            var errored = results.error !== null;
            var chartData = (_a = results.histograms) === null || _a === void 0 ? void 0 : _a[_field];
            if (errored) {
                return (<errorPanel_1.default height="250px">
                <iconWarning_1.IconWarning color="gray300" size="lg"/>
              </errorPanel_1.default>);
            }
            if (!chartData) {
                return null;
            }
            var series = {
                seriesName: locale_1.t('Count'),
                data: utils_1.formatHistogramData(chartData, { type: 'duration' }),
            };
            var allSeries = [];
            if (!loading && !errored) {
                allSeries.push(series);
            }
            var yAxis = {
                type: 'value',
                axisLabel: {
                    color: theme.chartLabel,
                },
            };
            return (<react_1.Fragment>
              <barChartZoom_1.default minZoomWidth={Math.pow(10, -PRECISION) * NUM_BUCKETS} location={location} paramStart={_field + ":>="} paramEnd={_field + ":<="} xAxisIndex={[0]} buckets={utils_1.computeBuckets(chartData)} onHistoryPush={onFilterChange}>
                {function (zoomRenderProps) {
                    return (<BarChartContainer>
                      <MaskContainer>
                        <transparentLoadingMask_1.default visible={loading}/>
                        {getDynamicText_1.default({
                            value: (<barChart_1.default height={250} series={allSeries} xAxis={xAxis} yAxis={yAxis} grid={{
                                    left: space_1.default(3),
                                    right: space_1.default(3),
                                    top: space_1.default(3),
                                    bottom: loading ? space_1.default(4) : space_1.default(1.5),
                                }} stacked {...zoomRenderProps}/>),
                            fixed: <placeholder_1.default height="250px" testId="skeleton-ui"/>,
                        })}
                      </MaskContainer>
                    </BarChartContainer>);
                }}
              </barChartZoom_1.default>
            </react_1.Fragment>);
        }}
      </histogramQuery_1.default>
    </div>);
}
exports.HistogramChart = HistogramChart;
var BarChartContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding-top: ", ";\n  position: relative;\n"], ["\n  padding-top: ", ";\n  position: relative;\n"])), space_1.default(1));
var MaskContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
exports.default = react_2.withTheme(HistogramChart);
var templateObject_1, templateObject_2;
//# sourceMappingURL=histogramChart.jsx.map