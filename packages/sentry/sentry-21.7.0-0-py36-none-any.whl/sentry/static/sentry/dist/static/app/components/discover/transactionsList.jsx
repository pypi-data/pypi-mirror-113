Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var discoverButton_1 = tslib_1.__importDefault(require("app/components/discoverButton"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var discoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/discoverQuery"));
var baselineQuery_1 = tslib_1.__importDefault(require("app/utils/performance/baseline/baselineQuery"));
var trendsDiscoverQuery_1 = require("app/utils/performance/trends/trendsDiscoverQuery");
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var utils_1 = require("app/views/eventsV2/utils");
var utils_2 = require("app/views/performance/transactionSummary/transactionEvents/utils");
var transactionsTable_1 = tslib_1.__importDefault(require("./transactionsTable"));
var DEFAULT_TRANSACTION_LIMIT = 5;
var TransactionsList = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionsList, _super);
    function TransactionsList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleCursor = function (cursor, pathname, query) {
            var _a;
            var cursorName = _this.props.cursorName;
            react_router_1.browserHistory.push({
                pathname: pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, query), (_a = {}, _a[cursorName] = cursor, _a)),
            });
        };
        return _this;
    }
    TransactionsList.prototype.getEventView = function () {
        var _a = this.props, eventView = _a.eventView, selected = _a.selected;
        var sortedEventView = eventView.withSorts([selected.sort]);
        if (selected.query) {
            var query_1 = tokenizeSearch_1.tokenizeSearch(sortedEventView.query);
            selected.query.forEach(function (item) { return query_1.setTagValues(item[0], [item[1]]); });
            sortedEventView.query = query_1.formatString();
        }
        return sortedEventView;
    };
    TransactionsList.prototype.generateDiscoverEventView = function () {
        var generateDiscoverEventView = this.props.generateDiscoverEventView;
        if (typeof generateDiscoverEventView === 'function') {
            return generateDiscoverEventView();
        }
        return this.getEventView();
    };
    TransactionsList.prototype.generatePerformanceTransactionEventsView = function () {
        var _a;
        var generatePerformanceTransactionEventsView = this.props.generatePerformanceTransactionEventsView;
        return (_a = generatePerformanceTransactionEventsView === null || generatePerformanceTransactionEventsView === void 0 ? void 0 : generatePerformanceTransactionEventsView()) !== null && _a !== void 0 ? _a : this.getEventView();
    };
    TransactionsList.prototype.renderHeader = function () {
        var _a = this.props, organization = _a.organization, selected = _a.selected, options = _a.options, handleDropdownChange = _a.handleDropdownChange, handleOpenAllEventsClick = _a.handleOpenAllEventsClick, handleOpenInDiscoverClick = _a.handleOpenInDiscoverClick, showTransactions = _a.showTransactions, breakdown = _a.breakdown;
        return (<React.Fragment>
        <div>
          <dropdownControl_1.default data-test-id="filter-transactions" button={function (_a) {
                var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
                return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} prefix={locale_1.t('Filter')} size="small">
                {selected.label}
              </StyledDropdownButton>);
            }}>
            {options.map(function (_a) {
                var value = _a.value, label = _a.label;
                return (<dropdownControl_1.DropdownItem data-test-id={"option-" + value} key={value} onSelect={handleDropdownChange} eventKey={value} isActive={value === selected.value}>
                {label}
              </dropdownControl_1.DropdownItem>);
            })}
          </dropdownControl_1.default>
        </div>
        {!this.isTrend() &&
                (handleOpenAllEventsClick ? (<guideAnchor_1.default target="release_transactions_open_in_transaction_events">
              <button_1.default onClick={handleOpenAllEventsClick} to={this.generatePerformanceTransactionEventsView().getPerformanceTransactionEventsViewUrlTarget(organization.slug, {
                        showTransactions: utils_2.mapShowTransactionToPercentile(showTransactions),
                        breakdown: breakdown,
                    })} size="small" data-test-id="transaction-events-open">
                {locale_1.t('View All Events')}
              </button_1.default>
            </guideAnchor_1.default>) : (<guideAnchor_1.default target="release_transactions_open_in_discover">
              <discoverButton_1.default onClick={handleOpenInDiscoverClick} to={this.generateDiscoverEventView().getResultsViewUrlTarget(organization.slug)} size="small" data-test-id="discover-open">
                {locale_1.t('Open in Discover')}
              </discoverButton_1.default>
            </guideAnchor_1.default>))}
      </React.Fragment>);
    };
    TransactionsList.prototype.renderTransactionTable = function () {
        var _this = this;
        var _a;
        var _b = this.props, location = _b.location, organization = _b.organization, handleCellAction = _b.handleCellAction, cursorName = _b.cursorName, limit = _b.limit, titles = _b.titles, generateLink = _b.generateLink, baseline = _b.baseline, forceLoading = _b.forceLoading;
        var eventView = this.getEventView();
        var columnOrder = eventView.getColumns();
        var cursor = queryString_1.decodeScalar((_a = location.query) === null || _a === void 0 ? void 0 : _a[cursorName]);
        var baselineTransactionName = organization.features.includes('transaction-comparison')
            ? baseline !== null && baseline !== void 0 ? baseline : null
            : null;
        var tableRenderer = function (_a) {
            var isLoading = _a.isLoading, pageLinks = _a.pageLinks, tableData = _a.tableData, baselineData = _a.baselineData;
            return (<React.Fragment>
        <Header>
          {_this.renderHeader()}
          <StyledPagination pageLinks={pageLinks} onCursor={_this.handleCursor} size="small"/>
        </Header>
        <transactionsTable_1.default eventView={eventView} organization={organization} location={location} isLoading={isLoading} tableData={tableData} baselineData={baselineData !== null && baselineData !== void 0 ? baselineData : null} columnOrder={columnOrder} titles={titles} generateLink={generateLink} baselineTransactionName={baselineTransactionName} handleCellAction={handleCellAction}/>
      </React.Fragment>);
        };
        if (forceLoading) {
            return tableRenderer({
                isLoading: true,
                pageLinks: null,
                tableData: null,
                baselineData: null,
            });
        }
        if (baselineTransactionName) {
            var orgTableRenderer_1 = tableRenderer;
            tableRenderer = function (_a) {
                var isLoading = _a.isLoading, pageLinks = _a.pageLinks, tableData = _a.tableData;
                return (<baselineQuery_1.default eventView={eventView} orgSlug={organization.slug}>
          {function (baselineQueryProps) {
                        return orgTableRenderer_1({
                            isLoading: isLoading || baselineQueryProps.isLoading,
                            pageLinks: pageLinks,
                            tableData: tableData,
                            baselineData: baselineQueryProps.results,
                        });
                    }}
        </baselineQuery_1.default>);
            };
        }
        return (<discoverQuery_1.default location={location} eventView={eventView} orgSlug={organization.slug} limit={limit} cursor={cursor} referrer="api.discover.transactions-list">
        {tableRenderer}
      </discoverQuery_1.default>);
    };
    TransactionsList.prototype.renderTrendsTable = function () {
        var _this = this;
        var _a;
        var _b = this.props, trendView = _b.trendView, location = _b.location, selected = _b.selected, organization = _b.organization, cursorName = _b.cursorName, generateLink = _b.generateLink;
        var sortedEventView = trendView.clone();
        sortedEventView.sorts = [selected.sort];
        sortedEventView.trendType = selected.trendType;
        if (selected.query) {
            var query_2 = tokenizeSearch_1.tokenizeSearch(sortedEventView.query);
            selected.query.forEach(function (item) { return query_2.setTagValues(item[0], [item[1]]); });
            sortedEventView.query = query_2.formatString();
        }
        var cursor = queryString_1.decodeScalar((_a = location.query) === null || _a === void 0 ? void 0 : _a[cursorName]);
        return (<trendsDiscoverQuery_1.TrendsEventsDiscoverQuery eventView={sortedEventView} orgSlug={organization.slug} location={location} cursor={cursor} limit={5}>
        {function (_a) {
                var isLoading = _a.isLoading, trendsData = _a.trendsData, pageLinks = _a.pageLinks;
                return (<React.Fragment>
            <Header>
              {_this.renderHeader()}
              <StyledPagination pageLinks={pageLinks} onCursor={_this.handleCursor} size="small"/>
            </Header>
            <transactionsTable_1.default eventView={sortedEventView} organization={organization} location={location} isLoading={isLoading} tableData={trendsData} baselineData={null} titles={['transaction', 'percentage', 'difference']} columnOrder={utils_1.decodeColumnOrder([
                        { field: 'transaction' },
                        { field: 'trend_percentage()' },
                        { field: 'trend_difference()' },
                    ])} generateLink={generateLink} baselineTransactionName={null}/>
          </React.Fragment>);
            }}
      </trendsDiscoverQuery_1.TrendsEventsDiscoverQuery>);
    };
    TransactionsList.prototype.isTrend = function () {
        var selected = this.props.selected;
        return selected.trendType !== undefined;
    };
    TransactionsList.prototype.render = function () {
        return (<React.Fragment>
        {this.isTrend() ? this.renderTrendsTable() : this.renderTransactionTable()}
      </React.Fragment>);
    };
    TransactionsList.defaultProps = {
        cursorName: 'transactionCursor',
        limit: DEFAULT_TRANSACTION_LIMIT,
    };
    return TransactionsList;
}(React.Component));
var Header = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr auto auto;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr auto auto;\n  margin-bottom: ", ";\n"])), space_1.default(1));
var StyledDropdownButton = styled_1.default(dropdownButton_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  min-width: 145px;\n"], ["\n  min-width: 145px;\n"])));
var StyledPagination = styled_1.default(pagination_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin: 0 0 0 ", ";\n"], ["\n  margin: 0 0 0 ", ";\n"])), space_1.default(1));
exports.default = TransactionsList;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=transactionsList.jsx.map