Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var indicator_1 = require("app/actionCreators/indicator");
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var locale_1 = require("app/locale");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var utils_1 = require("app/views/releases/detail/overview/chart/utils");
var utils_2 = require("app/views/releases/utils");
var utils_3 = require("./utils");
function StatsRequest(_a) {
    var api = _a.api, organization = _a.organization, projectSlug = _a.projectSlug, groupings = _a.groupings, environments = _a.environments, datetime = _a.datetime, location = _a.location, children = _a.children, searchQuery = _a.searchQuery;
    var _b = tslib_1.__read(react_1.useState(false), 2), isLoading = _b[0], setIsLoading = _b[1];
    var _c = tslib_1.__read(react_1.useState(false), 2), errored = _c[0], setErrored = _c[1];
    var _d = tslib_1.__read(react_1.useState([]), 2), series = _d[0], setSeries = _d[1];
    var filteredGroupings = groupings.filter(function (_a) {
        var aggregation = _a.aggregation, metricMeta = _a.metricMeta;
        return !!(metricMeta === null || metricMeta === void 0 ? void 0 : metricMeta.name) && !!aggregation;
    });
    react_1.useEffect(function () {
        fetchData();
    }, [projectSlug, environments, datetime, groupings, searchQuery]);
    function fetchData() {
        if (!filteredGroupings.length) {
            return;
        }
        setErrored(false);
        setIsLoading(true);
        var requestExtraParams = getParams_1.getParams(pick_1.default(location.query, Object.values(globalSelectionHeader_1.URL_PARAM).filter(function (param) { return param !== globalSelectionHeader_1.URL_PARAM.PROJECT; })));
        var promises = filteredGroupings.map(function (_a) {
            var metricMeta = _a.metricMeta, aggregation = _a.aggregation, groupBy = _a.groupBy;
            var query = tslib_1.__assign({ field: aggregation + "(" + metricMeta.name + ")", interval: utils_1.getInterval(datetime) }, requestExtraParams);
            if (searchQuery) {
                var tagsWithDoubleQuotes = searchQuery
                    .split(' ')
                    .filter(function (tag) { return !!tag; })
                    .map(function (tag) {
                    var _a = tslib_1.__read(tag.split(':'), 2), key = _a[0], value = _a[1];
                    if (key && value) {
                        return key + ":\"" + value + "\"";
                    }
                    return '';
                })
                    .filter(function (tag) { return !!tag; });
                if (!!tagsWithDoubleQuotes.length) {
                    query.query = new tokenizeSearch_1.QueryResults(tagsWithDoubleQuotes).formatString();
                }
            }
            var metricDataEndpoint = "/projects/" + organization.slug + "/" + projectSlug + "/metrics/data/";
            if (!!(groupBy === null || groupBy === void 0 ? void 0 : groupBy.length)) {
                var groupByParameter = tslib_1.__spreadArray([], tslib_1.__read(groupBy)).join('&groupBy=');
                return api.requestPromise(metricDataEndpoint + "?groupBy=" + groupByParameter, {
                    query: query,
                });
            }
            return api.requestPromise(metricDataEndpoint, {
                query: query,
            });
        });
        Promise.all(promises)
            .then(function (results) {
            getChartData(results);
        })
            .catch(function (error) {
            var _a, _b;
            indicator_1.addErrorMessage((_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : locale_1.t('Error loading chart data'));
            setErrored(true);
        });
    }
    function getChartData(sessionReponses) {
        if (!sessionReponses.length) {
            setIsLoading(false);
            return;
        }
        var seriesData = sessionReponses.map(function (sessionResponse, index) {
            var _a = filteredGroupings[index], aggregation = _a.aggregation, legend = _a.legend, metricMeta = _a.metricMeta;
            var field = aggregation + "(" + metricMeta.name + ")";
            var breakDownChartData = utils_3.getBreakdownChartData({
                response: sessionResponse,
                sessionResponseIndex: index + 1,
                legend: legend,
            });
            var chartData = utils_3.fillChartDataFromMetricsResponse({
                response: sessionResponse,
                field: field,
                chartData: breakDownChartData,
                valueFormatter: metricMeta.name === 'session.duration'
                    ? function (duration) { return utils_2.roundDuration(duration ? duration / 1000 : 0); }
                    : undefined,
            });
            return tslib_1.__spreadArray([], tslib_1.__read(Object.values(chartData)));
        });
        var newSeries = seriesData.reduce(function (mergedSeries, chartDataSeries) {
            return mergedSeries.concat(chartDataSeries);
        }, []);
        setSeries(newSeries);
        setIsLoading(false);
    }
    return children({ isLoading: isLoading, errored: errored, series: series });
}
exports.default = StatsRequest;
//# sourceMappingURL=statsRequest.jsx.map