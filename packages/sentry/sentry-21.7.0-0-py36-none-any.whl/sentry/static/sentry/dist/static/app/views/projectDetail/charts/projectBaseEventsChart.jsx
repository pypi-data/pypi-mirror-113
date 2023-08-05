Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var events_1 = require("app/actionCreators/events");
var eventsChart_1 = tslib_1.__importDefault(require("app/components/charts/eventsChart"));
var styles_1 = require("app/components/charts/styles");
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var locale_1 = require("app/locale");
var charts_1 = require("app/utils/discover/charts");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var ProjectBaseEventsChart = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectBaseEventsChart, _super);
    function ProjectBaseEventsChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectBaseEventsChart.prototype.componentDidMount = function () {
        this.fetchTotalCount();
    };
    ProjectBaseEventsChart.prototype.componentDidUpdate = function (prevProps) {
        if (!utils_1.isSelectionEqual(this.props.selection, prevProps.selection)) {
            this.fetchTotalCount();
        }
    };
    ProjectBaseEventsChart.prototype.fetchTotalCount = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, organization, selection, onTotalValuesChange, query, projects, environments, datetime, totals, err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection, onTotalValuesChange = _a.onTotalValuesChange, query = _a.query;
                        projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, events_1.fetchTotalCount(api, organization.slug, tslib_1.__assign({ field: [], query: query, environment: environments, project: projects.map(function (proj) { return String(proj); }) }, getParams_1.getParams(datetime)))];
                    case 2:
                        totals = _b.sent();
                        onTotalValuesChange(totals);
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        onTotalValuesChange(null);
                        Sentry.captureException(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    ProjectBaseEventsChart.prototype.render = function () {
        var _a = this.props, router = _a.router, organization = _a.organization, selection = _a.selection, api = _a.api, yAxis = _a.yAxis, query = _a.query, field = _a.field, title = _a.title, theme = _a.theme, help = _a.help, eventsChartProps = tslib_1.__rest(_a, ["router", "organization", "selection", "api", "yAxis", "query", "field", "title", "theme", "help"]);
        var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
        var start = datetime.start, end = datetime.end, period = datetime.period, utc = datetime.utc;
        return getDynamicText_1.default({
            value: (<eventsChart_1.default {...eventsChartProps} router={router} organization={organization} showLegend yAxis={yAxis} query={query} api={api} projects={projects} environments={environments} start={start} end={end} period={period} utc={utc} field={field} currentSeriesName={locale_1.t('This Period')} previousSeriesName={locale_1.t('Previous Period')} disableableSeries={[locale_1.t('This Period'), locale_1.t('Previous Period')]} chartHeader={<styles_1.HeaderTitleLegend>
              {title}
              {help && <questionTooltip_1.default size="sm" position="top" title={help}/>}
            </styles_1.HeaderTitleLegend>} legendOptions={{ right: 10, top: 0 }} chartOptions={{
                    grid: { left: '10px', right: '10px', top: '40px', bottom: '0px' },
                    yAxis: {
                        axisLabel: {
                            color: theme.gray200,
                            formatter: function (value) { return charts_1.axisLabelFormatter(value, yAxis); },
                        },
                        scale: true,
                    },
                }}/>),
            fixed: title + " Chart",
        });
    };
    return ProjectBaseEventsChart;
}(react_1.Component));
exports.default = withGlobalSelection_1.default(react_2.withTheme(ProjectBaseEventsChart));
//# sourceMappingURL=projectBaseEventsChart.jsx.map