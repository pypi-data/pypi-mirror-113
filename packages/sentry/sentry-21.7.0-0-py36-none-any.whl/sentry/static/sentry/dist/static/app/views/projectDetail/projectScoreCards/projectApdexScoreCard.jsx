Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var round_1 = tslib_1.__importDefault(require("lodash/round"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var utils_1 = require("app/components/organizations/timeRangeSelector/utils");
var scoreCard_1 = tslib_1.__importDefault(require("app/components/scoreCard"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var utils_2 = require("app/utils");
var fields_1 = require("app/utils/discover/fields");
var getPeriod_1 = require("app/utils/getPeriod");
var data_1 = require("app/views/performance/data");
var missingPerformanceButtons_1 = tslib_1.__importDefault(require("../missingFeatureButtons/missingPerformanceButtons"));
var utils_3 = require("../utils");
var ProjectApdexScoreCard = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectApdexScoreCard, _super);
    function ProjectApdexScoreCard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldRenderBadRequests = true;
        return _this;
    }
    ProjectApdexScoreCard.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { currentApdex: null, previousApdex: null });
    };
    ProjectApdexScoreCard.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized, hasTransactions = _a.hasTransactions, query = _a.query;
        if (!this.hasFeature() || !isProjectStabilized || !hasTransactions) {
            return [];
        }
        var apdexField = organization.features.includes('project-transaction-threshold')
            ? 'apdex()'
            : "apdex(" + organization.apdexThreshold + ")";
        var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
        var period = datetime.period;
        var commonQuery = {
            environment: environments,
            project: projects.map(function (proj) { return String(proj); }),
            field: [apdexField],
            query: ['event.type:transaction count():>0', query].join(' ').trim(),
        };
        var endpoints = [
            [
                'currentApdex',
                "/organizations/" + organization.slug + "/eventsv2/",
                { query: tslib_1.__assign(tslib_1.__assign({}, commonQuery), getParams_1.getParams(datetime)) },
            ],
        ];
        if (utils_3.shouldFetchPreviousPeriod(datetime)) {
            var previousStart = utils_1.parseStatsPeriod(getPeriod_1.getPeriod({ period: period, start: undefined, end: undefined }, { shouldDoublePeriod: true })
                .statsPeriod).start;
            var previousEnd = utils_1.parseStatsPeriod(getPeriod_1.getPeriod({ period: period, start: undefined, end: undefined }, { shouldDoublePeriod: false })
                .statsPeriod).start;
            endpoints.push([
                'previousApdex',
                "/organizations/" + organization.slug + "/eventsv2/",
                { query: tslib_1.__assign(tslib_1.__assign({}, commonQuery), { start: previousStart, end: previousEnd }) },
            ]);
        }
        return endpoints;
    };
    ProjectApdexScoreCard.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized, hasTransactions = _a.hasTransactions, query = _a.query;
        if (prevProps.selection !== selection ||
            prevProps.hasTransactions !== hasTransactions ||
            prevProps.isProjectStabilized !== isProjectStabilized ||
            prevProps.query !== query) {
            this.remountComponent();
        }
    };
    ProjectApdexScoreCard.prototype.hasFeature = function () {
        return this.props.organization.features.includes('performance-view');
    };
    Object.defineProperty(ProjectApdexScoreCard.prototype, "cardTitle", {
        get: function () {
            return locale_1.t('Apdex');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectApdexScoreCard.prototype, "cardHelp", {
        get: function () {
            var organization = this.props.organization;
            var performanceTerm = organization.features.includes('project-transaction-threshold')
                ? data_1.PERFORMANCE_TERM.APDEX_NEW
                : data_1.PERFORMANCE_TERM.APDEX;
            var baseHelp = data_1.getTermHelp(this.props.organization, performanceTerm);
            if (this.trend) {
                return baseHelp + locale_1.t(' This shows how it has changed since the last period.');
            }
            return baseHelp;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectApdexScoreCard.prototype, "currentApdex", {
        get: function () {
            var _a;
            var organization = this.props.organization;
            var currentApdex = this.state.currentApdex;
            var apdexField = organization.features.includes('project-transaction-threshold')
                ? 'apdex()'
                : "apdex(" + organization.apdexThreshold + ")";
            var apdex = (_a = currentApdex === null || currentApdex === void 0 ? void 0 : currentApdex.data[0]) === null || _a === void 0 ? void 0 : _a[fields_1.getAggregateAlias(apdexField)];
            return typeof apdex === 'undefined' ? undefined : Number(apdex);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectApdexScoreCard.prototype, "previousApdex", {
        get: function () {
            var _a;
            var organization = this.props.organization;
            var previousApdex = this.state.previousApdex;
            var apdexField = organization.features.includes('project-transaction-threshold')
                ? 'apdex()'
                : "apdex(" + organization.apdexThreshold + ")";
            var apdex = (_a = previousApdex === null || previousApdex === void 0 ? void 0 : previousApdex.data[0]) === null || _a === void 0 ? void 0 : _a[fields_1.getAggregateAlias(apdexField)];
            return typeof apdex === 'undefined' ? undefined : Number(apdex);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectApdexScoreCard.prototype, "trend", {
        get: function () {
            if (this.currentApdex && this.previousApdex) {
                return round_1.default(this.currentApdex - this.previousApdex, 3);
            }
            return null;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectApdexScoreCard.prototype, "trendStatus", {
        get: function () {
            if (!this.trend) {
                return undefined;
            }
            return this.trend > 0 ? 'good' : 'bad';
        },
        enumerable: false,
        configurable: true
    });
    ProjectApdexScoreCard.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectApdexScoreCard.prototype.renderMissingFeatureCard = function () {
        var organization = this.props.organization;
        return (<scoreCard_1.default title={this.cardTitle} help={this.cardHelp} score={<missingPerformanceButtons_1.default organization={organization}/>}/>);
    };
    ProjectApdexScoreCard.prototype.renderScore = function () {
        return utils_2.defined(this.currentApdex) ? <count_1.default value={this.currentApdex}/> : '\u2014';
    };
    ProjectApdexScoreCard.prototype.renderTrend = function () {
        // we want to show trend only after currentApdex has loaded to prevent jumping
        return utils_2.defined(this.currentApdex) && utils_2.defined(this.trend) ? (<React.Fragment>
        {this.trend >= 0 ? (<icons_1.IconArrow direction="up" size="xs"/>) : (<icons_1.IconArrow direction="down" size="xs"/>)}
        <count_1.default value={Math.abs(this.trend)}/>
      </React.Fragment>) : null;
    };
    ProjectApdexScoreCard.prototype.renderBody = function () {
        var hasTransactions = this.props.hasTransactions;
        if (!this.hasFeature() || hasTransactions === false) {
            return this.renderMissingFeatureCard();
        }
        return (<scoreCard_1.default title={this.cardTitle} help={this.cardHelp} score={this.renderScore()} trend={this.renderTrend()} trendStatus={this.trendStatus}/>);
    };
    return ProjectApdexScoreCard;
}(asyncComponent_1.default));
exports.default = ProjectApdexScoreCard;
//# sourceMappingURL=projectApdexScoreCard.jsx.map