Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var miniBarChart_1 = tslib_1.__importDefault(require("app/components/charts/miniBarChart"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var locale_1 = require("app/locale");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var getInitialState = function () {
    var until = Math.floor(new Date().getTime() / 1000);
    return {
        since: until - 3600 * 24 * 30,
        until: until,
        loading: true,
        error: false,
        series: [],
        emptyStats: false,
    };
};
var KeyStats = /** @class */ (function (_super) {
    tslib_1.__extends(KeyStats, _super);
    function KeyStats() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = getInitialState();
        _this.fetchData = function () {
            var _a = _this.props.params, keyId = _a.keyId, orgId = _a.orgId, projectId = _a.projectId;
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/keys/" + keyId + "/stats/", {
                query: {
                    since: _this.state.since,
                    until: _this.state.until,
                    resolution: '1d',
                },
                success: function (data) {
                    var emptyStats = true;
                    var dropped = [];
                    var accepted = [];
                    data.forEach(function (p) {
                        if (p.total) {
                            emptyStats = false;
                        }
                        dropped.push({ name: p.ts * 1000, value: p.dropped });
                        accepted.push({ name: p.ts * 1000, value: p.accepted });
                    });
                    var series = [
                        {
                            seriesName: locale_1.t('Accepted'),
                            data: accepted,
                        },
                        {
                            seriesName: locale_1.t('Rate Limited'),
                            data: dropped,
                        },
                    ];
                    _this.setState({
                        series: series,
                        emptyStats: emptyStats,
                        error: false,
                        loading: false,
                    });
                },
                error: function () {
                    _this.setState({ error: true, loading: false });
                },
            });
        };
        return _this;
    }
    KeyStats.prototype.componentDidMount = function () {
        this.fetchData();
    };
    KeyStats.prototype.render = function () {
        if (this.state.error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Key usage in the last 30 days (by day)')}</panels_1.PanelHeader>
        <panels_1.PanelBody withPadding>
          {this.state.loading ? (<placeholder_1.default height="150px"/>) : !this.state.emptyStats ? (<miniBarChart_1.default isGroupedByDate series={this.state.series} height={150} colors={[theme_1.default.gray200, theme_1.default.red300]} stacked labelYAxisExtents/>) : (<emptyMessage_1.default title={locale_1.t('Nothing recorded in the last 30 days.')} description={locale_1.t('Total events captured using these credentials.')}/>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    return KeyStats;
}(react_1.Component));
exports.default = KeyStats;
//# sourceMappingURL=keyStats.jsx.map