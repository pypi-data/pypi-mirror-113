Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var types_1 = require("app/types");
var sessions_1 = require("app/utils/sessions");
var utils_1 = require("../../utils");
var utils_2 = require("../utils");
var styles_1 = require("./styles");
function ReleaseComparisonChart(_a) {
    var release = _a.release, project = _a.project, releaseSessions = _a.releaseSessions, allSessions = _a.allSessions, loading = _a.loading, reloading = _a.reloading, errored = _a.errored, theme = _a.theme, router = _a.router, location = _a.location;
    var hasUsers = !!sessions_1.getCount(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS);
    function getSeries() {
        if (!releaseSessions) {
            return [];
        }
        var sessionsMarkLines = utils_2.generateReleaseMarkLines(release, project.slug, theme, {
            hideLabel: true,
            axisIndex: 0,
        });
        var series = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(sessionsMarkLines)), [
            {
                seriesName: locale_1.t('Sessions Adopted'),
                connectNulls: true,
                yAxisIndex: 0,
                xAxisIndex: 0,
                data: sessions_1.getAdoptionSeries(releaseSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, releaseSessions.intervals, types_1.SessionField.SESSIONS),
            },
        ]);
        if (hasUsers) {
            var usersMarkLines = utils_2.generateReleaseMarkLines(release, project.slug, theme, {
                hideLabel: true,
                axisIndex: 1,
            });
            series.push.apply(series, tslib_1.__spreadArray([], tslib_1.__read(usersMarkLines)));
            series.push({
                seriesName: locale_1.t('Users Adopted'),
                connectNulls: true,
                yAxisIndex: 1,
                xAxisIndex: 1,
                data: sessions_1.getAdoptionSeries(releaseSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, releaseSessions.intervals, types_1.SessionField.USERS),
            });
        }
        return series;
    }
    var colors = theme.charts.getColorPalette(2);
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
        max: 100,
        axisLabel: {
            formatter: function (value) { return value + "%"; },
            color: theme.chartLabel,
        },
    };
    var chartOptions = {
        height: hasUsers ? 280 : 140,
        grid: [
            {
                top: '40px',
                left: '10px',
                right: '10px',
                height: '100px',
            },
            {
                top: '180px',
                left: '10px',
                right: '10px',
                height: '100px',
            },
        ],
        axisPointer: {
            // Link each x-axis together.
            link: [{ xAxisIndex: [0, 1] }],
        },
        xAxes: Array.from(new Array(2)).map(function (_i, index) { return ({
            gridIndex: index,
            type: 'time',
            show: false,
        }); }),
        yAxes: [
            tslib_1.__assign({ 
                // sessions adopted
                gridIndex: 0 }, axisLineConfig),
            tslib_1.__assign({ 
                // users adopted
                gridIndex: 1 }, axisLineConfig),
        ],
        // utc: utc === 'true', //TODO(release-comparison)
        isGroupedByDate: true,
        showTimeInTooltip: true,
        colors: [colors[0], colors[1]],
        tooltip: {
            trigger: 'axis',
            truncate: 80,
            valueFormatter: function (value, label) {
                return label && Object.values(utils_2.releaseMarkLinesLabels).includes(label) ? '' : value + "%";
            },
        },
    };
    var _b = utils_1.getReleaseParams({
        location: location,
        releaseBounds: utils_1.getReleaseBounds(release),
        defaultStatsPeriod: constants_1.DEFAULT_STATS_PERIOD,
        allowEmptyPeriod: true,
    }), period = _b.statsPeriod, start = _b.start, end = _b.end, utc = _b.utc;
    return (<RelativeBox>
      <ChartLabel top="0px">
        <ChartTitle>
          {locale_1.t('Sessions Adopted')}
          <questionTooltip_1.default position="top" title={locale_1.t('Adoption compares the sessions of a release with the total sessions for this project.')} size="sm"/>
        </ChartTitle>
      </ChartLabel>

      {hasUsers && (<ChartLabel top="140px">
          <ChartTitle>
            {locale_1.t('Users Adopted')}
            <questionTooltip_1.default position="top" title={locale_1.t('Adoption compares the users of a release with the total users for this project.')} size="sm"/>
          </ChartTitle>
        </ChartLabel>)}

      {errored ? (<errorPanel_1.default height="280px">
          <icons_1.IconWarning color="gray300" size="lg"/>
        </errorPanel_1.default>) : (<transitionChart_1.default loading={loading} reloading={reloading} height="280px">
          <transparentLoadingMask_1.default visible={reloading}/>
          <chartZoom_1.default router={router} period={period !== null && period !== void 0 ? period : undefined} utc={utc === 'true'} start={start} end={end} usePageDate xAxisIndex={[0, 1]}>
            {function (zoomRenderProps) { return (<lineChart_1.default {...chartOptions} {...zoomRenderProps} series={getSeries()}/>); }}
          </chartZoom_1.default>
        </transitionChart_1.default>)}
    </RelativeBox>);
}
var RelativeBox = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var ChartTitle = styled_1.default(styles_1.SectionHeading)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var ChartLabel = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  z-index: 1;\n  left: 0;\n  right: 0;\n"], ["\n  position: absolute;\n  top: ", ";\n  z-index: 1;\n  left: 0;\n  right: 0;\n"])), function (p) { return p.top; });
exports.default = react_1.withTheme(react_router_1.withRouter(ReleaseComparisonChart));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=releaseAdoption.jsx.map