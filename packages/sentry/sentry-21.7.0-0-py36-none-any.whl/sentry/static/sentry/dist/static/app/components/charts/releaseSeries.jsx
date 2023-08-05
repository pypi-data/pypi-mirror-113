Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var react_1 = require("@emotion/react");
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var memoize_1 = tslib_1.__importDefault(require("lodash/memoize"));
var partition_1 = tslib_1.__importDefault(require("lodash/partition"));
var indicator_1 = require("app/actionCreators/indicator");
var markLine_1 = tslib_1.__importDefault(require("app/components/charts/components/markLine"));
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var dates_1 = require("app/utils/dates");
var formatters_1 = require("app/utils/formatters");
var parseLinkHeader_1 = tslib_1.__importDefault(require("app/utils/parseLinkHeader"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
// This is not an exported action/function because releases list uses AsyncComponent
// and this is not re-used anywhere else afaict
function getOrganizationReleases(api, organization, conditions) {
    var query = {};
    Object.keys(conditions).forEach(function (key) {
        var value = conditions[key];
        if (value && (key === 'start' || key === 'end')) {
            value = dates_1.getUtcDateString(value);
        }
        if (value) {
            query[key] = value;
        }
    });
    api.clear();
    return api.requestPromise("/organizations/" + organization.slug + "/releases/stats/", {
        includeAllArgs: true,
        method: 'GET',
        query: query,
    });
}
var ReleaseSeries = /** @class */ (function (_super) {
    tslib_1.__extends(ReleaseSeries, _super);
    function ReleaseSeries() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            releases: null,
            releaseSeries: [],
        };
        _this._isMounted = false;
        _this.getOrganizationReleasesMemoized = memoize_1.default(function (api, conditions, organization) {
            return getOrganizationReleases(api, conditions, organization);
        }, function (_, __, conditions) {
            return Object.values(conditions)
                .map(function (val) { return JSON.stringify(val); })
                .join('-');
        });
        _this.getReleaseSeries = function (releases, lineStyle) {
            if (lineStyle === void 0) { lineStyle = {}; }
            var _a = _this.props, organization = _a.organization, router = _a.router, tooltip = _a.tooltip, environments = _a.environments, start = _a.start, end = _a.end, period = _a.period, preserveQueryParams = _a.preserveQueryParams, queryExtra = _a.queryExtra, theme = _a.theme;
            var query = tslib_1.__assign({}, queryExtra);
            if (organization.features.includes('global-views')) {
                query.project = router.location.query.project;
            }
            if (preserveQueryParams) {
                query.environment = tslib_1.__spreadArray([], tslib_1.__read(environments));
                query.start = start ? dates_1.getUtcDateString(start) : undefined;
                query.end = end ? dates_1.getUtcDateString(end) : undefined;
                query.statsPeriod = period || undefined;
            }
            var markLine = markLine_1.default({
                animation: false,
                lineStyle: tslib_1.__assign({ color: theme.purple300, opacity: 0.3, type: 'solid' }, lineStyle),
                label: {
                    show: false,
                },
                data: releases.map(function (release) { return ({
                    xAxis: +new Date(release.date),
                    name: formatters_1.formatVersion(release.version, true),
                    value: formatters_1.formatVersion(release.version, true),
                    onClick: function () {
                        router.push({
                            pathname: "/organizations/" + organization.slug + "/releases/" + release.version + "/",
                            query: query,
                        });
                    },
                    label: {
                        formatter: function () { return formatters_1.formatVersion(release.version, true); },
                    },
                }); }),
            });
            // TODO(tonyx): This conflicts with the types declaration of `MarkLine`
            // if we add it in the constructor. So we opt to add it here so typescript
            // doesn't complain.
            markLine.tooltip =
                tooltip ||
                    {
                        trigger: 'item',
                        formatter: function (_a) {
                            var data = _a.data;
                            // XXX using this.props here as this function does not get re-run
                            // unless projects are changed. Using a closure variable would result
                            // in stale values.
                            var time = dates_1.getFormattedDate(data.value, 'MMM D, YYYY LT', {
                                local: !_this.props.utc,
                            });
                            var version = utils_1.escape(formatters_1.formatVersion(data.name, true));
                            return [
                                '<div class="tooltip-series">',
                                "<div><span class=\"tooltip-label\"><strong>" + locale_1.t('Release') + "</strong></span> " + version + "</div>",
                                '</div>',
                                '<div class="tooltip-date">',
                                time,
                                '</div>',
                                '</div>',
                                '<div class="tooltip-arrow"></div>',
                            ].join('');
                        },
                    };
            return {
                seriesName: 'Releases',
                color: theme.purple200,
                data: [],
                markLine: markLine,
            };
        };
        return _this;
    }
    ReleaseSeries.prototype.componentDidMount = function () {
        this._isMounted = true;
        var releases = this.props.releases;
        if (releases) {
            // No need to fetch releases if passed in from props
            this.setReleasesWithSeries(releases);
            return;
        }
        this.fetchData();
    };
    ReleaseSeries.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual_1.default(prevProps.projects, this.props.projects) ||
            !isEqual_1.default(prevProps.environments, this.props.environments) ||
            !isEqual_1.default(prevProps.start, this.props.start) ||
            !isEqual_1.default(prevProps.end, this.props.end) ||
            !isEqual_1.default(prevProps.period, this.props.period) ||
            !isEqual_1.default(prevProps.query, this.props.query)) {
            this.fetchData();
        }
        else if (!isEqual_1.default(prevProps.emphasizeReleases, this.props.emphasizeReleases)) {
            this.setReleasesWithSeries(this.state.releases);
        }
    };
    ReleaseSeries.prototype.componentWillUnmount = function () {
        this._isMounted = false;
        this.props.api.clear();
    };
    ReleaseSeries.prototype.fetchData = function () {
        var _a, _b;
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _c, api, organization, projects, environments, period, start, end, memoized, query, conditions, hasMore, releases, getReleases, _d, newReleases, xhr, pageLinks, paginationObject, _e;
            return tslib_1.__generator(this, function (_f) {
                switch (_f.label) {
                    case 0:
                        _c = this.props, api = _c.api, organization = _c.organization, projects = _c.projects, environments = _c.environments, period = _c.period, start = _c.start, end = _c.end, memoized = _c.memoized, query = _c.query;
                        conditions = {
                            start: start,
                            end: end,
                            project: projects,
                            environment: environments,
                            statsPeriod: period,
                            query: query,
                        };
                        hasMore = true;
                        releases = [];
                        _f.label = 1;
                    case 1:
                        if (!hasMore) return [3 /*break*/, 6];
                        _f.label = 2;
                    case 2:
                        _f.trys.push([2, 4, , 5]);
                        getReleases = memoized
                            ? this.getOrganizationReleasesMemoized
                            : getOrganizationReleases;
                        return [4 /*yield*/, getReleases(api, organization, conditions)];
                    case 3:
                        _d = tslib_1.__read.apply(void 0, [_f.sent(), 3]), newReleases = _d[0], xhr = _d[2];
                        releases.push.apply(releases, tslib_1.__spreadArray([], tslib_1.__read(newReleases)));
                        if (this._isMounted) {
                            this.setReleasesWithSeries(releases);
                        }
                        pageLinks = xhr && xhr.getResponseHeader('Link');
                        if (pageLinks) {
                            paginationObject = parseLinkHeader_1.default(pageLinks);
                            hasMore = (_b = (_a = paginationObject === null || paginationObject === void 0 ? void 0 : paginationObject.next) === null || _a === void 0 ? void 0 : _a.results) !== null && _b !== void 0 ? _b : false;
                            conditions.cursor = paginationObject.next.cursor;
                        }
                        else {
                            hasMore = false;
                        }
                        return [3 /*break*/, 5];
                    case 4:
                        _e = _f.sent();
                        indicator_1.addErrorMessage(locale_1.t('Error fetching releases'));
                        hasMore = false;
                        return [3 /*break*/, 5];
                    case 5: return [3 /*break*/, 1];
                    case 6: return [2 /*return*/];
                }
            });
        });
    };
    ReleaseSeries.prototype.setReleasesWithSeries = function (releases) {
        var _a = this.props.emphasizeReleases, emphasizeReleases = _a === void 0 ? [] : _a;
        var releaseSeries = [];
        if (emphasizeReleases.length) {
            var _b = tslib_1.__read(partition_1.default(releases, function (release) { return !emphasizeReleases.includes(release.version); }), 2), unemphasizedReleases = _b[0], emphasizedReleases = _b[1];
            if (unemphasizedReleases.length) {
                releaseSeries.push(this.getReleaseSeries(unemphasizedReleases, { type: 'dotted' }));
            }
            if (emphasizedReleases.length) {
                releaseSeries.push(this.getReleaseSeries(emphasizedReleases, {
                    opacity: 0.8,
                }));
            }
        }
        else {
            releaseSeries.push(this.getReleaseSeries(releases));
        }
        this.setState({
            releases: releases,
            releaseSeries: releaseSeries,
        });
    };
    ReleaseSeries.prototype.render = function () {
        var children = this.props.children;
        return children({
            releases: this.state.releases,
            releaseSeries: this.state.releaseSeries,
        });
    };
    return ReleaseSeries;
}(React.Component));
exports.default = react_router_1.withRouter(withOrganization_1.default(withApi_1.default(react_1.withTheme(ReleaseSeries))));
//# sourceMappingURL=releaseSeries.jsx.map