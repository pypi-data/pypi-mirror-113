Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var events_1 = require("app/actionCreators/events");
var utils_1 = require("app/components/charts/utils");
var utils_2 = require("app/components/organizations/globalSelectionHeader/utils");
var locale_1 = require("app/locale");
var dates_1 = require("app/utils/dates");
var genericDiscoverQuery_1 = require("app/utils/discover/genericDiscoverQuery");
var utils_3 = require("./utils");
// Don't fetch more than 4000 bins as we're plotting on a small area.
var MAX_BIN_COUNT = 4000;
function getWidgetInterval(widget, datetimeObj) {
    // Bars charts are daily totals to aligned with discover. It also makes them
    // usefully different from line/area charts until we expose the interval control, or remove it.
    var interval = widget.displayType === 'bar' ? '1d' : widget.interval;
    if (!interval) {
        // Default to 5 minutes
        interval = '5m';
    }
    var desiredPeriod = dates_1.parsePeriodToHours(interval);
    var selectedRange = utils_1.getDiffInMinutes(datetimeObj);
    if (selectedRange / desiredPeriod > MAX_BIN_COUNT) {
        return utils_1.getInterval(datetimeObj, true);
    }
    return interval;
}
function transformSeries(stats, seriesName) {
    return {
        seriesName: seriesName,
        data: stats.data.map(function (_a) {
            var _b = tslib_1.__read(_a, 2), timestamp = _b[0], counts = _b[1];
            return ({
                name: timestamp * 1000,
                value: counts.reduce(function (acc, _a) {
                    var count = _a.count;
                    return acc + count;
                }, 0),
            });
        }),
    };
}
function transformResult(query, result) {
    var output = [];
    var seriesNamePrefix = query.name;
    if (utils_1.isMultiSeriesStats(result)) {
        // Convert multi-series results into chartable series. Multi series results
        // are created when multiple yAxis are used. Convert the timeseries
        // data into a multi-series result set.  As the server will have
        // replied with a map like: {[titleString: string]: EventsStats}
        var transformed = Object.keys(result)
            .map(function (seriesName) {
            var prefixedName = seriesNamePrefix
                ? seriesNamePrefix + " : " + seriesName
                : seriesName;
            var seriesData = result[seriesName];
            return [seriesData.order || 0, transformSeries(seriesData, prefixedName)];
        })
            .sort(function (a, b) { return a[0] - b[0]; })
            .map(function (item) { return item[1]; });
        output = output.concat(transformed);
    }
    else {
        var field = query.fields[0];
        var prefixedName = seriesNamePrefix ? seriesNamePrefix + " : " + field : field;
        var transformed = transformSeries(result, prefixedName);
        output.push(transformed);
    }
    return output;
}
var WidgetQueries = /** @class */ (function (_super) {
    tslib_1.__extends(WidgetQueries, _super);
    function WidgetQueries() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            queryFetchID: undefined,
            errorMessage: undefined,
            timeseriesResults: undefined,
            rawResults: undefined,
            tableResults: undefined,
        };
        return _this;
    }
    WidgetQueries.prototype.componentDidMount = function () {
        this.fetchData();
    };
    WidgetQueries.prototype.componentDidUpdate = function (prevProps) {
        var _a;
        var _b = this.props, selection = _b.selection, widget = _b.widget;
        // We do not fetch data whenever the query name changes.
        var _c = tslib_1.__read(prevProps.widget.queries.reduce(function (_a, _b) {
            var _c = tslib_1.__read(_a, 2), names = _c[0], queries = _c[1];
            var name = _b.name, rest = tslib_1.__rest(_b, ["name"]);
            names.push(name);
            queries.push(rest);
            return [names, queries];
        }, [[], []]), 2), prevWidgetQueryNames = _c[0], prevWidgetQueries = _c[1];
        var _d = tslib_1.__read(widget.queries.reduce(function (_a, _b) {
            var _c = tslib_1.__read(_a, 2), names = _c[0], queries = _c[1];
            var name = _b.name, rest = tslib_1.__rest(_b, ["name"]);
            names.push(name);
            queries.push(rest);
            return [names, queries];
        }, [[], []]), 2), widgetQueryNames = _d[0], widgetQueries = _d[1];
        if (!isEqual_1.default(widget.displayType, prevProps.widget.displayType) ||
            !isEqual_1.default(widget.interval, prevProps.widget.interval) ||
            !isEqual_1.default(widgetQueries, prevWidgetQueries) ||
            !isEqual_1.default(widget.displayType, prevProps.widget.displayType) ||
            !utils_2.isSelectionEqual(selection, prevProps.selection)) {
            this.fetchData();
            return;
        }
        if (!this.state.loading &&
            !isEqual_1.default(prevWidgetQueryNames, widgetQueryNames) &&
            ((_a = this.state.rawResults) === null || _a === void 0 ? void 0 : _a.length) === widget.queries.length) {
            // If the query names has changed, then update timeseries labels
            // eslint-disable-next-line react/no-did-update-set-state
            this.setState(function (prevState) {
                var timeseriesResults = widget.queries.reduce(function (acc, query, index) {
                    return acc.concat(transformResult(query, prevState.rawResults[index]));
                }, []);
                return tslib_1.__assign(tslib_1.__assign({}, prevState), { timeseriesResults: timeseriesResults });
            });
        }
    };
    WidgetQueries.prototype.fetchEventData = function (queryFetchID) {
        var _this = this;
        var _a = this.props, selection = _a.selection, api = _a.api, organization = _a.organization, widget = _a.widget;
        var tableResults = [];
        // Table, world map, and stat widgets use table results and need
        // to do a discover 'table' query instead of a 'timeseries' query.
        this.setState({ tableResults: [] });
        var promises = widget.queries.map(function (query) {
            var eventView = utils_3.eventViewFromWidget(widget.title, query, selection);
            var url = '';
            var params = {
                per_page: 5,
                noPagination: true,
            };
            if (widget.displayType === 'table') {
                url = "/organizations/" + organization.slug + "/eventsv2/";
                params.referrer = 'api.dashboards.tablewidget';
            }
            else if (widget.displayType === 'big_number') {
                url = "/organizations/" + organization.slug + "/eventsv2/";
                params.per_page = 1;
                params.referrer = 'api.dashboards.bignumberwidget';
            }
            else if (widget.displayType === 'world_map') {
                url = "/organizations/" + organization.slug + "/events-geo/";
                delete params.per_page;
                params.referrer = 'api.dashboards.worldmapwidget';
            }
            else {
                throw Error('Expected widget displayType to be either big_number, table or world_map');
            }
            return genericDiscoverQuery_1.doDiscoverQuery(api, url, tslib_1.__assign(tslib_1.__assign({}, eventView.generateQueryStringObject()), params));
        });
        var completed = 0;
        promises.forEach(function (promise, i) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, data, tableData, err_1, errorMessage;
            var _b, _c, _d;
            return tslib_1.__generator(this, function (_e) {
                switch (_e.label) {
                    case 0:
                        _e.trys.push([0, 2, 3, 4]);
                        return [4 /*yield*/, promise];
                    case 1:
                        _a = tslib_1.__read.apply(void 0, [_e.sent(), 1]), data = _a[0];
                        tableData = data;
                        tableData.title = (_c = (_b = widget.queries[i]) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '';
                        // Overwrite the local var to work around state being stale in tests.
                        tableResults = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(tableResults)), [tableData]);
                        this.setState(function (prevState) {
                            if (prevState.queryFetchID !== queryFetchID) {
                                // invariant: a different request was initiated after this request
                                return prevState;
                            }
                            return tslib_1.__assign(tslib_1.__assign({}, prevState), { tableResults: tableResults });
                        });
                        return [3 /*break*/, 4];
                    case 2:
                        err_1 = _e.sent();
                        errorMessage = ((_d = err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON) === null || _d === void 0 ? void 0 : _d.detail) || locale_1.t('An unknown error occurred.');
                        this.setState({ errorMessage: errorMessage });
                        return [3 /*break*/, 4];
                    case 3:
                        completed++;
                        this.setState(function (prevState) {
                            if (prevState.queryFetchID !== queryFetchID) {
                                // invariant: a different request was initiated after this request
                                return prevState;
                            }
                            return tslib_1.__assign(tslib_1.__assign({}, prevState), { loading: completed === promises.length ? false : true });
                        });
                        return [7 /*endfinally*/];
                    case 4: return [2 /*return*/];
                }
            });
        }); });
    };
    WidgetQueries.prototype.fetchTimeseriesData = function (queryFetchID) {
        var _this = this;
        var _a = this.props, selection = _a.selection, api = _a.api, organization = _a.organization, widget = _a.widget;
        this.setState({ timeseriesResults: [], rawResults: [] });
        var environments = selection.environments, projects = selection.projects;
        var _b = selection.datetime, start = _b.start, end = _b.end, statsPeriod = _b.period;
        var interval = getWidgetInterval(widget, {
            start: start,
            end: end,
            period: statsPeriod,
        });
        var promises = widget.queries.map(function (query) {
            var requestData = {
                organization: organization,
                interval: interval,
                start: start,
                end: end,
                project: projects,
                environment: environments,
                period: statsPeriod,
                query: query.conditions,
                yAxis: query.fields,
                orderby: query.orderby,
                includePrevious: false,
                referrer: 'api.dashboards.timeserieswidget',
                partial: true,
            };
            return events_1.doEventsRequest(api, requestData);
        });
        var completed = 0;
        promises.forEach(function (promise, i) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var rawResults_1, err_2, errorMessage;
            var _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _b.trys.push([0, 2, 3, 4]);
                        return [4 /*yield*/, promise];
                    case 1:
                        rawResults_1 = _b.sent();
                        this.setState(function (prevState) {
                            var _a, _b;
                            if (prevState.queryFetchID !== queryFetchID) {
                                // invariant: a different request was initiated after this request
                                return prevState;
                            }
                            var timeseriesResults = ((_a = prevState.timeseriesResults) !== null && _a !== void 0 ? _a : []).concat(transformResult(widget.queries[i], rawResults_1));
                            return tslib_1.__assign(tslib_1.__assign({}, prevState), { timeseriesResults: timeseriesResults, rawResults: ((_b = prevState.rawResults) !== null && _b !== void 0 ? _b : []).concat(rawResults_1) });
                        });
                        return [3 /*break*/, 4];
                    case 2:
                        err_2 = _b.sent();
                        errorMessage = ((_a = err_2 === null || err_2 === void 0 ? void 0 : err_2.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) || locale_1.t('An unknown error occurred.');
                        this.setState({ errorMessage: errorMessage });
                        return [3 /*break*/, 4];
                    case 3:
                        completed++;
                        this.setState(function (prevState) {
                            if (prevState.queryFetchID !== queryFetchID) {
                                // invariant: a different request was initiated after this request
                                return prevState;
                            }
                            return tslib_1.__assign(tslib_1.__assign({}, prevState), { loading: completed === promises.length ? false : true });
                        });
                        return [7 /*endfinally*/];
                    case 4: return [2 /*return*/];
                }
            });
        }); });
    };
    WidgetQueries.prototype.fetchData = function () {
        var widget = this.props.widget;
        var queryFetchID = Symbol('queryFetchID');
        this.setState({ loading: true, errorMessage: undefined, queryFetchID: queryFetchID });
        if (['table', 'world_map', 'big_number'].includes(widget.displayType)) {
            this.fetchEventData(queryFetchID);
        }
        else {
            this.fetchTimeseriesData(queryFetchID);
        }
    };
    WidgetQueries.prototype.render = function () {
        var children = this.props.children;
        var _a = this.state, loading = _a.loading, timeseriesResults = _a.timeseriesResults, tableResults = _a.tableResults, errorMessage = _a.errorMessage;
        return children({ loading: loading, timeseriesResults: timeseriesResults, tableResults: tableResults, errorMessage: errorMessage });
    };
    return WidgetQueries;
}(React.Component));
exports.default = WidgetQueries;
//# sourceMappingURL=widgetQueries.jsx.map