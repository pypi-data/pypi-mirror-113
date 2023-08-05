Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectFiltersChart = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var miniBarChart_1 = tslib_1.__importDefault(require("app/components/charts/miniBarChart"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var locale_1 = require("app/locale");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var STAT_OPS = {
    'browser-extensions': { title: locale_1.t('Browser Extension'), color: theme_1.default.gray200 },
    cors: { title: 'CORS', color: theme_1.default.orange400 },
    'error-message': { title: locale_1.t('Error Message'), color: theme_1.default.purple300 },
    'discarded-hash': { title: locale_1.t('Discarded Issue'), color: theme_1.default.gray200 },
    'invalid-csp': { title: locale_1.t('Invalid CSP'), color: theme_1.default.blue300 },
    'ip-address': { title: locale_1.t('IP Address'), color: theme_1.default.red200 },
    'legacy-browsers': { title: locale_1.t('Legacy Browser'), color: theme_1.default.gray200 },
    localhost: { title: locale_1.t('Localhost'), color: theme_1.default.blue300 },
    'release-version': { title: locale_1.t('Release'), color: theme_1.default.purple200 },
    'web-crawlers': { title: locale_1.t('Web Crawler'), color: theme_1.default.red300 },
};
var ProjectFiltersChart = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectFiltersChart, _super);
    function ProjectFiltersChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            statsError: false,
            formattedData: [],
            blankStats: true,
        };
        _this.fetchData = function () {
            _this.getFilterStats();
        };
        return _this;
    }
    ProjectFiltersChart.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ProjectFiltersChart.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.project !== this.props.project) {
            this.fetchData();
        }
    };
    ProjectFiltersChart.prototype.formatData = function (rawData) {
        var _this = this;
        var seriesWithData = new Set();
        var transformed = Object.keys(STAT_OPS).map(function (stat) { return ({
            data: rawData[stat].map(function (_a) {
                var _b = tslib_1.__read(_a, 2), timestamp = _b[0], value = _b[1];
                if (value > 0) {
                    seriesWithData.add(STAT_OPS[stat].title);
                    _this.setState({ blankStats: false });
                }
                return { name: timestamp * 1000, value: value };
            }),
            seriesName: STAT_OPS[stat].title,
            color: STAT_OPS[stat].color,
        }); });
        return transformed.filter(function (series) { return seriesWithData.has(series.seriesName); });
    };
    ProjectFiltersChart.prototype.getFilterStats = function () {
        var _this = this;
        var statOptions = Object.keys(STAT_OPS);
        var project = this.props.project;
        var orgId = this.props.params.orgId;
        var until = Math.floor(new Date().getTime() / 1000);
        var since = until - 3600 * 24 * 30;
        var statEndpoint = "/projects/" + orgId + "/" + project.slug + "/stats/";
        var query = {
            since: since,
            until: until,
            resolution: '1d',
        };
        var requests = statOptions.map(function (stat) {
            return _this.props.api.requestPromise(statEndpoint, {
                query: Object.assign({ stat: stat }, query),
            });
        });
        Promise.all(requests)
            .then(function (results) {
            var rawStatsData = {};
            for (var i = 0; i < statOptions.length; i++) {
                rawStatsData[statOptions[i]] = results[i];
            }
            _this.setState({
                formattedData: _this.formatData(rawStatsData),
                error: false,
                loading: false,
            });
        })
            .catch(function () {
            _this.setState({ error: true, loading: false });
        });
    };
    ProjectFiltersChart.prototype.render = function () {
        var _a = this.state, loading = _a.loading, error = _a.error, formattedData = _a.formattedData;
        var isLoading = loading || !formattedData;
        var hasError = !isLoading && error;
        var hasLoaded = !isLoading && !error;
        var colors = formattedData
            ? formattedData.map(function (series) { return series.color || theme_1.default.gray200; })
            : undefined;
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Errors filtered in the last 30 days (by day)')}</panels_1.PanelHeader>

        <panels_1.PanelBody withPadding>
          {isLoading && <placeholder_1.default height="100px"/>}
          {hasError && <loadingError_1.default onRetry={this.fetchData}/>}
          {hasLoaded && !this.state.blankStats && (<miniBarChart_1.default series={formattedData} colors={colors} height={100} isGroupedByDate stacked labelYAxisExtents/>)}
          {hasLoaded && this.state.blankStats && (<emptyMessage_1.default title={locale_1.t('Nothing filtered in the last 30 days.')} description={locale_1.t('Issues filtered as a result of your settings below will be shown here.')}/>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    return ProjectFiltersChart;
}(react_1.Component));
exports.ProjectFiltersChart = ProjectFiltersChart;
exports.default = withApi_1.default(ProjectFiltersChart);
//# sourceMappingURL=projectFiltersChart.jsx.map