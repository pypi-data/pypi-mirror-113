Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var projects_1 = require("app/actionCreators/projects");
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var utils_1 = require("app/components/organizations/timeRangeSelector/utils");
var scoreCard_1 = tslib_1.__importDefault(require("app/components/scoreCard"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var utils_2 = require("app/utils");
var getPeriod_1 = require("app/utils/getPeriod");
var missingReleasesButtons_1 = tslib_1.__importDefault(require("../missingFeatureButtons/missingReleasesButtons"));
var utils_3 = require("../utils");
var API_LIMIT = 1000;
var ProjectVelocityScoreCard = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectVelocityScoreCard, _super);
    function ProjectVelocityScoreCard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldRenderBadRequests = true;
        return _this;
    }
    ProjectVelocityScoreCard.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { currentReleases: null, previousReleases: null, noReleaseEver: false });
    };
    ProjectVelocityScoreCard.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized, query = _a.query;
        if (!isProjectStabilized) {
            return [];
        }
        var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
        var period = datetime.period;
        var commonQuery = {
            environment: environments,
            project: projects[0],
            query: query,
        };
        var endpoints = [
            [
                'currentReleases',
                "/organizations/" + organization.slug + "/releases/stats/",
                {
                    includeAllArgs: true,
                    method: 'GET',
                    query: tslib_1.__assign(tslib_1.__assign({}, commonQuery), getParams_1.getParams(datetime)),
                },
            ],
        ];
        if (utils_3.shouldFetchPreviousPeriod(datetime)) {
            var previousStart = utils_1.parseStatsPeriod(getPeriod_1.getPeriod({ period: period, start: undefined, end: undefined }, { shouldDoublePeriod: true })
                .statsPeriod).start;
            var previousEnd = utils_1.parseStatsPeriod(getPeriod_1.getPeriod({ period: period, start: undefined, end: undefined }, { shouldDoublePeriod: false })
                .statsPeriod).start;
            endpoints.push([
                'previousReleases',
                "/organizations/" + organization.slug + "/releases/stats/",
                {
                    query: tslib_1.__assign(tslib_1.__assign({}, commonQuery), { start: previousStart, end: previousEnd }),
                },
            ]);
        }
        return endpoints;
    };
    /**
     * If our releases are empty, determine if we had a release in the last 90 days (empty message differs then)
     */
    ProjectVelocityScoreCard.prototype.onLoadAllEndpointsSuccess = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, currentReleases, previousReleases, _b, organization, selection, isProjectStabilized, hasOlderReleases;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.state, currentReleases = _a.currentReleases, previousReleases = _a.previousReleases;
                        _b = this.props, organization = _b.organization, selection = _b.selection, isProjectStabilized = _b.isProjectStabilized;
                        if (!isProjectStabilized) {
                            return [2 /*return*/];
                        }
                        if (tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read((currentReleases !== null && currentReleases !== void 0 ? currentReleases : []))), tslib_1.__read((previousReleases !== null && previousReleases !== void 0 ? previousReleases : []))).length !== 0) {
                            this.setState({ noReleaseEver: false });
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        return [4 /*yield*/, projects_1.fetchAnyReleaseExistence(this.api, organization.slug, selection.projects[0])];
                    case 1:
                        hasOlderReleases = _c.sent();
                        this.setState({ noReleaseEver: !hasOlderReleases, loading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    Object.defineProperty(ProjectVelocityScoreCard.prototype, "cardTitle", {
        get: function () {
            return locale_1.t('Number of Releases');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectVelocityScoreCard.prototype, "cardHelp", {
        get: function () {
            return this.trend
                ? locale_1.t('The number of releases for this project and how it has changed since the last period.')
                : locale_1.t('The number of releases for this project.');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectVelocityScoreCard.prototype, "trend", {
        get: function () {
            var _a = this.state, currentReleases = _a.currentReleases, previousReleases = _a.previousReleases;
            if (!utils_2.defined(currentReleases) || !utils_2.defined(previousReleases)) {
                return null;
            }
            return currentReleases.length - previousReleases.length;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectVelocityScoreCard.prototype, "trendStatus", {
        get: function () {
            if (!this.trend) {
                return undefined;
            }
            return this.trend > 0 ? 'good' : 'bad';
        },
        enumerable: false,
        configurable: true
    });
    ProjectVelocityScoreCard.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized;
        if (prevProps.selection !== selection ||
            prevProps.isProjectStabilized !== isProjectStabilized) {
            this.remountComponent();
        }
    };
    ProjectVelocityScoreCard.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectVelocityScoreCard.prototype.renderMissingFeatureCard = function () {
        var organization = this.props.organization;
        return (<scoreCard_1.default title={this.cardTitle} help={this.cardHelp} score={<missingReleasesButtons_1.default organization={organization}/>}/>);
    };
    ProjectVelocityScoreCard.prototype.renderScore = function () {
        var _a = this.state, currentReleases = _a.currentReleases, loading = _a.loading;
        if (loading || !utils_2.defined(currentReleases)) {
            return '\u2014';
        }
        return currentReleases.length === API_LIMIT
            ? API_LIMIT - 1 + "+"
            : currentReleases.length;
    };
    ProjectVelocityScoreCard.prototype.renderTrend = function () {
        var _a = this.state, loading = _a.loading, currentReleases = _a.currentReleases;
        if (loading || !utils_2.defined(this.trend) || (currentReleases === null || currentReleases === void 0 ? void 0 : currentReleases.length) === API_LIMIT) {
            return null;
        }
        return (<React.Fragment>
        {this.trend >= 0 ? (<icons_1.IconArrow direction="up" size="xs"/>) : (<icons_1.IconArrow direction="down" size="xs"/>)}
        {Math.abs(this.trend)}
      </React.Fragment>);
    };
    ProjectVelocityScoreCard.prototype.renderBody = function () {
        var noReleaseEver = this.state.noReleaseEver;
        if (noReleaseEver) {
            return this.renderMissingFeatureCard();
        }
        return (<scoreCard_1.default title={this.cardTitle} help={this.cardHelp} score={this.renderScore()} trend={this.renderTrend()} trendStatus={this.trendStatus}/>);
    };
    return ProjectVelocityScoreCard;
}(asyncComponent_1.default));
exports.default = ProjectVelocityScoreCard;
//# sourceMappingURL=projectVelocityScoreCard.jsx.map