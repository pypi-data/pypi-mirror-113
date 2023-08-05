Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var round_1 = tslib_1.__importDefault(require("lodash/round"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var utils_1 = require("app/components/charts/utils");
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var scoreCard_1 = tslib_1.__importDefault(require("app/components/scoreCard"));
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var utils_2 = require("app/utils");
var formatters_1 = require("app/utils/formatters");
var getPeriod_1 = require("app/utils/getPeriod");
var utils_3 = require("app/views/releases/utils");
var sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
var missingReleasesButtons_1 = tslib_1.__importDefault(require("../missingFeatureButtons/missingReleasesButtons"));
var utils_4 = require("../utils");
var ProjectStabilityScoreCard = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectStabilityScoreCard, _super);
    function ProjectStabilityScoreCard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldRenderBadRequests = true;
        return _this;
    }
    ProjectStabilityScoreCard.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { currentSessions: null, previousSessions: null });
    };
    ProjectStabilityScoreCard.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized, hasSessions = _a.hasSessions, query = _a.query;
        if (!isProjectStabilized || !hasSessions) {
            return [];
        }
        var projects = selection.projects, environment = selection.environments, datetime = selection.datetime;
        var period = datetime.period;
        var commonQuery = {
            environment: environment,
            project: projects[0],
            field: 'sum(session)',
            groupBy: 'session.status',
            interval: utils_1.getDiffInMinutes(datetime) > 24 * 60 ? '1d' : '1h',
            query: query,
        };
        // Unfortunately we can't do something like statsPeriod=28d&interval=14d to get scores for this and previous interval with the single request
        // https://github.com/getsentry/sentry/pull/22770#issuecomment-758595553
        var endpoints = [
            [
                'currentSessions',
                "/organizations/" + organization.slug + "/sessions/",
                {
                    query: tslib_1.__assign(tslib_1.__assign({}, commonQuery), getParams_1.getParams(datetime)),
                },
            ],
        ];
        if (utils_4.shouldFetchPreviousPeriod(datetime)) {
            var doubledPeriod = getPeriod_1.getPeriod({ period: period, start: undefined, end: undefined }, { shouldDoublePeriod: true }).statsPeriod;
            endpoints.push([
                'previousSessions',
                "/organizations/" + organization.slug + "/sessions/",
                {
                    query: tslib_1.__assign(tslib_1.__assign({}, commonQuery), { statsPeriodStart: doubledPeriod, statsPeriodEnd: period !== null && period !== void 0 ? period : constants_1.DEFAULT_STATS_PERIOD }),
                },
            ]);
        }
        return endpoints;
    };
    Object.defineProperty(ProjectStabilityScoreCard.prototype, "cardTitle", {
        get: function () {
            return locale_1.t('Crash Free Sessions');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectStabilityScoreCard.prototype, "cardHelp", {
        get: function () {
            return this.trend
                ? locale_1.t('The percentage of crash free sessions and how it has changed since the last period.')
                : sessionTerm_1.getSessionTermDescription(sessionTerm_1.SessionTerm.STABILITY, null);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectStabilityScoreCard.prototype, "score", {
        get: function () {
            var currentSessions = this.state.currentSessions;
            return this.calculateCrashFree(currentSessions);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectStabilityScoreCard.prototype, "trend", {
        get: function () {
            var previousSessions = this.state.previousSessions;
            var previousScore = this.calculateCrashFree(previousSessions);
            if (!utils_2.defined(this.score) || !utils_2.defined(previousScore)) {
                return undefined;
            }
            return round_1.default(this.score - previousScore, 3);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectStabilityScoreCard.prototype, "trendStatus", {
        get: function () {
            if (!this.trend) {
                return undefined;
            }
            return this.trend > 0 ? 'good' : 'bad';
        },
        enumerable: false,
        configurable: true
    });
    ProjectStabilityScoreCard.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized, hasSessions = _a.hasSessions, query = _a.query;
        if (prevProps.selection !== selection ||
            prevProps.hasSessions !== hasSessions ||
            prevProps.isProjectStabilized !== isProjectStabilized ||
            prevProps.query !== query) {
            this.remountComponent();
        }
    };
    ProjectStabilityScoreCard.prototype.calculateCrashFree = function (data) {
        var _a;
        if (!data) {
            return undefined;
        }
        var totalSessions = data.groups.reduce(function (acc, group) { return acc + group.totals['sum(session)']; }, 0);
        var crashedSessions = (_a = data.groups.find(function (group) { return group.by['session.status'] === 'crashed'; })) === null || _a === void 0 ? void 0 : _a.totals['sum(session)'];
        if (totalSessions === 0 || !utils_2.defined(totalSessions) || !utils_2.defined(crashedSessions)) {
            return undefined;
        }
        var crashedSessionsPercent = utils_2.percent(crashedSessions, totalSessions);
        return utils_3.getCrashFreePercent(100 - crashedSessionsPercent);
    };
    ProjectStabilityScoreCard.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectStabilityScoreCard.prototype.renderMissingFeatureCard = function () {
        var organization = this.props.organization;
        return (<scoreCard_1.default title={this.cardTitle} help={this.cardHelp} score={<missingReleasesButtons_1.default organization={organization} health/>}/>);
    };
    ProjectStabilityScoreCard.prototype.renderScore = function () {
        var loading = this.state.loading;
        if (loading || !utils_2.defined(this.score)) {
            return '\u2014';
        }
        return utils_3.displayCrashFreePercent(this.score);
    };
    ProjectStabilityScoreCard.prototype.renderTrend = function () {
        var loading = this.state.loading;
        if (loading || !utils_2.defined(this.score) || !utils_2.defined(this.trend)) {
            return null;
        }
        return (<div>
        {this.trend >= 0 ? (<icons_1.IconArrow direction="up" size="xs"/>) : (<icons_1.IconArrow direction="down" size="xs"/>)}
        {formatters_1.formatAbbreviatedNumber(Math.abs(this.trend)) + "%"}
      </div>);
    };
    ProjectStabilityScoreCard.prototype.renderBody = function () {
        var hasSessions = this.props.hasSessions;
        if (hasSessions === false) {
            return this.renderMissingFeatureCard();
        }
        return (<scoreCard_1.default title={this.cardTitle} help={this.cardHelp} score={this.renderScore()} trend={this.renderTrend()} trendStatus={this.trendStatus}/>);
    };
    return ProjectStabilityScoreCard;
}(asyncComponent_1.default));
exports.default = ProjectStabilityScoreCard;
//# sourceMappingURL=projectStabilityScoreCard.jsx.map