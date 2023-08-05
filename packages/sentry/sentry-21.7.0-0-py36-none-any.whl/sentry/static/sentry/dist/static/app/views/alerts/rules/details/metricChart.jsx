Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var color_1 = tslib_1.__importDefault(require("color"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var moment_timezone_1 = tslib_1.__importDefault(require("moment-timezone"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var graphic_1 = tslib_1.__importDefault(require("app/components/charts/components/graphic"));
var markArea_1 = tslib_1.__importDefault(require("app/components/charts/components/markArea"));
var markLine_1 = tslib_1.__importDefault(require("app/components/charts/components/markLine"));
var eventsRequest_1 = tslib_1.__importDefault(require("app/components/charts/eventsRequest"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var styles_1 = require("app/components/charts/styles");
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var dates_1 = require("app/utils/dates");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var details_1 = require("app/views/alerts/details");
var incidentRulePresets_1 = require("app/views/alerts/incidentRules/incidentRulePresets");
var options_1 = require("app/views/alerts/wizard/options");
var utils_1 = require("app/views/alerts/wizard/utils");
var types_1 = require("../../types");
var X_AXIS_BOUNDARY_GAP = 20;
var VERTICAL_PADDING = 22;
function formatTooltipDate(date, format) {
    var timezone = configStore_1.default.get('user').options.timezone;
    return moment_timezone_1.default.tz(date, timezone).format(format);
}
function createThresholdSeries(lineColor, threshold) {
    return {
        seriesName: 'Threshold Line',
        type: 'line',
        markLine: markLine_1.default({
            silent: true,
            lineStyle: { color: lineColor, type: 'dashed', width: 1 },
            data: [{ yAxis: threshold }],
            label: {
                show: false,
            },
        }),
        data: [],
    };
}
function createStatusAreaSeries(lineColor, startTime, endTime) {
    return {
        seriesName: 'Status Area',
        type: 'line',
        markLine: markLine_1.default({
            silent: true,
            lineStyle: { color: lineColor, type: 'solid', width: 4 },
            data: [[{ coord: [startTime, 0] }, { coord: [endTime, 0] }]],
        }),
        data: [],
    };
}
function createIncidentSeries(router, organization, lineColor, incidentTimestamp, incident, dataPoint, seriesName) {
    var series = {
        seriesName: 'Incident Line',
        type: 'line',
        markLine: markLine_1.default({
            silent: false,
            lineStyle: { color: lineColor, type: 'solid' },
            data: [
                {
                    xAxis: incidentTimestamp,
                    onClick: function () {
                        router.push({
                            pathname: details_1.alertDetailsLink(organization, incident),
                            query: { alert: incident.identifier },
                        });
                    },
                },
            ],
            label: {
                show: incident.identifier,
                position: 'insideEndBottom',
                formatter: incident.identifier,
                color: lineColor,
                fontSize: 10,
                fontFamily: 'Rubik',
            },
        }),
        data: [],
    };
    // tooltip conflicts with MarkLine types
    series.markLine.tooltip = {
        trigger: 'item',
        alwaysShowContent: true,
        formatter: function (_a) {
            var _b;
            var value = _a.value, marker = _a.marker;
            var time = formatTooltipDate(moment_1.default(value), 'MMM D, YYYY LT');
            return [
                "<div class=\"tooltip-series\"><div>",
                "<span class=\"tooltip-label\">" + marker + " <strong>" + locale_1.t('Alert') + " #" + incident.identifier + "</strong></span>" + seriesName + " " + ((_b = dataPoint === null || dataPoint === void 0 ? void 0 : dataPoint.value) === null || _b === void 0 ? void 0 : _b.toLocaleString()),
                "</div></div>",
                "<div class=\"tooltip-date\">" + time + "</div>",
                "<div class=\"tooltip-arrow\"></div>",
            ].join('');
        },
    };
    return series;
}
var MetricChart = /** @class */ (function (_super) {
    tslib_1.__extends(MetricChart, _super);
    function MetricChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            width: -1,
            height: -1,
        };
        _this.ref = null;
        /**
         * Syncs component state with the chart's width/heights
         */
        _this.updateDimensions = function () {
            var _a, _b;
            var chartRef = (_b = (_a = _this.ref) === null || _a === void 0 ? void 0 : _a.getEchartsInstance) === null || _b === void 0 ? void 0 : _b.call(_a);
            if (!chartRef) {
                return;
            }
            var width = chartRef.getWidth();
            var height = chartRef.getHeight();
            if (width !== _this.state.width || height !== _this.state.height) {
                _this.setState({
                    width: width,
                    height: height,
                });
            }
        };
        _this.handleRef = function (ref) {
            if (ref && !_this.ref) {
                _this.ref = ref;
                _this.updateDimensions();
            }
            if (!ref) {
                _this.ref = null;
            }
        };
        _this.getRuleChangeThresholdElements = function (data) {
            var _a = _this.state, height = _a.height, width = _a.width;
            var dateModified = (_this.props.rule || {}).dateModified;
            if (!data.length || !data[0].data.length || !dateModified) {
                return [];
            }
            var seriesData = data[0].data;
            var seriesStart = seriesData[0].name;
            var seriesEnd = seriesData[seriesData.length - 1].name;
            var ruleChanged = moment_1.default(dateModified).valueOf();
            if (ruleChanged < seriesStart) {
                return [];
            }
            var chartWidth = width - X_AXIS_BOUNDARY_GAP;
            var position = X_AXIS_BOUNDARY_GAP +
                Math.round((chartWidth * (ruleChanged - seriesStart)) / (seriesEnd - seriesStart));
            return [
                {
                    type: 'line',
                    draggable: false,
                    position: [position, 0],
                    shape: { y1: 0, y2: height - VERTICAL_PADDING, x1: 1, x2: 1 },
                    style: {
                        stroke: theme_1.default.gray200,
                    },
                },
                {
                    type: 'rect',
                    draggable: false,
                    position: [X_AXIS_BOUNDARY_GAP, 0],
                    shape: {
                        // +1 makes the gray area go midway onto the dashed line above
                        width: position - X_AXIS_BOUNDARY_GAP + 1,
                        height: height - VERTICAL_PADDING,
                    },
                    style: {
                        fill: color_1.default(theme_1.default.gray100).alpha(0.42).rgb().string(),
                    },
                },
            ];
        };
        return _this;
    }
    MetricChart.prototype.renderChartActions = function (totalDuration, criticalDuration, warningDuration) {
        var _a = this.props, rule = _a.rule, orgId = _a.orgId, projects = _a.projects, timePeriod = _a.timePeriod, query = _a.query;
        var ctaOpts = {
            orgSlug: orgId,
            projects: projects,
            rule: rule,
            eventType: query,
            start: timePeriod.start,
            end: timePeriod.end,
        };
        var _b = incidentRulePresets_1.makeDefaultCta(ctaOpts), buttonText = _b.buttonText, props = tslib_1.__rest(_b, ["buttonText"]);
        var resolvedPercent = ((100 * Math.max(totalDuration - criticalDuration - warningDuration, 0)) /
            totalDuration).toFixed(2);
        var criticalPercent = (100 * Math.min(criticalDuration / totalDuration, 1)).toFixed(2);
        var warningPercent = (100 * Math.min(warningDuration / totalDuration, 1)).toFixed(2);
        return (<ChartActions>
        <ChartSummary>
          <SummaryText>{locale_1.t('SUMMARY')}</SummaryText>
          <SummaryStats>
            <StatItem>
              <icons_1.IconCheckmark color="green300" isCircled/>
              <StatCount>{resolvedPercent}%</StatCount>
            </StatItem>
            <StatItem>
              <icons_1.IconWarning color="yellow300"/>
              <StatCount>{warningPercent}%</StatCount>
            </StatItem>
            <StatItem>
              <icons_1.IconFire color="red300"/>
              <StatCount>{criticalPercent}%</StatCount>
            </StatItem>
          </SummaryStats>
        </ChartSummary>
        <feature_1.default features={['discover-basic']}>
          <button_1.default size="small" {...props}>
            {buttonText}
          </button_1.default>
        </feature_1.default>
      </ChartActions>);
    };
    MetricChart.prototype.renderChart = function (data, series, areaSeries, maxThresholdValue, maxSeriesValue) {
        var _this = this;
        var _a = this.props, router = _a.router, interval = _a.interval, handleZoom = _a.handleZoom, _b = _a.timePeriod, start = _b.start, end = _b.end;
        var _c = this.props.rule || {}, dateModified = _c.dateModified, timeWindow = _c.timeWindow;
        return (<chartZoom_1.default router={router} start={start} end={end} onZoom={function (zoomArgs) { return handleZoom(zoomArgs.start, zoomArgs.end); }}>
        {function (zoomRenderProps) { return (<lineChart_1.default {...zoomRenderProps} isGroupedByDate showTimeInTooltip forwardedRef={_this.handleRef} grid={{
                    left: 0,
                    right: space_1.default(2),
                    top: space_1.default(2),
                    bottom: 0,
                }} yAxis={maxThresholdValue > maxSeriesValue ? { max: maxThresholdValue } : undefined} series={tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(series)), tslib_1.__read(areaSeries))} graphic={graphic_1.default({
                    elements: _this.getRuleChangeThresholdElements(data),
                })} tooltip={{
                    formatter: function (seriesParams) {
                        var _a;
                        // seriesParams can be object instead of array
                        var pointSeries = Array.isArray(seriesParams)
                            ? seriesParams
                            : [seriesParams];
                        var _b = pointSeries[0], marker = _b.marker, pointData = _b.data, seriesName = _b.seriesName;
                        var _c = tslib_1.__read(pointData, 2), pointX = _c[0], pointY = _c[1];
                        var isModified = dateModified && pointX <= new Date(dateModified).getTime();
                        var startTime = formatTooltipDate(moment_1.default(pointX), 'MMM D LT');
                        var _d = (_a = getParams_1.parseStatsPeriod(interval)) !== null && _a !== void 0 ? _a : {
                            periodLength: 'm',
                            period: "" + timeWindow,
                        }, period = _d.period, periodLength = _d.periodLength;
                        var endTime = formatTooltipDate(moment_1.default(pointX).add(parseInt(period, 10), periodLength), 'MMM D LT');
                        var title = isModified
                            ? "<strong>" + locale_1.t('Alert Rule Modified') + "</strong>"
                            : marker + " <strong>" + seriesName + "</strong>";
                        var value = isModified
                            ? seriesName + " " + pointY.toLocaleString()
                            : pointY.toLocaleString();
                        return [
                            "<div class=\"tooltip-series\"><div>",
                            "<span class=\"tooltip-label\">" + title + "</span>" + value,
                            "</div></div>",
                            "<div class=\"tooltip-date\">" + startTime + " &mdash; " + endTime + "</div>",
                            "<div class=\"tooltip-arrow\"></div>",
                        ].join('');
                    },
                }} onFinished={function () {
                    // We want to do this whenever the chart finishes re-rendering so that we can update the dimensions of
                    // any graphics related to the triggers (e.g. the threshold areas + boundaries)
                    _this.updateDimensions();
                }}/>); }}
      </chartZoom_1.default>);
    };
    MetricChart.prototype.renderEmpty = function () {
        return (<ChartPanel>
        <panels_1.PanelBody withPadding>
          <placeholder_1.default height="200px"/>
        </panels_1.PanelBody>
      </ChartPanel>);
    };
    MetricChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, router = _a.router, rule = _a.rule, organization = _a.organization, timePeriod = _a.timePeriod, selectedIncident = _a.selectedIncident, projects = _a.projects, interval = _a.interval, filter = _a.filter, query = _a.query, incidents = _a.incidents;
        var criticalTrigger = rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTrigger = rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'warning';
        });
        // If the chart duration isn't as long as the rollup duration the events-stats
        // endpoint will return an invalid timeseriesData data set
        var viableStartDate = dates_1.getUtcDateString(moment_1.default.min(moment_1.default.utc(timePeriod.start), moment_1.default.utc(timePeriod.end).subtract(rule.timeWindow, 'minutes')));
        var viableEndDate = dates_1.getUtcDateString(moment_1.default.utc(timePeriod.end).add(rule.timeWindow, 'minutes'));
        return (<eventsRequest_1.default api={api} organization={organization} query={query} environment={rule.environment ? [rule.environment] : undefined} project={projects
                .filter(function (p) { return p && p.slug; })
                .map(function (project) { return Number(project.id); })} interval={interval} start={viableStartDate} end={viableEndDate} yAxis={rule.aggregate} includePrevious={false} currentSeriesName={rule.aggregate} partial={false}>
        {function (_a) {
                var loading = _a.loading, timeseriesData = _a.timeseriesData;
                if (loading || !timeseriesData) {
                    return _this.renderEmpty();
                }
                var series = tslib_1.__spreadArray([], tslib_1.__read(timeseriesData));
                var areaSeries = [];
                // Ensure series data appears above incident lines
                series[0].z = 100;
                var dataArr = timeseriesData[0].data;
                var maxSeriesValue = dataArr.reduce(function (currMax, coord) { return Math.max(currMax, coord.value); }, 0);
                var firstPoint = Number(dataArr[0].name);
                var lastPoint = dataArr[dataArr.length - 1].name;
                var totalDuration = lastPoint - firstPoint;
                var criticalDuration = 0;
                var warningDuration = 0;
                series.push(createStatusAreaSeries(theme_1.default.green300, firstPoint, lastPoint));
                if (incidents) {
                    // select incidents that fall within the graph range
                    var periodStart_1 = moment_1.default.utc(firstPoint);
                    incidents
                        .filter(function (incident) {
                        return !incident.dateClosed || moment_1.default(incident.dateClosed).isAfter(periodStart_1);
                    })
                        .forEach(function (incident) {
                        var _a, _b;
                        var statusChanges = (_a = incident.activities) === null || _a === void 0 ? void 0 : _a.filter(function (_a) {
                            var type = _a.type, value = _a.value;
                            return type === types_1.IncidentActivityType.STATUS_CHANGE &&
                                value &&
                                [
                                    "" + types_1.IncidentStatus.WARNING,
                                    "" + types_1.IncidentStatus.CRITICAL,
                                ].includes(value);
                        }).sort(function (a, b) {
                            return moment_1.default(a.dateCreated).valueOf() - moment_1.default(b.dateCreated).valueOf();
                        });
                        var incidentEnd = (_b = incident.dateClosed) !== null && _b !== void 0 ? _b : moment_1.default().valueOf();
                        var timeWindowMs = rule.timeWindow * 60 * 1000;
                        var incidentColor = warningTrigger &&
                            statusChanges &&
                            !statusChanges.find(function (_a) {
                                var value = _a.value;
                                return value === "" + types_1.IncidentStatus.CRITICAL;
                            })
                            ? theme_1.default.yellow300
                            : theme_1.default.red300;
                        var incidentStartDate = moment_1.default(incident.dateStarted).valueOf();
                        var incidentCloseDate = incident.dateClosed
                            ? moment_1.default(incident.dateClosed).valueOf()
                            : lastPoint;
                        var incidentStartValue = dataArr.find(function (point) { return point.name >= incidentStartDate; });
                        series.push(createIncidentSeries(router, organization, incidentColor, incidentStartDate, incident, incidentStartValue, series[0].seriesName));
                        var areaStart = Math.max(moment_1.default(incident.dateStarted).valueOf(), firstPoint);
                        var areaEnd = Math.min((statusChanges === null || statusChanges === void 0 ? void 0 : statusChanges.length) && statusChanges[0].dateCreated
                            ? moment_1.default(statusChanges[0].dateCreated).valueOf() - timeWindowMs
                            : moment_1.default(incidentEnd).valueOf(), lastPoint);
                        var areaColor = warningTrigger ? theme_1.default.yellow300 : theme_1.default.red300;
                        if (areaEnd > areaStart) {
                            series.push(createStatusAreaSeries(areaColor, areaStart, areaEnd));
                            if (areaColor === theme_1.default.yellow300) {
                                warningDuration += Math.abs(areaEnd - areaStart);
                            }
                            else {
                                criticalDuration += Math.abs(areaEnd - areaStart);
                            }
                        }
                        statusChanges === null || statusChanges === void 0 ? void 0 : statusChanges.forEach(function (activity, idx) {
                            var statusAreaStart = Math.max(moment_1.default(activity.dateCreated).valueOf() - timeWindowMs, firstPoint);
                            var statusAreaEnd = Math.min(idx === statusChanges.length - 1
                                ? moment_1.default(incidentEnd).valueOf()
                                : moment_1.default(statusChanges[idx + 1].dateCreated).valueOf() -
                                    timeWindowMs, lastPoint);
                            var statusAreaColor = activity.value === "" + types_1.IncidentStatus.CRITICAL
                                ? theme_1.default.red300
                                : theme_1.default.yellow300;
                            if (statusAreaEnd > statusAreaStart) {
                                series.push(createStatusAreaSeries(statusAreaColor, statusAreaStart, statusAreaEnd));
                                if (statusAreaColor === theme_1.default.yellow300) {
                                    warningDuration += Math.abs(statusAreaEnd - statusAreaStart);
                                }
                                else {
                                    criticalDuration += Math.abs(statusAreaEnd - statusAreaStart);
                                }
                            }
                        });
                        if (selectedIncident && incident.id === selectedIncident.id) {
                            var selectedIncidentColor = incidentColor === theme_1.default.yellow300 ? theme_1.default.yellow100 : theme_1.default.red100;
                            areaSeries.push({
                                type: 'line',
                                markArea: markArea_1.default({
                                    silent: true,
                                    itemStyle: {
                                        color: color_1.default(selectedIncidentColor).alpha(0.42).rgb().string(),
                                    },
                                    data: [
                                        [{ xAxis: incidentStartDate }, { xAxis: incidentCloseDate }],
                                    ],
                                }),
                                data: [],
                            });
                        }
                    });
                }
                var maxThresholdValue = 0;
                if (warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold) {
                    var alertThreshold = warningTrigger.alertThreshold;
                    var warningThresholdLine = createThresholdSeries(theme_1.default.yellow300, alertThreshold);
                    series.push(warningThresholdLine);
                    maxThresholdValue = Math.max(maxThresholdValue, alertThreshold);
                }
                if (criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold) {
                    var alertThreshold = criticalTrigger.alertThreshold;
                    var criticalThresholdLine = createThresholdSeries(theme_1.default.red300, alertThreshold);
                    series.push(criticalThresholdLine);
                    maxThresholdValue = Math.max(maxThresholdValue, alertThreshold);
                }
                return (<ChartPanel>
              <StyledPanelBody withPadding>
                <ChartHeader>
                  <ChartTitle>
                    {options_1.AlertWizardAlertNames[utils_1.getAlertTypeFromAggregateDataset(rule)]}
                  </ChartTitle>
                  {filter}
                </ChartHeader>
                {_this.renderChart(timeseriesData, series, areaSeries, maxThresholdValue, maxSeriesValue)}
              </StyledPanelBody>
              {_this.renderChartActions(totalDuration, criticalDuration, warningDuration)}
            </ChartPanel>);
            }}
      </eventsRequest_1.default>);
    };
    return MetricChart;
}(React.PureComponent));
exports.default = react_router_1.withRouter(MetricChart);
var ChartPanel = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(2));
var ChartHeader = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(3));
var ChartTitle = styled_1.default('header')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n"], ["\n  display: flex;\n  flex-direction: row;\n"])));
var ChartActions = styled_1.default(panels_1.PanelFooter)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  padding: ", " 20px;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  padding: ", " 20px;\n"])), space_1.default(1));
var ChartSummary = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-right: auto;\n"], ["\n  display: flex;\n  margin-right: auto;\n"])));
var SummaryText = styled_1.default(styles_1.SectionHeading)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  display: flex;\n  align-items: center;\n  margin: 0;\n  font-weight: bold;\n  font-size: ", ";\n  line-height: 1;\n"], ["\n  flex: 1;\n  display: flex;\n  align-items: center;\n  margin: 0;\n  font-weight: bold;\n  font-size: ", ";\n  line-height: 1;\n"])), function (p) { return p.theme.fontSizeSmall; });
var SummaryStats = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0 ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0 ", ";\n"])), space_1.default(2));
var StatItem = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0 ", " 0 0;\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0 ", " 0 0;\n"])), space_1.default(2));
/* Override padding to make chart appear centered */
var StyledPanelBody = styled_1.default(panels_1.PanelBody)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  padding-right: 6px;\n"], ["\n  padding-right: 6px;\n"])));
var StatCount = styled_1.default('span')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  margin-top: ", ";\n  color: ", ";\n"], ["\n  margin-left: ", ";\n  margin-top: ", ";\n  color: ", ";\n"])), space_1.default(0.5), space_1.default(0.25), function (p) { return p.theme.textColor; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=metricChart.jsx.map