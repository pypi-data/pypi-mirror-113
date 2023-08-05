Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var baseChart_1 = tslib_1.__importDefault(require("app/components/charts/baseChart"));
var styles_1 = require("app/components/charts/styles");
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var ALLOWED_TIME_PERIODS = ['1h', '24h', '7d', '14d', '30d'];
var ProjectErrorsBasicChart = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectErrorsBasicChart, _super);
    function ProjectErrorsBasicChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectErrorsBasicChart.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { projects: null });
    };
    ProjectErrorsBasicChart.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId;
        if (!projectId) {
            return [];
        }
        return [
            [
                'projects',
                "/organizations/" + organization.slug + "/projects/",
                {
                    query: {
                        statsPeriod: this.getStatsPeriod(),
                        query: "id:" + projectId,
                    },
                },
            ],
        ];
    };
    ProjectErrorsBasicChart.prototype.componentDidMount = function () {
        var location = this.props.location;
        if (!ALLOWED_TIME_PERIODS.includes(location.query.statsPeriod)) {
            react_router_1.browserHistory.replace({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { statsPeriod: this.getStatsPeriod(), start: undefined, end: undefined }),
            });
        }
    };
    ProjectErrorsBasicChart.prototype.onLoadAllEndpointsSuccess = function () {
        var _a, _b, _c, _d;
        this.props.onTotalValuesChange((_d = (_c = (_b = (_a = this.state.projects) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b.stats) === null || _c === void 0 ? void 0 : _c.reduce(function (acc, _a) {
            var _b = tslib_1.__read(_a, 2), value = _b[1];
            return acc + value;
        }, 0)) !== null && _d !== void 0 ? _d : null);
    };
    ProjectErrorsBasicChart.prototype.getStatsPeriod = function () {
        var location = this.props.location;
        var statsPeriod = location.query.statsPeriod;
        if (ALLOWED_TIME_PERIODS.includes(statsPeriod)) {
            return statsPeriod;
        }
        return constants_1.DEFAULT_STATS_PERIOD;
    };
    ProjectErrorsBasicChart.prototype.getSeries = function () {
        var _a, _b, _c;
        var projects = this.state.projects;
        return [
            {
                cursor: 'normal',
                name: locale_1.t('Errors'),
                type: 'bar',
                data: (_c = (_b = (_a = projects === null || projects === void 0 ? void 0 : projects[0]) === null || _a === void 0 ? void 0 : _a.stats) === null || _b === void 0 ? void 0 : _b.map(function (_a) {
                    var _b = tslib_1.__read(_a, 2), timestamp = _b[0], value = _b[1];
                    return [timestamp * 1000, value];
                })) !== null && _c !== void 0 ? _c : [],
            },
        ];
    };
    ProjectErrorsBasicChart.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectErrorsBasicChart.prototype.renderBody = function () {
        var _a = this.state, loading = _a.loading, reloading = _a.reloading;
        return getDynamicText_1.default({
            value: (<transitionChart_1.default loading={loading} reloading={reloading}>
          <transparentLoadingMask_1.default visible={reloading}/>

          <styles_1.HeaderTitleLegend>{locale_1.t('Daily Errors')}</styles_1.HeaderTitleLegend>

          <baseChart_1.default series={this.getSeries()} isGroupedByDate showTimeInTooltip colors={function (theme) { return [theme.purple300, theme.purple200]; }} grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }}/>
        </transitionChart_1.default>),
            fixed: locale_1.t('Number of Errors Chart'),
        });
    };
    return ProjectErrorsBasicChart;
}(asyncComponent_1.default));
exports.default = ProjectErrorsBasicChart;
//# sourceMappingURL=projectErrorsBasicChart.jsx.map