Object.defineProperty(exports, "__esModule", { value: true });
exports.sessionDisplayToField = exports.reduceTimeSeriesGroups = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var indicator_1 = require("app/actionCreators/indicator");
var utils_1 = require("app/components/charts/utils");
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var locale_1 = require("app/locale");
var types_1 = require("app/types");
var utils_2 = require("app/utils");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var utils_3 = require("../list/utils");
var _1 = require(".");
function omitIgnoredProps(props) {
    return omit_1.default(props, [
        'api',
        'organization',
        'children',
        'selection.datetime.utc',
        'location',
    ]);
}
function getInterval(datetimeObj) {
    var diffInMinutes = utils_1.getDiffInMinutes(datetimeObj);
    if (diffInMinutes >= utils_1.TWO_WEEKS) {
        return '1d';
    }
    if (diffInMinutes >= utils_1.ONE_WEEK) {
        return '6h';
    }
    if (diffInMinutes > utils_1.TWENTY_FOUR_HOURS) {
        return '4h';
    }
    // TODO(sessions): sub-hour session resolution is still not possible
    return '1h';
}
function reduceTimeSeriesGroups(acc, group, field) {
    var _a;
    (_a = group.series[field]) === null || _a === void 0 ? void 0 : _a.forEach(function (value, index) { var _a; return (acc[index] = ((_a = acc[index]) !== null && _a !== void 0 ? _a : 0) + value); });
    return acc;
}
exports.reduceTimeSeriesGroups = reduceTimeSeriesGroups;
function sessionDisplayToField(display) {
    switch (display) {
        case utils_3.DisplayOption.USERS:
            return 'count_unique(user)';
        case utils_3.DisplayOption.SESSIONS:
        default:
            return 'sum(session)';
    }
}
exports.sessionDisplayToField = sessionDisplayToField;
var ReleaseHealthRequest = /** @class */ (function (_super) {
    tslib_1.__extends(ReleaseHealthRequest, _super);
    function ReleaseHealthRequest() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            errored: false,
            statusCountByReleaseInPeriod: null,
            totalCountByReleaseIn24h: null,
            totalCountByProjectIn24h: null,
            statusCountByProjectInPeriod: null,
        };
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, healthStatsPeriod, disable, promises, _b, statusCountByReleaseInPeriod, totalCountByReleaseIn24h, totalCountByProjectIn24h, statusCountByProjectInPeriod, error_1;
            var _c, _d;
            return tslib_1.__generator(this, function (_e) {
                switch (_e.label) {
                    case 0:
                        _a = this.props, api = _a.api, healthStatsPeriod = _a.healthStatsPeriod, disable = _a.disable;
                        if (disable) {
                            return [2 /*return*/];
                        }
                        api.clear();
                        this.setState({
                            loading: true,
                            errored: false,
                            statusCountByReleaseInPeriod: null,
                            totalCountByReleaseIn24h: null,
                            totalCountByProjectIn24h: null,
                        });
                        promises = [
                            this.fetchStatusCountByReleaseInPeriod(),
                            this.fetchTotalCountByReleaseIn24h(),
                            this.fetchTotalCountByProjectIn24h(),
                        ];
                        if (healthStatsPeriod === types_1.HealthStatsPeriodOption.AUTO) {
                            promises.push(this.fetchStatusCountByProjectInPeriod());
                        }
                        _e.label = 1;
                    case 1:
                        _e.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, Promise.all(promises)];
                    case 2:
                        _b = tslib_1.__read.apply(void 0, [_e.sent(), 4]), statusCountByReleaseInPeriod = _b[0], totalCountByReleaseIn24h = _b[1], totalCountByProjectIn24h = _b[2], statusCountByProjectInPeriod = _b[3];
                        this.setState({
                            loading: false,
                            statusCountByReleaseInPeriod: statusCountByReleaseInPeriod,
                            totalCountByReleaseIn24h: totalCountByReleaseIn24h,
                            totalCountByProjectIn24h: totalCountByProjectIn24h,
                            statusCountByProjectInPeriod: statusCountByProjectInPeriod,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _e.sent();
                        indicator_1.addErrorMessage((_d = (_c = error_1.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) !== null && _d !== void 0 ? _d : locale_1.t('Error loading health data'));
                        this.setState({
                            loading: false,
                            errored: true,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.getHealthData = function () {
            // TODO(sessions): investigate if this needs to be optimized to lower O(n) complexity
            return {
                getCrashCount: _this.getCrashCount,
                getCrashFreeRate: _this.getCrashFreeRate,
                get24hCountByRelease: _this.get24hCountByRelease,
                get24hCountByProject: _this.get24hCountByProject,
                getTimeSeries: _this.getTimeSeries,
                getAdoption: _this.getAdoption,
            };
        };
        _this.getCrashCount = function (version, project, display) {
            var _a;
            var statusCountByReleaseInPeriod = _this.state.statusCountByReleaseInPeriod;
            var field = sessionDisplayToField(display);
            return (_a = statusCountByReleaseInPeriod === null || statusCountByReleaseInPeriod === void 0 ? void 0 : statusCountByReleaseInPeriod.groups.find(function (_a) {
                var by = _a.by;
                return by.release === version &&
                    by.project === project &&
                    by['session.status'] === 'crashed';
            })) === null || _a === void 0 ? void 0 : _a.totals[field];
        };
        _this.getCrashFreeRate = function (version, project, display) {
            var _a;
            var statusCountByReleaseInPeriod = _this.state.statusCountByReleaseInPeriod;
            var field = sessionDisplayToField(display);
            var totalCount = (_a = statusCountByReleaseInPeriod === null || statusCountByReleaseInPeriod === void 0 ? void 0 : statusCountByReleaseInPeriod.groups.filter(function (_a) {
                var by = _a.by;
                return by.release === version && by.project === project;
            })) === null || _a === void 0 ? void 0 : _a.reduce(function (acc, group) { return acc + group.totals[field]; }, 0);
            var crashedCount = _this.getCrashCount(version, project, display);
            return !utils_2.defined(totalCount) || totalCount === 0
                ? null
                : _1.getCrashFreePercent(100 - utils_2.percent(crashedCount !== null && crashedCount !== void 0 ? crashedCount : 0, totalCount !== null && totalCount !== void 0 ? totalCount : 0));
        };
        _this.get24hCountByRelease = function (version, project, display) {
            var _a;
            var totalCountByReleaseIn24h = _this.state.totalCountByReleaseIn24h;
            var field = sessionDisplayToField(display);
            return (_a = totalCountByReleaseIn24h === null || totalCountByReleaseIn24h === void 0 ? void 0 : totalCountByReleaseIn24h.groups.filter(function (_a) {
                var by = _a.by;
                return by.release === version && by.project === project;
            })) === null || _a === void 0 ? void 0 : _a.reduce(function (acc, group) { return acc + group.totals[field]; }, 0);
        };
        _this.get24hCountByProject = function (project, display) {
            var _a;
            var totalCountByProjectIn24h = _this.state.totalCountByProjectIn24h;
            var field = sessionDisplayToField(display);
            return (_a = totalCountByProjectIn24h === null || totalCountByProjectIn24h === void 0 ? void 0 : totalCountByProjectIn24h.groups.filter(function (_a) {
                var by = _a.by;
                return by.project === project;
            })) === null || _a === void 0 ? void 0 : _a.reduce(function (acc, group) { return acc + group.totals[field]; }, 0);
        };
        _this.getTimeSeries = function (version, project, display) {
            var healthStatsPeriod = _this.props.healthStatsPeriod;
            if (healthStatsPeriod === types_1.HealthStatsPeriodOption.AUTO) {
                return _this.getPeriodTimeSeries(version, project, display);
            }
            return _this.get24hTimeSeries(version, project, display);
        };
        _this.get24hTimeSeries = function (version, project, display) {
            var _a, _b, _c;
            var _d = _this.state, totalCountByReleaseIn24h = _d.totalCountByReleaseIn24h, totalCountByProjectIn24h = _d.totalCountByProjectIn24h;
            var field = sessionDisplayToField(display);
            var intervals = (_a = totalCountByProjectIn24h === null || totalCountByProjectIn24h === void 0 ? void 0 : totalCountByProjectIn24h.intervals) !== null && _a !== void 0 ? _a : [];
            var projectData = (_b = totalCountByProjectIn24h === null || totalCountByProjectIn24h === void 0 ? void 0 : totalCountByProjectIn24h.groups.find(function (_a) {
                var by = _a.by;
                return by.project === project;
            })) === null || _b === void 0 ? void 0 : _b.series[field];
            var releaseData = (_c = totalCountByReleaseIn24h === null || totalCountByReleaseIn24h === void 0 ? void 0 : totalCountByReleaseIn24h.groups.find(function (_a) {
                var by = _a.by;
                return by.project === project && by.release === version;
            })) === null || _c === void 0 ? void 0 : _c.series[field];
            return [
                {
                    seriesName: locale_1.t('This Release'),
                    data: intervals === null || intervals === void 0 ? void 0 : intervals.map(function (interval, index) {
                        var _a;
                        return ({
                            name: moment_1.default(interval).valueOf(),
                            value: (_a = releaseData === null || releaseData === void 0 ? void 0 : releaseData[index]) !== null && _a !== void 0 ? _a : 0,
                        });
                    }),
                },
                {
                    seriesName: locale_1.t('Total Project'),
                    data: intervals === null || intervals === void 0 ? void 0 : intervals.map(function (interval, index) {
                        var _a;
                        return ({
                            name: moment_1.default(interval).valueOf(),
                            value: (_a = projectData === null || projectData === void 0 ? void 0 : projectData[index]) !== null && _a !== void 0 ? _a : 0,
                        });
                    }),
                    z: 0,
                },
            ];
        };
        _this.getPeriodTimeSeries = function (version, project, display) {
            var _a, _b, _c;
            var _d = _this.state, statusCountByReleaseInPeriod = _d.statusCountByReleaseInPeriod, statusCountByProjectInPeriod = _d.statusCountByProjectInPeriod;
            var field = sessionDisplayToField(display);
            var intervals = (_a = statusCountByProjectInPeriod === null || statusCountByProjectInPeriod === void 0 ? void 0 : statusCountByProjectInPeriod.intervals) !== null && _a !== void 0 ? _a : [];
            var projectData = (_b = statusCountByProjectInPeriod === null || statusCountByProjectInPeriod === void 0 ? void 0 : statusCountByProjectInPeriod.groups.filter(function (_a) {
                var by = _a.by;
                return by.project === project;
            })) === null || _b === void 0 ? void 0 : _b.reduce(function (acc, group) { return reduceTimeSeriesGroups(acc, group, field); }, []);
            var releaseData = (_c = statusCountByReleaseInPeriod === null || statusCountByReleaseInPeriod === void 0 ? void 0 : statusCountByReleaseInPeriod.groups.filter(function (_a) {
                var by = _a.by;
                return by.project === project && by.release === version;
            })) === null || _c === void 0 ? void 0 : _c.reduce(function (acc, group) { return reduceTimeSeriesGroups(acc, group, field); }, []);
            return [
                {
                    seriesName: locale_1.t('This Release'),
                    data: intervals === null || intervals === void 0 ? void 0 : intervals.map(function (interval, index) {
                        var _a;
                        return ({
                            name: moment_1.default(interval).valueOf(),
                            value: (_a = releaseData === null || releaseData === void 0 ? void 0 : releaseData[index]) !== null && _a !== void 0 ? _a : 0,
                        });
                    }),
                },
                {
                    seriesName: locale_1.t('Total Project'),
                    data: intervals === null || intervals === void 0 ? void 0 : intervals.map(function (interval, index) {
                        var _a;
                        return ({
                            name: moment_1.default(interval).valueOf(),
                            value: (_a = projectData === null || projectData === void 0 ? void 0 : projectData[index]) !== null && _a !== void 0 ? _a : 0,
                        });
                    }),
                    z: 0,
                },
            ];
        };
        _this.getAdoption = function (version, project, display) {
            var get24hCountByRelease = _this.get24hCountByRelease(version, project, display);
            var get24hCountByProject = _this.get24hCountByProject(project, display);
            return utils_2.defined(get24hCountByRelease) && utils_2.defined(get24hCountByProject)
                ? utils_2.percent(get24hCountByRelease, get24hCountByProject)
                : undefined;
        };
        return _this;
    }
    ReleaseHealthRequest.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ReleaseHealthRequest.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.releasesReloading) {
            return;
        }
        if (isEqual_1.default(omitIgnoredProps(prevProps), omitIgnoredProps(this.props))) {
            return;
        }
        this.fetchData();
    };
    Object.defineProperty(ReleaseHealthRequest.prototype, "path", {
        get: function () {
            var organization = this.props.organization;
            return "/organizations/" + organization.slug + "/sessions/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ReleaseHealthRequest.prototype, "baseQueryParams", {
        get: function () {
            var _a = this.props, location = _a.location, selection = _a.selection, defaultStatsPeriod = _a.defaultStatsPeriod, releases = _a.releases;
            return tslib_1.__assign({ query: new tokenizeSearch_1.QueryResults(releases.reduce(function (acc, release, index, allReleases) {
                    acc.push("release:\"" + release + "\"");
                    if (index < allReleases.length - 1) {
                        acc.push('OR');
                    }
                    return acc;
                }, [])).formatString(), interval: getInterval(selection.datetime) }, getParams_1.getParams(pick_1.default(location.query, Object.values(globalSelectionHeader_1.URL_PARAM)), {
                defaultStatsPeriod: defaultStatsPeriod,
            }));
        },
        enumerable: false,
        configurable: true
    });
    /**
     * Used to calculate crash free rate, count histogram (This Release series), and crash count
     */
    ReleaseHealthRequest.prototype.fetchStatusCountByReleaseInPeriod = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, display, response;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, display = _a.display;
                        return [4 /*yield*/, api.requestPromise(this.path, {
                                query: tslib_1.__assign(tslib_1.__assign({}, this.baseQueryParams), { field: tslib_1.__spreadArray([], tslib_1.__read(new Set(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(display.map(function (d) { return sessionDisplayToField(d); }))), ['sum(session)'])))), groupBy: ['project', 'release', 'session.status'] }),
                            })];
                    case 1:
                        response = _b.sent();
                        return [2 /*return*/, response];
                }
            });
        });
    };
    /**
     * Used to calculate count histogram (Total Project series)
     */
    ReleaseHealthRequest.prototype.fetchStatusCountByProjectInPeriod = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, display, response;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, display = _a.display;
                        return [4 /*yield*/, api.requestPromise(this.path, {
                                query: tslib_1.__assign(tslib_1.__assign({}, this.baseQueryParams), { query: undefined, field: tslib_1.__spreadArray([], tslib_1.__read(new Set(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(display.map(function (d) { return sessionDisplayToField(d); }))), ['sum(session)'])))), groupBy: ['project', 'session.status'] }),
                            })];
                    case 1:
                        response = _b.sent();
                        return [2 /*return*/, response];
                }
            });
        });
    };
    /**
     * Used to calculate adoption, and count histogram (This Release series)
     */
    ReleaseHealthRequest.prototype.fetchTotalCountByReleaseIn24h = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, display, response;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, display = _a.display;
                        return [4 /*yield*/, api.requestPromise(this.path, {
                                query: tslib_1.__assign(tslib_1.__assign({}, this.baseQueryParams), { field: display.map(function (d) { return sessionDisplayToField(d); }), groupBy: ['project', 'release'], interval: '1h', statsPeriod: '24h' }),
                            })];
                    case 1:
                        response = _b.sent();
                        return [2 /*return*/, response];
                }
            });
        });
    };
    /**
     * Used to calculate adoption, and count histogram (Total Project series)
     */
    ReleaseHealthRequest.prototype.fetchTotalCountByProjectIn24h = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, display, response;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, display = _a.display;
                        return [4 /*yield*/, api.requestPromise(this.path, {
                                query: tslib_1.__assign(tslib_1.__assign({}, this.baseQueryParams), { query: undefined, field: display.map(function (d) { return sessionDisplayToField(d); }), groupBy: ['project'], interval: '1h', statsPeriod: '24h' }),
                            })];
                    case 1:
                        response = _b.sent();
                        return [2 /*return*/, response];
                }
            });
        });
    };
    ReleaseHealthRequest.prototype.render = function () {
        var _a = this.state, loading = _a.loading, errored = _a.errored;
        var children = this.props.children;
        return children({
            isHealthLoading: loading,
            errored: errored,
            getHealthData: this.getHealthData(),
        });
    };
    return ReleaseHealthRequest;
}(React.Component));
exports.default = withApi_1.default(ReleaseHealthRequest);
//# sourceMappingURL=releaseHealthRequest.jsx.map