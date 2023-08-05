Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var indicator_1 = require("app/actionCreators/indicator");
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var sessions_1 = require("app/utils/sessions");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var utils_1 = require("../../utils");
var ReleaseDetailsRequest = /** @class */ (function (_super) {
    tslib_1.__extends(ReleaseDetailsRequest, _super);
    function ReleaseDetailsRequest() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            reloading: false,
            errored: false,
            thisRelease: null,
            allReleases: null,
        };
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, disable, promises, _b, thisRelease, allReleases, error_1;
            var _c, _d;
            return tslib_1.__generator(this, function (_e) {
                switch (_e.label) {
                    case 0:
                        _a = this.props, api = _a.api, disable = _a.disable;
                        if (disable) {
                            return [2 /*return*/];
                        }
                        api.clear();
                        this.setState(function (state) { return ({
                            reloading: state.thisRelease !== null && state.allReleases !== null,
                            errored: false,
                        }); });
                        promises = [this.fetchThisRelease(), this.fetchAllReleases()];
                        _e.label = 1;
                    case 1:
                        _e.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, Promise.all(promises)];
                    case 2:
                        _b = tslib_1.__read.apply(void 0, [_e.sent(), 2]), thisRelease = _b[0], allReleases = _b[1];
                        this.setState({
                            reloading: false,
                            thisRelease: sessions_1.filterSessionsInTimeWindow(thisRelease, this.baseQueryParams.start, this.baseQueryParams.end),
                            allReleases: sessions_1.filterSessionsInTimeWindow(allReleases, this.baseQueryParams.start, this.baseQueryParams.end),
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _e.sent();
                        indicator_1.addErrorMessage((_d = (_c = error_1.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) !== null && _d !== void 0 ? _d : locale_1.t('Error loading health data'));
                        this.setState({
                            reloading: false,
                            errored: true,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ReleaseDetailsRequest.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ReleaseDetailsRequest.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.version !== this.props.version ||
            !isEqual_1.default(prevProps.location, this.props.location)) {
            this.fetchData();
        }
    };
    Object.defineProperty(ReleaseDetailsRequest.prototype, "path", {
        get: function () {
            var organization = this.props.organization;
            return "/organizations/" + organization.slug + "/sessions/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ReleaseDetailsRequest.prototype, "baseQueryParams", {
        get: function () {
            var _a;
            var _b = this.props, location = _b.location, releaseBounds = _b.releaseBounds, organization = _b.organization;
            var releaseParams = utils_1.getReleaseParams({
                location: location,
                releaseBounds: releaseBounds,
                defaultStatsPeriod: constants_1.DEFAULT_STATS_PERIOD,
                allowEmptyPeriod: true,
            });
            return tslib_1.__assign({ field: ['count_unique(user)', 'sum(session)'], groupBy: ['session.status'], interval: sessions_1.getSessionsInterval({
                    start: releaseParams.start,
                    end: releaseParams.end,
                    period: (_a = releaseParams.statsPeriod) !== null && _a !== void 0 ? _a : undefined,
                }, { highFidelity: organization.features.includes('minute-resolution-sessions') }) }, releaseParams);
        },
        enumerable: false,
        configurable: true
    });
    ReleaseDetailsRequest.prototype.fetchThisRelease = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, version, response;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, version = _a.version;
                        return [4 /*yield*/, api.requestPromise(this.path, {
                                query: tslib_1.__assign(tslib_1.__assign({}, this.baseQueryParams), { query: "release:" + version }),
                            })];
                    case 1:
                        response = _b.sent();
                        return [2 /*return*/, response];
                }
            });
        });
    };
    ReleaseDetailsRequest.prototype.fetchAllReleases = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var api, response;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        api = this.props.api;
                        return [4 /*yield*/, api.requestPromise(this.path, {
                                query: this.baseQueryParams,
                            })];
                    case 1:
                        response = _a.sent();
                        return [2 /*return*/, response];
                }
            });
        });
    };
    ReleaseDetailsRequest.prototype.render = function () {
        var _a = this.state, reloading = _a.reloading, errored = _a.errored, thisRelease = _a.thisRelease, allReleases = _a.allReleases;
        var children = this.props.children;
        var loading = thisRelease === null && allReleases === null;
        return children({
            loading: loading,
            reloading: reloading,
            errored: errored,
            thisRelease: thisRelease,
            allReleases: allReleases,
        });
    };
    return ReleaseDetailsRequest;
}(React.Component));
exports.default = withApi_1.default(ReleaseDetailsRequest);
//# sourceMappingURL=releaseDetailsRequest.jsx.map