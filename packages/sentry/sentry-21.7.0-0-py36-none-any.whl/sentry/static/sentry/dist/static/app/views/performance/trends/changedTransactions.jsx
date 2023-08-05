Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var styles_1 = require("app/components/charts/styles");
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var radio_1 = tslib_1.__importDefault(require("app/components/radio"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var formatters_1 = require("app/utils/formatters");
var trendsDiscoverQuery_1 = tslib_1.__importDefault(require("app/utils/performance/trends/trendsDiscoverQuery"));
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var radioGroup_1 = require("app/views/settings/components/forms/controls/radioGroup");
var charts_1 = require("../transactionSummary/charts");
var utils_1 = require("../transactionSummary/utils");
var chart_1 = tslib_1.__importDefault(require("./chart"));
var types_1 = require("./types");
var utils_2 = require("./utils");
function onTrendsCursor(trendChangeType) {
    return function onCursor(cursor, path, query, _direction) {
        var cursorQuery = {};
        if (trendChangeType === types_1.TrendChangeType.IMPROVED) {
            cursorQuery.improvedCursor = cursor;
        }
        else if (trendChangeType === types_1.TrendChangeType.REGRESSION) {
            cursorQuery.regressionCursor = cursor;
        }
        var selectedQueryKey = utils_2.getSelectedQueryKey(trendChangeType);
        delete query[selectedQueryKey];
        react_router_1.browserHistory.push({
            pathname: path,
            query: tslib_1.__assign(tslib_1.__assign({}, query), cursorQuery),
        });
    };
}
function getChartTitle(trendChangeType) {
    switch (trendChangeType) {
        case types_1.TrendChangeType.IMPROVED:
            return locale_1.t('Most Improved Transactions');
        case types_1.TrendChangeType.REGRESSION:
            return locale_1.t('Most Regressed Transactions');
        default:
            throw new Error('No trend type passed');
    }
}
function getSelectedTransaction(location, trendChangeType, transactions) {
    var queryKey = utils_2.getSelectedQueryKey(trendChangeType);
    var selectedTransactionName = queryString_1.decodeScalar(location.query[queryKey]);
    if (!transactions) {
        return undefined;
    }
    var selectedTransaction = transactions.find(function (transaction) {
        return transaction.transaction + "-" + transaction.project === selectedTransactionName;
    });
    if (selectedTransaction) {
        return selectedTransaction;
    }
    return transactions.length > 0 ? transactions[0] : undefined;
}
function handleChangeSelected(location, trendChangeType) {
    return function updateSelected(transaction) {
        var selectedQueryKey = utils_2.getSelectedQueryKey(trendChangeType);
        var query = tslib_1.__assign({}, location.query);
        if (!transaction) {
            delete query[selectedQueryKey];
        }
        else {
            query[selectedQueryKey] = transaction
                ? transaction.transaction + "-" + transaction.project
                : undefined;
        }
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: query,
        });
    };
}
var FilterSymbols;
(function (FilterSymbols) {
    FilterSymbols["GREATER_THAN_EQUALS"] = ">=";
    FilterSymbols["LESS_THAN_EQUALS"] = "<=";
})(FilterSymbols || (FilterSymbols = {}));
function handleFilterTransaction(location, transaction) {
    var queryString = queryString_1.decodeScalar(location.query.query);
    var conditions = tokenizeSearch_1.tokenizeSearch(queryString || '');
    conditions.addTagValues('!transaction', [transaction]);
    var query = conditions.formatString();
    react_router_1.browserHistory.push({
        pathname: location.pathname,
        query: tslib_1.__assign(tslib_1.__assign({}, location.query), { query: String(query).trim() }),
    });
}
function handleFilterDuration(location, value, symbol) {
    var durationTag = utils_2.getCurrentTrendParameter(location).column;
    var queryString = queryString_1.decodeScalar(location.query.query);
    var conditions = tokenizeSearch_1.tokenizeSearch(queryString || '');
    var existingValues = conditions.getTagValues(durationTag);
    var alternateSymbol = symbol === FilterSymbols.GREATER_THAN_EQUALS ? '>' : '<';
    if (existingValues) {
        existingValues.forEach(function (existingValue) {
            if (existingValue.startsWith(symbol) || existingValue.startsWith(alternateSymbol)) {
                conditions.removeTagValue(durationTag, existingValue);
            }
        });
    }
    conditions.addTagValues(durationTag, ["" + symbol + value]);
    var query = conditions.formatString();
    react_router_1.browserHistory.push({
        pathname: location.pathname,
        query: tslib_1.__assign(tslib_1.__assign({}, location.query), { query: String(query).trim() }),
    });
}
function ChangedTransactions(props) {
    var api = props.api, location = props.location, trendChangeType = props.trendChangeType, previousTrendFunction = props.previousTrendFunction, previousTrendColumn = props.previousTrendColumn, organization = props.organization, projects = props.projects, setError = props.setError;
    var trendView = props.trendView.clone();
    var chartTitle = getChartTitle(trendChangeType);
    utils_2.modifyTrendView(trendView, location, trendChangeType);
    var onCursor = onTrendsCursor(trendChangeType);
    var cursor = queryString_1.decodeScalar(location.query[utils_2.trendCursorNames[trendChangeType]]);
    return (<trendsDiscoverQuery_1.default eventView={trendView} orgSlug={organization.slug} location={location} trendChangeType={trendChangeType} cursor={cursor} limit={5} setError={setError}>
      {function (_a) {
            var isLoading = _a.isLoading, trendsData = _a.trendsData, pageLinks = _a.pageLinks;
            var trendFunction = utils_2.getCurrentTrendFunction(location);
            var trendParameter = utils_2.getCurrentTrendParameter(location);
            var events = utils_2.normalizeTrends((trendsData && trendsData.events && trendsData.events.data) || []);
            var selectedTransaction = getSelectedTransaction(location, trendChangeType, events);
            var statsData = (trendsData === null || trendsData === void 0 ? void 0 : trendsData.stats) || {};
            var transactionsList = events && events.slice ? events.slice(0, 5) : [];
            var currentTrendFunction = isLoading && previousTrendFunction
                ? previousTrendFunction
                : trendFunction.field;
            var currentTrendColumn = isLoading && previousTrendColumn ? previousTrendColumn : trendParameter.column;
            var titleTooltipContent = locale_1.t('This compares the baseline (%s) of the past with the present.', trendFunction.legendLabel);
            return (<TransactionsListContainer>
            <TrendsTransactionPanel>
              <StyledHeaderTitleLegend>
                {chartTitle}
                <questionTooltip_1.default size="sm" position="top" title={titleTooltipContent}/>
              </StyledHeaderTitleLegend>
              {isLoading ? (<loadingIndicator_1.default style={{
                        margin: '237px auto',
                    }}/>) : (<react_1.Fragment>
                  {transactionsList.length ? (<react_1.Fragment>
                      <ChartContainer>
                        <chart_1.default statsData={statsData} query={trendView.query} project={trendView.project} environment={trendView.environment} start={trendView.start} end={trendView.end} statsPeriod={trendView.statsPeriod} transaction={selectedTransaction} isLoading={isLoading} {...props}/>
                      </ChartContainer>
                      {transactionsList.map(function (transaction, index) { return (<TrendsListItem api={api} currentTrendFunction={currentTrendFunction} currentTrendColumn={currentTrendColumn} trendView={props.trendView} organization={organization} transaction={transaction} key={transaction.transaction} index={index} trendChangeType={trendChangeType} transactions={transactionsList} location={location} projects={projects} statsData={statsData} handleSelectTransaction={handleChangeSelected(location, trendChangeType)}/>); })}
                    </react_1.Fragment>) : (<StyledEmptyStateWarning small>
                      {locale_1.t('No results')}
                    </StyledEmptyStateWarning>)}
                </react_1.Fragment>)}
            </TrendsTransactionPanel>
            <pagination_1.default pageLinks={pageLinks} onCursor={onCursor}/>
          </TransactionsListContainer>);
        }}
    </trendsDiscoverQuery_1.default>);
}
function TrendsListItem(props) {
    var transaction = props.transaction, transactions = props.transactions, trendChangeType = props.trendChangeType, currentTrendFunction = props.currentTrendFunction, currentTrendColumn = props.currentTrendColumn, index = props.index, location = props.location, projects = props.projects, handleSelectTransaction = props.handleSelectTransaction;
    var color = utils_2.trendToColor[trendChangeType].default;
    var selectedTransaction = getSelectedTransaction(location, trendChangeType, transactions);
    var isSelected = selectedTransaction === transaction;
    var project = projects.find(function (_a) {
        var slug = _a.slug;
        return slug === transaction.project;
    });
    var currentPeriodValue = transaction.aggregate_range_2;
    var previousPeriodValue = transaction.aggregate_range_1;
    var absolutePercentChange = formatters_1.formatPercentage(Math.abs(transaction.trend_percentage - 1), 0);
    var previousDuration = formatters_1.getDuration(previousPeriodValue / 1000, previousPeriodValue < 1000 && previousPeriodValue > 10 ? 0 : 2);
    var currentDuration = formatters_1.getDuration(currentPeriodValue / 1000, currentPeriodValue < 1000 && currentPeriodValue > 10 ? 0 : 2);
    var percentChangeExplanation = locale_1.t('Over this period, the %s for %s has %s %s from %s to %s', currentTrendFunction, currentTrendColumn, trendChangeType === types_1.TrendChangeType.IMPROVED ? locale_1.t('decreased') : locale_1.t('increased'), absolutePercentChange, previousDuration, currentDuration);
    var longestPeriodValue = trendChangeType === types_1.TrendChangeType.IMPROVED
        ? previousPeriodValue
        : currentPeriodValue;
    var longestDuration = trendChangeType === types_1.TrendChangeType.IMPROVED ? previousDuration : currentDuration;
    return (<ListItemContainer data-test-id={'trends-list-item-' + trendChangeType}>
      <ItemRadioContainer color={color}>
        <tooltip_1.default title={<TooltipContent>
              <span>{locale_1.t('Total Events')}</span>
              <span>
                <count_1.default value={transaction.count_range_1}/>
                <utils_2.StyledIconArrow direction="right" size="xs"/>
                <count_1.default value={transaction.count_range_2}/>
              </span>
            </TooltipContent>}>
          <radioGroup_1.RadioLineItem index={index} role="radio">
            <radio_1.default checked={isSelected} onChange={function () { return handleSelectTransaction(transaction); }}/>
          </radioGroup_1.RadioLineItem>
        </tooltip_1.default>
      </ItemRadioContainer>
      <TransactionSummaryLink {...props}/>
      <ItemTransactionPercentage>
        <tooltip_1.default title={percentChangeExplanation}>
          <react_1.Fragment>
            {trendChangeType === types_1.TrendChangeType.REGRESSION ? '+' : ''}
            {formatters_1.formatPercentage(transaction.trend_percentage - 1, 0)}
          </react_1.Fragment>
        </tooltip_1.default>
      </ItemTransactionPercentage>
      <dropdownLink_1.default caret={false} anchorRight title={<StyledButton size="xsmall" icon={<icons_1.IconEllipsis data-test-id="trends-item-action" size="xs"/>}/>}>
        <menuItem_1.default onClick={function () {
            return handleFilterDuration(location, longestPeriodValue, FilterSymbols.LESS_THAN_EQUALS);
        }}>
          <StyledMenuAction>{locale_1.t('Show \u2264 %s', longestDuration)}</StyledMenuAction>
        </menuItem_1.default>
        <menuItem_1.default onClick={function () {
            return handleFilterDuration(location, longestPeriodValue, FilterSymbols.GREATER_THAN_EQUALS);
        }}>
          <StyledMenuAction>{locale_1.t('Show \u2265 %s', longestDuration)}</StyledMenuAction>
        </menuItem_1.default>
        <menuItem_1.default onClick={function () { return handleFilterTransaction(location, transaction.transaction); }}>
          <StyledMenuAction>{locale_1.t('Hide from list')}</StyledMenuAction>
        </menuItem_1.default>
      </dropdownLink_1.default>
      <ItemTransactionDurationChange>
        {project && (<tooltip_1.default title={transaction.project}>
            <idBadge_1.default avatarSize={16} project={project} hideName/>
          </tooltip_1.default>)}
        <CompareDurations {...props}/>
      </ItemTransactionDurationChange>
      <ItemTransactionStatus color={color}>
        <react_1.Fragment>
          {utils_2.transformValueDelta(transaction.trend_difference, trendChangeType)}
        </react_1.Fragment>
      </ItemTransactionStatus>
    </ListItemContainer>);
}
var CompareDurations = function (props) {
    var transaction = props.transaction;
    return (<DurationChange>
      {utils_2.transformDeltaSpread(transaction.aggregate_range_1, transaction.aggregate_range_2)}
    </DurationChange>);
};
var TransactionSummaryLink = function (props) {
    var organization = props.organization, eventView = props.trendView, transaction = props.transaction, projects = props.projects, currentTrendFunction = props.currentTrendFunction, currentTrendColumn = props.currentTrendColumn;
    var summaryView = eventView.clone();
    var projectID = utils_2.getTrendProjectId(transaction, projects);
    var target = utils_1.transactionSummaryRouteWithQuery({
        orgSlug: organization.slug,
        transaction: String(transaction.transaction),
        query: summaryView.generateQueryStringObject(),
        projectID: projectID,
        display: charts_1.DisplayModes.TREND,
        trendFunction: currentTrendFunction,
        trendColumn: currentTrendColumn,
    });
    return <ItemTransactionName to={target}>{transaction.transaction}</ItemTransactionName>;
};
var TransactionsListContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var TrendsTransactionPanel = styled_1.default(panels_1.Panel)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n  flex-grow: 1;\n"], ["\n  margin: 0;\n  flex-grow: 1;\n"])));
var ChartContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space_1.default(3));
var StyledHeaderTitleLegend = styled_1.default(styles_1.HeaderTitleLegend)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  border-radius: ", ";\n  padding: ", " ", ";\n"], ["\n  border-radius: ", ";\n  padding: ", " ", ";\n"])), function (p) { return p.theme.borderRadius; }, space_1.default(2), space_1.default(3));
var StyledButton = styled_1.default(button_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  vertical-align: middle;\n"], ["\n  vertical-align: middle;\n"])));
var StyledMenuAction = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n  color: ", ";\n"], ["\n  white-space: nowrap;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var StyledEmptyStateWarning = styled_1.default(emptyStateWarning_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  min-height: 300px;\n  justify-content: center;\n"], ["\n  min-height: 300px;\n  justify-content: center;\n"])));
var ListItemContainer = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 24px auto 100px 30px;\n  grid-template-rows: repeat(2, auto);\n  grid-column-gap: ", ";\n  border-top: 1px solid ", ";\n  padding: ", " ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 24px auto 100px 30px;\n  grid-template-rows: repeat(2, auto);\n  grid-column-gap: ", ";\n  border-top: 1px solid ", ";\n  padding: ", " ", ";\n"])), space_1.default(1), function (p) { return p.theme.border; }, space_1.default(1), space_1.default(2));
var ItemRadioContainer = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  grid-row: 1/3;\n  input {\n    cursor: pointer;\n  }\n  input:checked::after {\n    background-color: ", ";\n  }\n"], ["\n  grid-row: 1/3;\n  input {\n    cursor: pointer;\n  }\n  input:checked::after {\n    background-color: ", ";\n  }\n"])), function (p) { return p.color; });
var ItemTransactionName = styled_1.default(link_1.default)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-right: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  margin-right: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(1), overflowEllipsis_1.default);
var ItemTransactionDurationChange = styled_1.default('div')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  font-size: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
var DurationChange = styled_1.default('span')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin: 0 ", ";\n"], ["\n  color: ", ";\n  margin: 0 ", ";\n"])), function (p) { return p.theme.gray300; }, space_1.default(1));
var ItemTransactionPercentage = styled_1.default('div')(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n  font-size: ", ";\n"], ["\n  text-align: right;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var ItemTransactionStatus = styled_1.default('div')(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  text-align: right;\n  font-size: ", ";\n"], ["\n  color: ", ";\n  text-align: right;\n  font-size: ", ";\n"])), function (p) { return p.color; }, function (p) { return p.theme.fontSizeSmall; });
var TooltipContent = styled_1.default('div')(templateObject_15 || (templateObject_15 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"])));
exports.default = withApi_1.default(withProjects_1.default(withOrganization_1.default(ChangedTransactions)));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15;
//# sourceMappingURL=changedTransactions.jsx.map