Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var miniBarChart_1 = tslib_1.__importDefault(require("app/components/charts/miniBarChart"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var MonitorStats = /** @class */ (function (_super) {
    tslib_1.__extends(MonitorStats, _super);
    function MonitorStats() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MonitorStats.prototype.getEndpoints = function () {
        var monitor = this.props.monitor;
        var until = Math.floor(new Date().getTime() / 1000);
        var since = until - 3600 * 24 * 30;
        return [
            [
                'stats',
                "/monitors/" + monitor.id + "/stats/",
                {
                    query: {
                        since: since,
                        until: until,
                        resolution: '1d',
                    },
                },
            ],
        ];
    };
    MonitorStats.prototype.renderBody = function () {
        var _a;
        var emptyStats = true;
        var success = {
            seriesName: locale_1.t('Successful'),
            data: [],
        };
        var failed = {
            seriesName: locale_1.t('Failed'),
            data: [],
        };
        (_a = this.state.stats) === null || _a === void 0 ? void 0 : _a.forEach(function (p) {
            if (p.ok || p.error) {
                emptyStats = false;
            }
            var timestamp = p.ts * 1000;
            success.data.push({ name: timestamp.toString(), value: p.ok });
            failed.data.push({ name: timestamp.toString(), value: p.error });
        });
        var colors = [theme_1.default.green300, theme_1.default.red300];
        return (<panels_1.Panel>
        <panels_1.PanelBody withPadding>
          {!emptyStats ? (<miniBarChart_1.default isGroupedByDate showTimeInTooltip labelYAxisExtents stacked colors={colors} height={150} series={[success, failed]}/>) : (<emptyMessage_1.default title={locale_1.t('Nothing recorded in the last 30 days.')} description={locale_1.t('All check-ins for this monitor.')}/>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    return MonitorStats;
}(asyncComponent_1.default));
exports.default = MonitorStats;
//# sourceMappingURL=monitorStats.jsx.map