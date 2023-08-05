Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var miniBarChart_1 = tslib_1.__importDefault(require("app/components/charts/miniBarChart"));
var locale_1 = require("app/locale");
var formatters_1 = require("app/utils/formatters");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var sidebarSection_1 = tslib_1.__importDefault(require("./sidebarSection"));
function GroupReleaseChart(props) {
    var className = props.className, group = props.group, lastSeen = props.lastSeen, firstSeen = props.firstSeen, statsPeriod = props.statsPeriod, release = props.release, releaseStats = props.releaseStats, environment = props.environment, environmentStats = props.environmentStats, title = props.title;
    var stats = group.stats[statsPeriod];
    if (!stats || !stats.length) {
        return null;
    }
    var series = [];
    // Add all events.
    series.push({
        seriesName: locale_1.t('Events'),
        data: stats.map(function (point) { return ({ name: point[0] * 1000, value: point[1] }); }),
    });
    // Get the timestamp of the first point.
    var firstTime = series[0].data[0].value;
    if (environment && environmentStats) {
        series.push({
            seriesName: locale_1.t('Events in %s', environment),
            data: environmentStats[statsPeriod].map(function (point) { return ({
                name: point[0] * 1000,
                value: point[1],
            }); }),
        });
    }
    if (release && releaseStats) {
        series.push({
            seriesName: locale_1.t('Events in release %s', formatters_1.formatVersion(release.version)),
            data: releaseStats[statsPeriod].map(function (point) { return ({
                name: point[0] * 1000,
                value: point[1],
            }); }),
        });
    }
    var markers = [];
    if (firstSeen) {
        var firstSeenX = new Date(firstSeen).getTime();
        if (firstSeenX >= firstTime) {
            markers.push({
                name: locale_1.t('First seen'),
                value: firstSeenX,
                color: theme_1.default.pink300,
            });
        }
    }
    if (lastSeen) {
        var lastSeenX = new Date(lastSeen).getTime();
        if (lastSeenX >= firstTime) {
            markers.push({
                name: locale_1.t('Last seen'),
                value: lastSeenX,
                color: theme_1.default.green300,
            });
        }
    }
    return (<sidebarSection_1.default secondary title={title} className={className}>
      <miniBarChart_1.default isGroupedByDate showTimeInTooltip height={42} series={series} markers={markers}/>
    </sidebarSection_1.default>);
}
exports.default = GroupReleaseChart;
//# sourceMappingURL=releaseChart.jsx.map