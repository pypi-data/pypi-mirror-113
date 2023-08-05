Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupEvents = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var eventsTable_1 = tslib_1.__importDefault(require("app/components/eventsTable/eventsTable"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var locale_1 = require("app/locale");
var parseApiError_1 = tslib_1.__importDefault(require("app/utils/parseApiError"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var GroupEvents = /** @class */ (function (_super) {
    tslib_1.__extends(GroupEvents, _super);
    function GroupEvents(props) {
        var _this = _super.call(this, props) || this;
        _this.handleSearch = function (query) {
            var targetQueryParams = tslib_1.__assign({}, _this.props.location.query);
            targetQueryParams.query = query;
            var _a = _this.props.params, groupId = _a.groupId, orgId = _a.orgId;
            react_router_1.browserHistory.push({
                pathname: "/organizations/" + orgId + "/issues/" + groupId + "/events/",
                query: targetQueryParams,
            });
        };
        _this.fetchData = function () {
            _this.setState({
                loading: true,
                error: false,
            });
            var query = tslib_1.__assign(tslib_1.__assign({}, pick_1.default(_this.props.location.query, ['cursor', 'environment'])), { limit: 50, query: _this.state.query });
            _this.props.api.request("/issues/" + _this.props.params.groupId + "/events/", {
                query: query,
                method: 'GET',
                success: function (data, _, jqXHR) {
                    var _a;
                    _this.setState({
                        eventList: data,
                        error: false,
                        loading: false,
                        pageLinks: (_a = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : '',
                    });
                },
                error: function (err) {
                    _this.setState({
                        error: parseApiError_1.default(err),
                        loading: false,
                    });
                },
            });
        };
        var queryParams = _this.props.location.query;
        _this.state = {
            eventList: [],
            loading: true,
            error: false,
            pageLinks: '',
            query: queryParams.query || '',
        };
        return _this;
    }
    GroupEvents.prototype.UNSAFE_componentWillMount = function () {
        this.fetchData();
    };
    GroupEvents.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (this.props.location.search !== nextProps.location.search) {
            var queryParams = nextProps.location.query;
            this.setState({
                query: queryParams.query,
            }, this.fetchData);
        }
    };
    GroupEvents.prototype.renderNoQueryResults = function () {
        return (<emptyStateWarning_1.default>
        <p>{locale_1.t('Sorry, no events match your search query.')}</p>
      </emptyStateWarning_1.default>);
    };
    GroupEvents.prototype.renderEmpty = function () {
        return (<emptyStateWarning_1.default>
        <p>{locale_1.t("There don't seem to be any events yet.")}</p>
      </emptyStateWarning_1.default>);
    };
    GroupEvents.prototype.renderResults = function () {
        var _a = this.props, group = _a.group, params = _a.params;
        var tagList = group.tags.filter(function (tag) { return tag.key !== 'user'; }) || [];
        return (<eventsTable_1.default tagList={tagList} events={this.state.eventList} orgId={params.orgId} projectId={group.project.slug} groupId={params.groupId}/>);
    };
    GroupEvents.prototype.renderBody = function () {
        var body;
        if (this.state.loading) {
            body = <loadingIndicator_1.default />;
        }
        else if (this.state.error) {
            body = <loadingError_1.default message={this.state.error} onRetry={this.fetchData}/>;
        }
        else if (this.state.eventList.length > 0) {
            body = this.renderResults();
        }
        else if (this.state.query && this.state.query !== '') {
            body = this.renderNoQueryResults();
        }
        else {
            body = this.renderEmpty();
        }
        return body;
    };
    GroupEvents.prototype.render = function () {
        return (<div>
        <div style={{ marginBottom: 20 }}>
          <searchBar_1.default defaultQuery="" placeholder={locale_1.t('search event id, message, or tags')} query={this.state.query} onSearch={this.handleSearch}/>
        </div>
        <panels_1.Panel className="event-list">
          <panels_1.PanelBody>{this.renderBody()}</panels_1.PanelBody>
        </panels_1.Panel>
        <pagination_1.default pageLinks={this.state.pageLinks}/>
      </div>);
    };
    return GroupEvents;
}(React.Component));
exports.GroupEvents = GroupEvents;
exports.default = withApi_1.default(GroupEvents);
//# sourceMappingURL=groupEvents.jsx.map