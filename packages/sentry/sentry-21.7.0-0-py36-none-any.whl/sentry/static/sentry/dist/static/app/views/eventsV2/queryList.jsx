Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var globalSelection_1 = require("app/actionCreators/globalSelection");
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var parseLinkHeader_1 = tslib_1.__importDefault(require("app/utils/parseLinkHeader"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var utils_1 = require("./savedQuery/utils");
var miniGraph_1 = tslib_1.__importDefault(require("./miniGraph"));
var querycard_1 = tslib_1.__importDefault(require("./querycard"));
var utils_2 = require("./utils");
var QueryList = /** @class */ (function (_super) {
    tslib_1.__extends(QueryList, _super);
    function QueryList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDeleteQuery = function (eventView) { return function (event) {
            event.preventDefault();
            event.stopPropagation();
            var _a = _this.props, api = _a.api, organization = _a.organization, onQueryChange = _a.onQueryChange, location = _a.location, savedQueries = _a.savedQueries;
            utils_1.handleDeleteQuery(api, organization, eventView).then(function () {
                if (savedQueries.length === 1 && location.query.cursor) {
                    react_router_1.browserHistory.push({
                        pathname: location.pathname,
                        query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined }),
                    });
                }
                else {
                    onQueryChange();
                }
            });
        }; };
        _this.handleDuplicateQuery = function (eventView) { return function (event) {
            event.preventDefault();
            event.stopPropagation();
            var _a = _this.props, api = _a.api, location = _a.location, organization = _a.organization, onQueryChange = _a.onQueryChange;
            eventView = eventView.clone();
            eventView.name = eventView.name + " copy";
            utils_1.handleCreateQuery(api, organization, eventView).then(function () {
                onQueryChange();
                react_router_1.browserHistory.push({
                    pathname: location.pathname,
                    query: {},
                });
            });
        }; };
        return _this;
    }
    QueryList.prototype.componentDidMount = function () {
        /**
         * We need to reset global selection here because the saved queries can define their own projects
         * in the query. This can lead to mismatched queries for the project
         */
        globalSelection_1.resetGlobalSelection();
    };
    QueryList.prototype.renderQueries = function () {
        var _a = this.props, pageLinks = _a.pageLinks, renderPrebuilt = _a.renderPrebuilt;
        var links = parseLinkHeader_1.default(pageLinks || '');
        var cards = [];
        // If we're on the first page (no-previous page exists)
        // include the pre-built queries.
        if (renderPrebuilt && (!links.previous || links.previous.results === false)) {
            cards = cards.concat(this.renderPrebuiltQueries());
        }
        cards = cards.concat(this.renderSavedQueries());
        if (cards.filter(function (x) { return x; }).length === 0) {
            return (<StyledEmptyStateWarning>
          <p>{locale_1.t('No saved queries match that filter')}</p>
        </StyledEmptyStateWarning>);
        }
        return cards;
    };
    QueryList.prototype.renderPrebuiltQueries = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, savedQuerySearchQuery = _a.savedQuerySearchQuery;
        var views = utils_2.getPrebuiltQueries(organization);
        var hasSearchQuery = typeof savedQuerySearchQuery === 'string' && savedQuerySearchQuery.length > 0;
        var needleSearch = hasSearchQuery ? savedQuerySearchQuery.toLowerCase() : '';
        var list = views.map(function (view, index) {
            var eventView = eventView_1.default.fromNewQueryWithLocation(view, location);
            // if a search is performed on the list of queries, we filter
            // on the pre-built queries
            if (hasSearchQuery &&
                eventView.name &&
                !eventView.name.toLowerCase().includes(needleSearch)) {
                return null;
            }
            var recentTimeline = locale_1.t('Last ') + eventView.statsPeriod;
            var customTimeline = moment_1.default(eventView.start).format('MMM D, YYYY h:mm A') +
                ' - ' +
                moment_1.default(eventView.end).format('MMM D, YYYY h:mm A');
            var to = eventView.getResultsViewUrlTarget(organization.slug);
            return (<querycard_1.default key={index + "-" + eventView.name} to={to} title={eventView.name} subtitle={eventView.statsPeriod ? recentTimeline : customTimeline} queryDetail={eventView.query} createdBy={eventView.createdBy} renderGraph={function () { return (<miniGraph_1.default location={location} eventView={eventView} organization={organization}/>); }} onEventClick={function () {
                    analytics_1.trackAnalyticsEvent({
                        eventKey: 'discover_v2.prebuilt_query_click',
                        eventName: 'Discoverv2: Click a pre-built query',
                        organization_id: parseInt(_this.props.organization.id, 10),
                        query_name: eventView.name,
                    });
                }}/>);
        });
        return list;
    };
    QueryList.prototype.renderSavedQueries = function () {
        var _this = this;
        var _a = this.props, savedQueries = _a.savedQueries, location = _a.location, organization = _a.organization;
        if (!savedQueries || !Array.isArray(savedQueries) || savedQueries.length === 0) {
            return [];
        }
        return savedQueries.map(function (savedQuery, index) {
            var eventView = eventView_1.default.fromSavedQuery(savedQuery);
            var recentTimeline = locale_1.t('Last ') + eventView.statsPeriod;
            var customTimeline = moment_1.default(eventView.start).format('MMM D, YYYY h:mm A') +
                ' - ' +
                moment_1.default(eventView.end).format('MMM D, YYYY h:mm A');
            var to = eventView.getResultsViewShortUrlTarget(organization.slug);
            var dateStatus = <timeSince_1.default date={savedQuery.dateUpdated}/>;
            return (<querycard_1.default key={index + "-" + eventView.id} to={to} title={eventView.name} subtitle={eventView.statsPeriod ? recentTimeline : customTimeline} queryDetail={eventView.query} createdBy={eventView.createdBy} dateStatus={dateStatus} onEventClick={function () {
                    analytics_1.trackAnalyticsEvent({
                        eventKey: 'discover_v2.saved_query_click',
                        eventName: 'Discoverv2: Click a saved query',
                        organization_id: parseInt(_this.props.organization.id, 10),
                    });
                }} renderGraph={function () { return (<miniGraph_1.default location={location} eventView={eventView} organization={organization}/>); }} renderContextMenu={function () { return (<ContextMenu>
              <menuItem_1.default data-test-id="delete-query" onClick={_this.handleDeleteQuery(eventView)}>
                {locale_1.t('Delete Query')}
              </menuItem_1.default>
              <menuItem_1.default data-test-id="duplicate-query" onClick={_this.handleDuplicateQuery(eventView)}>
                {locale_1.t('Duplicate Query')}
              </menuItem_1.default>
            </ContextMenu>); }}/>);
        });
    };
    QueryList.prototype.render = function () {
        var pageLinks = this.props.pageLinks;
        return (<React.Fragment>
        <QueryGrid>{this.renderQueries()}</QueryGrid>
        <PaginationRow pageLinks={pageLinks} onCursor={function (cursor, path, query, direction) {
                var offset = Number(cursor.split(':')[1]);
                var newQuery = tslib_1.__assign(tslib_1.__assign({}, query), { cursor: cursor });
                var isPrevious = direction === -1;
                if (offset <= 0 && isPrevious) {
                    delete newQuery.cursor;
                }
                react_router_1.browserHistory.push({
                    pathname: path,
                    query: newQuery,
                });
            }}/>
      </React.Fragment>);
    };
    return QueryList;
}(React.Component));
var PaginationRow = styled_1.default(pagination_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 20px;\n"], ["\n  margin-bottom: 20px;\n"])));
var QueryGrid = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; });
var ContextMenu = function (_a) {
    var children = _a.children;
    return (<dropdownMenu_1.default>
    {function (_a) {
            var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
            var topLevelCx = classnames_1.default('dropdown', {
                'anchor-right': true,
                open: isOpen,
            });
            return (<MoreOptions {...getRootProps({
                className: topLevelCx,
            })}>
          <DropdownTarget {...getActorProps({
                onClick: function (event) {
                    event.stopPropagation();
                    event.preventDefault();
                },
            })}>
            <icons_1.IconEllipsis data-test-id="context-menu" size="md"/>
          </DropdownTarget>
          {isOpen && (<ul {...getMenuProps({})} className={classnames_1.default('dropdown-menu')}>
              {children}
            </ul>)}
        </MoreOptions>);
        }}
  </dropdownMenu_1.default>);
};
var MoreOptions = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  color: ", ";\n"], ["\n  display: flex;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var DropdownTarget = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledEmptyStateWarning = styled_1.default(emptyStateWarning_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  grid-column: 1 / 4;\n"], ["\n  grid-column: 1 / 4;\n"])));
exports.default = withApi_1.default(QueryList);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=queryList.jsx.map