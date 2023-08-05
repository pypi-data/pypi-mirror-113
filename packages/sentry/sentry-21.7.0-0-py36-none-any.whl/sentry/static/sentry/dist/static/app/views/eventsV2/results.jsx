Object.defineProperty(exports, "__esModule", { value: true });
exports.Top = exports.StyledSearchBar = exports.StyledPageContent = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var ReactRouter = tslib_1.__importStar(require("react-router"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var events_1 = require("app/actionCreators/events");
var projects_1 = require("app/actionCreators/projects");
var tags_1 = require("app/actionCreators/tags");
var api_1 = require("app/api");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var searchBar_1 = tslib_1.__importDefault(require("app/components/events/searchBar"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var eventView_1 = tslib_1.__importStar(require("app/utils/discover/eventView"));
var fields_1 = require("app/utils/discover/fields");
var localStorage_1 = tslib_1.__importDefault(require("app/utils/localStorage"));
var queryString_1 = require("app/utils/queryString");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var utils_2 = require("../performance/utils");
var data_1 = require("./data");
var resultsChart_1 = tslib_1.__importDefault(require("./resultsChart"));
var resultsHeader_1 = tslib_1.__importDefault(require("./resultsHeader"));
var table_1 = tslib_1.__importDefault(require("./table"));
var tags_2 = tslib_1.__importDefault(require("./tags"));
var utils_3 = require("./utils");
var SHOW_TAGS_STORAGE_KEY = 'discover2:show-tags';
function readShowTagsState() {
    var value = localStorage_1.default.getItem(SHOW_TAGS_STORAGE_KEY);
    return value === '1';
}
var Results = /** @class */ (function (_super) {
    tslib_1.__extends(Results, _super);
    function Results() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: eventView_1.default.fromSavedQueryOrLocation(_this.props.savedQuery, _this.props.location),
            error: '',
            errorCode: 200,
            totalValues: null,
            showTags: readShowTagsState(),
            needConfirmation: false,
            confirmedQuery: false,
            incompatibleAlertNotice: null,
        };
        _this.tagsApi = new api_1.Client();
        _this.canLoadEvents = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, location, organization, eventView, needConfirmation, confirmedQuery, currentQuery, duration, projectLength, results, err_1;
            var _this = this;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, location = _a.location, organization = _a.organization;
                        eventView = this.state.eventView;
                        needConfirmation = false;
                        confirmedQuery = true;
                        currentQuery = eventView.getEventsAPIPayload(location);
                        duration = eventView.getDays();
                        if (!(duration > 30 && currentQuery.project)) return [3 /*break*/, 5];
                        projectLength = currentQuery.project.length;
                        if (!(projectLength === 0 ||
                            (projectLength === 1 && currentQuery.project[0] === '-1'))) return [3 /*break*/, 4];
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, projects_1.fetchProjectsCount(api, organization.slug)];
                    case 2:
                        results = _b.sent();
                        if (projectLength === 0)
                            projectLength = results.myProjects;
                        else
                            projectLength = results.allProjects;
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        return [3 /*break*/, 4];
                    case 4:
                        if (projectLength > 10) {
                            needConfirmation = true;
                            confirmedQuery = false;
                        }
                        _b.label = 5;
                    case 5:
                        // Once confirmed, a change of project or datetime will happen before this can set it to false,
                        // this means a query will still happen even if the new conditions need confirmation
                        // using a state callback to return this to false
                        this.setState({ needConfirmation: needConfirmation, confirmedQuery: confirmedQuery }, function () {
                            _this.setState({ confirmedQuery: false });
                        });
                        if (needConfirmation) {
                            this.openConfirm();
                        }
                        return [2 /*return*/];
                }
            });
        }); };
        _this.openConfirm = function () { };
        _this.setOpenFunction = function (_a) {
            var open = _a.open;
            _this.openConfirm = open;
            return null;
        };
        _this.handleConfirmed = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _this = this;
            return tslib_1.__generator(this, function (_a) {
                this.setState({ needConfirmation: false, confirmedQuery: true }, function () {
                    _this.setState({ confirmedQuery: false });
                });
                return [2 /*return*/];
            });
        }); };
        _this.handleCancelled = function () {
            _this.setState({ needConfirmation: false, confirmedQuery: false });
        };
        _this.handleChangeShowTags = function () {
            var organization = _this.props.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'discover_v2.results.toggle_tag_facets',
                eventName: 'Discoverv2: Toggle Tag Facets',
                organization_id: parseInt(organization.id, 10),
            });
            _this.setState(function (state) {
                var newValue = !state.showTags;
                localStorage_1.default.setItem(SHOW_TAGS_STORAGE_KEY, newValue ? '1' : '0');
                return tslib_1.__assign(tslib_1.__assign({}, state), { showTags: newValue });
            });
        };
        _this.handleSearch = function (query) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var queryParams = getParams_1.getParams(tslib_1.__assign(tslib_1.__assign({}, (location.query || {})), { query: query }));
            // do not propagate pagination when making a new search
            var searchQueryParams = omit_1.default(queryParams, 'cursor');
            router.push({
                pathname: location.pathname,
                query: searchQueryParams,
            });
        };
        _this.handleYAxisChange = function (value) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var newQuery = tslib_1.__assign(tslib_1.__assign({}, location.query), { yAxis: value });
            router.push({
                pathname: location.pathname,
                query: newQuery,
            });
            // Treat axis changing like the user already confirmed the query
            if (!_this.state.needConfirmation) {
                _this.handleConfirmed();
            }
            analytics_1.trackAnalyticsEvent({
                eventKey: 'discover_v2.y_axis_change',
                eventName: "Discoverv2: Change chart's y axis",
                organization_id: parseInt(_this.props.organization.id, 10),
                y_axis_value: value,
            });
        };
        _this.handleDisplayChange = function (value) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var newQuery = tslib_1.__assign(tslib_1.__assign({}, location.query), { display: value });
            router.push({
                pathname: location.pathname,
                query: newQuery,
            });
            // Treat display changing like the user already confirmed the query
            if (!_this.state.needConfirmation) {
                _this.handleConfirmed();
            }
        };
        _this.generateTagUrl = function (key, value) {
            var organization = _this.props.organization;
            var eventView = _this.state.eventView;
            var url = eventView.getResultsViewUrlTarget(organization.slug);
            url.query = utils_1.generateQueryWithTag(url.query, {
                key: key,
                value: value,
            });
            return url;
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, errors) {
            var organization = _this.props.organization;
            var eventView = _this.state.eventView;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'discover_v2.create_alert_clicked',
                eventName: 'Discoverv2: Create alert clicked',
                status: 'error',
                query: eventView.query,
                errors: errors,
                organization_id: organization.id,
                url: window.location.href,
            });
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        _this.setError = function (error, errorCode) {
            _this.setState({ error: error, errorCode: errorCode });
        };
        return _this;
    }
    Results.getDerivedStateFromProps = function (nextProps, prevState) {
        if (nextProps.savedQuery || !nextProps.loading) {
            var eventView = eventView_1.default.fromSavedQueryOrLocation(nextProps.savedQuery, nextProps.location);
            return tslib_1.__assign(tslib_1.__assign({}, prevState), { eventView: eventView });
        }
        return prevState;
    };
    Results.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, selection = _a.selection;
        tags_1.loadOrganizationTags(this.tagsApi, organization.slug, selection);
        utils_2.addRoutePerformanceContext(selection);
        this.checkEventView();
        this.canLoadEvents();
    };
    Results.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a = this.props, api = _a.api, location = _a.location, organization = _a.organization, selection = _a.selection;
        var _b = this.state, eventView = _b.eventView, confirmedQuery = _b.confirmedQuery;
        this.checkEventView();
        var currentQuery = eventView.getEventsAPIPayload(location);
        var prevQuery = prevState.eventView.getEventsAPIPayload(prevProps.location);
        if (!eventView_1.isAPIPayloadSimilar(currentQuery, prevQuery) ||
            this.hasChartParametersChanged(prevState.eventView, eventView)) {
            api.clear();
            this.canLoadEvents();
        }
        if (!isEqual_1.default(prevProps.selection.datetime, selection.datetime) ||
            !isEqual_1.default(prevProps.selection.projects, selection.projects)) {
            tags_1.loadOrganizationTags(this.tagsApi, organization.slug, selection);
            utils_2.addRoutePerformanceContext(selection);
        }
        if (prevState.confirmedQuery !== confirmedQuery)
            this.fetchTotalCount();
    };
    Results.prototype.hasChartParametersChanged = function (prevEventView, eventView) {
        var prevYAxisValue = prevEventView.getYAxis();
        var yAxisValue = eventView.getYAxis();
        if (prevYAxisValue !== yAxisValue) {
            return true;
        }
        var prevDisplay = prevEventView.getDisplayMode();
        var display = eventView.getDisplayMode();
        return prevDisplay !== display;
    };
    Results.prototype.fetchTotalCount = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, organization, location, _b, eventView, confirmedQuery, totals, err_2;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, location = _a.location;
                        _b = this.state, eventView = _b.eventView, confirmedQuery = _b.confirmedQuery;
                        if (confirmedQuery === false || !eventView.isValid()) {
                            return [2 /*return*/];
                        }
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, events_1.fetchTotalCount(api, organization.slug, eventView.getEventsAPIPayload(location))];
                    case 2:
                        totals = _c.sent();
                        this.setState({ totalValues: totals });
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _c.sent();
                        Sentry.captureException(err_2);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    Results.prototype.checkEventView = function () {
        var _a;
        var eventView = this.state.eventView;
        var loading = this.props.loading;
        if (eventView.isValid() || loading) {
            return;
        }
        // If the view is not valid, redirect to a known valid state.
        var _b = this.props, location = _b.location, organization = _b.organization, selection = _b.selection;
        var nextEventView = eventView_1.default.fromNewQueryWithLocation(data_1.DEFAULT_EVENT_VIEW, location);
        if (nextEventView.project.length === 0 && selection.projects) {
            nextEventView.project = selection.projects;
        }
        if ((_a = location.query) === null || _a === void 0 ? void 0 : _a.query) {
            nextEventView.query = queryString_1.decodeScalar(location.query.query, '');
        }
        ReactRouter.browserHistory.replace(nextEventView.getResultsViewUrlTarget(organization.slug));
    };
    Results.prototype.getDocumentTitle = function () {
        var organization = this.props.organization;
        var eventView = this.state.eventView;
        if (!eventView) {
            return '';
        }
        return utils_3.generateTitle({ eventView: eventView, organization: organization });
    };
    Results.prototype.renderTagsTable = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var _b = this.state, eventView = _b.eventView, totalValues = _b.totalValues, confirmedQuery = _b.confirmedQuery;
        return (<Layout.Side>
        <tags_2.default generateUrl={this.generateTagUrl} totalValues={totalValues} eventView={eventView} organization={organization} location={location} confirmedQuery={confirmedQuery}/>
      </Layout.Side>);
    };
    Results.prototype.renderError = function (error) {
        if (!error) {
            return null;
        }
        return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
        {error}
      </alert_1.default>);
    };
    Results.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, router = _a.router;
        var _b = this.state, eventView = _b.eventView, error = _b.error, errorCode = _b.errorCode, totalValues = _b.totalValues, showTags = _b.showTags, incompatibleAlertNotice = _b.incompatibleAlertNotice, confirmedQuery = _b.confirmedQuery;
        var fields = eventView.hasAggregateField()
            ? fields_1.generateAggregateFields(organization, eventView.fields)
            : eventView.fields;
        var query = eventView.query;
        var title = this.getDocumentTitle();
        return (<sentryDocumentTitle_1.default title={title} orgSlug={organization.slug}>
        <exports.StyledPageContent>
          <lightWeightNoProjectMessage_1.default organization={organization}>
            <resultsHeader_1.default errorCode={errorCode} organization={organization} location={location} eventView={eventView} onIncompatibleAlertQuery={this.handleIncompatibleQuery}/>
            <Layout.Body>
              {incompatibleAlertNotice && <exports.Top fullWidth>{incompatibleAlertNotice}</exports.Top>}
              <exports.Top fullWidth>
                {this.renderError(error)}
                <exports.StyledSearchBar searchSource="eventsv2" organization={organization} projectIds={eventView.project} query={query} fields={fields} onSearch={this.handleSearch} maxQueryLength={constants_1.MAX_QUERY_LENGTH}/>
                <resultsChart_1.default router={router} organization={organization} eventView={eventView} location={location} onAxisChange={this.handleYAxisChange} onDisplayChange={this.handleDisplayChange} total={totalValues} confirmedQuery={confirmedQuery}/>
              </exports.Top>
              <Layout.Main fullWidth={!showTags}>
                <table_1.default organization={organization} eventView={eventView} location={location} title={title} setError={this.setError} onChangeShowTags={this.handleChangeShowTags} showTags={showTags} confirmedQuery={confirmedQuery}/>
              </Layout.Main>
              {showTags ? this.renderTagsTable() : null}
              <confirm_1.default priority="primary" header={<strong>{locale_1.t('May lead to thumb twiddling')}</strong>} confirmText={locale_1.t('Do it')} cancelText={locale_1.t('Nevermind')} onConfirm={this.handleConfirmed} onCancel={this.handleCancelled} message={<p>
                    {locale_1.tct("You've created a query that will search for events made\n                      [dayLimit:over more than 30 days] for [projectLimit:more than 10 projects].\n                      A lot has happened during that time, so this might take awhile.\n                      Are you sure you want to do this?", {
                    dayLimit: <strong />,
                    projectLimit: <strong />,
                })}
                  </p>}>
                {this.setOpenFunction}
              </confirm_1.default>
            </Layout.Body>
          </lightWeightNoProjectMessage_1.default>
        </exports.StyledPageContent>
      </sentryDocumentTitle_1.default>);
    };
    return Results;
}(React.Component));
exports.StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
exports.StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
exports.Top = styled_1.default(Layout.Main)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex-grow: 0;\n"], ["\n  flex-grow: 0;\n"])));
var SavedQueryAPI = /** @class */ (function (_super) {
    tslib_1.__extends(SavedQueryAPI, _super);
    function SavedQueryAPI() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SavedQueryAPI.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        if (location.query.id) {
            return [
                [
                    'savedQuery',
                    "/organizations/" + organization.slug + "/discover/saved/" + location.query.id + "/",
                ],
            ];
        }
        return [];
    };
    SavedQueryAPI.prototype.renderLoading = function () {
        return this.renderBody();
    };
    SavedQueryAPI.prototype.renderBody = function () {
        var _a = this.state, savedQuery = _a.savedQuery, loading = _a.loading;
        return (<Results {...this.props} savedQuery={savedQuery !== null && savedQuery !== void 0 ? savedQuery : undefined} loading={loading}/>);
    };
    return SavedQueryAPI;
}(asyncComponent_1.default));
function ResultsContainer(props) {
    /**
     * Block `<Results>` from mounting until GSH is ready since there are API
     * requests being performed on mount.
     *
     * Also, we skip loading last used projects if you have multiple projects feature as
     * you no longer need to enforce a project if it is empty. We assume an empty project is
     * the desired behavior because saved queries can contain a project filter.
     */
    return (<globalSelectionHeader_1.default skipLoadLastUsed={props.organization.features.includes('global-views')}>
      <SavedQueryAPI {...props}/>
    </globalSelectionHeader_1.default>);
}
exports.default = withApi_1.default(withOrganization_1.default(withGlobalSelection_1.default(ResultsContainer)));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=results.jsx.map