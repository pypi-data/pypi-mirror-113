Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var compact_1 = tslib_1.__importDefault(require("lodash/compact"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var styles_1 = require("app/components/charts/styles");
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var utils_1 = require("app/components/charts/utils");
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_2 = require("app/utils");
var formatters_1 = require("app/utils/formatters");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var utils_3 = require("app/views/releases/list/utils");
var releaseHealthRequest_1 = require("app/views/releases/utils/releaseHealthRequest");
var ReleaseAdoptionChart = /** @class */ (function (_super) {
    tslib_1.__extends(ReleaseAdoptionChart, _super);
    function ReleaseAdoptionChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        _this.handleClick = function (params) {
            var _a = _this.props, organization = _a.organization, router = _a.router, selection = _a.selection, location = _a.location;
            var project = selection.projects[0];
            router.push({
                pathname: "/organizations/" + (organization === null || organization === void 0 ? void 0 : organization.slug) + "/releases/" + encodeURIComponent(params.seriesId) + "/",
                query: { project: project, environment: location.query.environment },
            });
        };
        return _this;
    }
    // TODO(release-adoption-chart): refactor duplication
    ReleaseAdoptionChart.prototype.getInterval = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var datetimeObj = {
            start: location.query.start,
            end: location.query.end,
            period: location.query.statsPeriod,
            utc: location.query.utc,
        };
        var diffInMinutes = utils_1.getDiffInMinutes(datetimeObj);
        // use high fidelity intervals when available
        // limit on backend is set to six hour
        if (organization.features.includes('minute-resolution-sessions') &&
            diffInMinutes < 360) {
            return '10m';
        }
        if (diffInMinutes >= utils_1.ONE_WEEK) {
            return '1d';
        }
        else {
            return '1h';
        }
    };
    ReleaseAdoptionChart.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, activeDisplay = _a.activeDisplay;
        var hasSemverFeature = organization.features.includes('semver');
        return [
            [
                'sessions',
                "/organizations/" + organization.slug + "/sessions/",
                {
                    query: tslib_1.__assign(tslib_1.__assign({ interval: this.getInterval() }, getParams_1.getParams(pick_1.default(location.query, Object.values(globalSelectionHeader_1.URL_PARAM)))), { groupBy: ['release'], field: [releaseHealthRequest_1.sessionDisplayToField(activeDisplay)], query: location.query.query
                            ? hasSemverFeature
                                ? location.query.query
                                : "release:" + location.query.query
                            : undefined }),
                },
            ],
        ];
    };
    ReleaseAdoptionChart.prototype.getReleasesSeries = function () {
        var _a;
        var activeDisplay = this.props.activeDisplay;
        var sessions = this.state.sessions;
        var releases = sessions === null || sessions === void 0 ? void 0 : sessions.groups.map(function (group) { return group.by.release; });
        if (!releases) {
            return null;
        }
        var totalData = (_a = sessions === null || sessions === void 0 ? void 0 : sessions.groups) === null || _a === void 0 ? void 0 : _a.reduce(function (acc, group) {
            return releaseHealthRequest_1.reduceTimeSeriesGroups(acc, group, releaseHealthRequest_1.sessionDisplayToField(activeDisplay));
        }, []);
        return releases.map(function (release) {
            var _a, _b;
            var releaseData = (_a = sessions === null || sessions === void 0 ? void 0 : sessions.groups.find(function (_a) {
                var by = _a.by;
                return by.release === release;
            })) === null || _a === void 0 ? void 0 : _a.series[releaseHealthRequest_1.sessionDisplayToField(activeDisplay)];
            return {
                id: release,
                seriesName: formatters_1.formatVersion(release),
                data: (_b = sessions === null || sessions === void 0 ? void 0 : sessions.intervals.map(function (interval, index) {
                    var _a, _b;
                    return ({
                        name: moment_1.default(interval).valueOf(),
                        value: utils_2.percent((_a = releaseData === null || releaseData === void 0 ? void 0 : releaseData[index]) !== null && _a !== void 0 ? _a : 0, (_b = totalData === null || totalData === void 0 ? void 0 : totalData[index]) !== null && _b !== void 0 ? _b : 0),
                    });
                })) !== null && _b !== void 0 ? _b : [],
            };
        });
    };
    ReleaseAdoptionChart.prototype.getTotal = function () {
        var activeDisplay = this.props.activeDisplay;
        var sessions = this.state.sessions;
        return ((sessions === null || sessions === void 0 ? void 0 : sessions.groups.reduce(function (acc, group) { return acc + group.totals[releaseHealthRequest_1.sessionDisplayToField(activeDisplay)]; }, 0)) || 0);
    };
    ReleaseAdoptionChart.prototype.renderEmpty = function () {
        return (<panels_1.Panel>
        <panels_1.PanelBody withPadding>
          <ChartHeader>
            <placeholder_1.default height="24px"/>
          </ChartHeader>
          <placeholder_1.default height="200px"/>
        </panels_1.PanelBody>
        <ChartFooter>
          <placeholder_1.default height="34px"/>
        </ChartFooter>
      </panels_1.Panel>);
    };
    ReleaseAdoptionChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, activeDisplay = _a.activeDisplay, router = _a.router, selection = _a.selection;
        var _b = selection.datetime, start = _b.start, end = _b.end, period = _b.period, utc = _b.utc;
        var _c = this.state, loading = _c.loading, reloading = _c.reloading, sessions = _c.sessions;
        var releasesSeries = this.getReleasesSeries();
        var totalCount = this.getTotal();
        if ((loading && !reloading) || (reloading && totalCount === 0) || !sessions) {
            return this.renderEmpty();
        }
        if (!(releasesSeries === null || releasesSeries === void 0 ? void 0 : releasesSeries.length)) {
            return null;
        }
        var interval = this.getInterval();
        var numDataPoints = releasesSeries[0].data.length;
        return (<panels_1.Panel>
        <panels_1.PanelBody withPadding>
          <ChartHeader>
            <ChartTitle>{locale_1.t('Release Adoption')}</ChartTitle>
          </ChartHeader>
          <transitionChart_1.default loading={loading} reloading={reloading}>
            <transparentLoadingMask_1.default visible={reloading}/>
            <chartZoom_1.default router={router} period={period} utc={utc} start={start} end={end}>
              {function (zoomRenderProps) { return (<lineChart_1.default {...zoomRenderProps} grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }} series={releasesSeries} yAxis={{
                    min: 0,
                    max: 100,
                    type: 'value',
                    interval: 10,
                    splitNumber: 10,
                    data: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                    axisLabel: {
                        formatter: '{value}%',
                    },
                }} tooltip={{
                    formatter: function (seriesParams) {
                        var series = Array.isArray(seriesParams)
                            ? seriesParams
                            : [seriesParams];
                        var timestamp = series[0].data[0];
                        var _a = tslib_1.__read(series
                            .filter(function (s) { return s.data[1] > 0; })
                            .sort(function (a, b) { return b.data[1] - a.data[1]; })), first = _a[0], second = _a[1], third = _a[2], rest = _a.slice(3);
                        var restSum = rest.reduce(function (acc, s) { return acc + s.data[1]; }, 0);
                        var seriesToRender = compact_1.default([first, second, third]);
                        if (rest.length) {
                            seriesToRender.push({
                                seriesName: locale_1.tn('%s Other', '%s Others', rest.length),
                                data: [timestamp, restSum],
                                marker: '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;"></span>',
                            });
                        }
                        if (!seriesToRender.length) {
                            return '<div/>';
                        }
                        var periodObj = getParams_1.parseStatsPeriod(interval) || {
                            periodLength: 'd',
                            period: '1',
                        };
                        var intervalStart = moment_1.default(timestamp).format('MMM D LT');
                        var intervalEnd = (series[0].dataIndex === numDataPoints - 1
                            ? moment_1.default(sessions.end)
                            : moment_1.default(timestamp).add(parseInt(periodObj.period, 10), periodObj.periodLength)).format('MMM D LT');
                        return [
                            '<div class="tooltip-series">',
                            seriesToRender
                                .map(function (s) {
                                return "<div><span class=\"tooltip-label\">" + s.marker + "<strong>" + (s.seriesName && utils_1.truncationFormatter(s.seriesName, 12)) + "</strong></span>" + s.data[1].toFixed(2) + "%</div>";
                            })
                                .join(''),
                            '</div>',
                            "<div class=\"tooltip-date\">" + intervalStart + " &mdash; " + intervalEnd + "</div>",
                            "<div class=\"tooltip-arrow\"></div>",
                        ].join('');
                    },
                }} onClick={_this.handleClick}/>); }}
            </chartZoom_1.default>
          </transitionChart_1.default>
        </panels_1.PanelBody>
        <ChartFooter>
          <styles_1.InlineContainer>
            <styles_1.SectionHeading>
              {locale_1.tct('Total [display]', {
                display: activeDisplay === utils_3.DisplayOption.USERS ? 'Users' : 'Sessions',
            })}
            </styles_1.SectionHeading>
            <styles_1.SectionValue>
              <count_1.default value={totalCount || 0}/>
            </styles_1.SectionValue>
          </styles_1.InlineContainer>
        </ChartFooter>
      </panels_1.Panel>);
    };
    return ReleaseAdoptionChart;
}(asyncComponent_1.default));
exports.default = withApi_1.default(ReleaseAdoptionChart);
var ChartHeader = styled_1.default(styles_1.HeaderTitleLegend)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(1));
var ChartTitle = styled_1.default('header')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n"], ["\n  display: flex;\n  flex-direction: row;\n"])));
var ChartFooter = styled_1.default(panels_1.PanelFooter)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", " 20px;\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", " 20px;\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=releaseAdoptionChart.jsx.map