Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var breakdownBars_1 = tslib_1.__importDefault(require("app/components/charts/breakdownBars"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var styles_1 = require("app/components/charts/styles");
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var discoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/discoverQuery"));
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var data_1 = require("app/views/performance/data");
function StatusBreakdown(_a) {
    var eventView = _a.eventView, location = _a.location, organization = _a.organization;
    var breakdownView = eventView
        .withColumns([
        { kind: 'function', function: ['count', '', '', undefined] },
        { kind: 'field', field: 'transaction.status' },
    ])
        .withSorts([{ kind: 'desc', field: 'count' }]);
    return (<react_1.Fragment>
      <styles_1.SectionHeading>
        {locale_1.t('Status Breakdown')}
        <questionTooltip_1.default position="top" title={data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.STATUS_BREAKDOWN)} size="sm"/>
      </styles_1.SectionHeading>
      <discoverQuery_1.default eventView={breakdownView} location={location} orgSlug={organization.slug} referrer="api.performance.status-breakdown">
        {function (_a) {
            var isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData;
            if (isLoading) {
                return <placeholder_1.default height="124px"/>;
            }
            if (error) {
                return (<errorPanel_1.default height="124px">
                <icons_1.IconWarning color="gray300" size="lg"/>
              </errorPanel_1.default>);
            }
            if (!tableData || tableData.data.length === 0) {
                return (<EmptyStatusBreakdown small>{locale_1.t('No statuses found')}</EmptyStatusBreakdown>);
            }
            var points = tableData.data.map(function (row) { return ({
                label: String(row['transaction.status']),
                value: parseInt(String(row.count), 10),
                onClick: function () {
                    var query = tokenizeSearch_1.tokenizeSearch(eventView.query);
                    query
                        .removeTag('!transaction.status')
                        .setTagValues('transaction.status', [row['transaction.status']]);
                    react_router_1.browserHistory.push({
                        pathname: location.pathname,
                        query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, query: query.formatString() }),
                    });
                },
            }); });
            return <breakdownBars_1.default data={points}/>;
        }}
      </discoverQuery_1.default>
    </react_1.Fragment>);
}
var EmptyStatusBreakdown = styled_1.default(emptyStateWarning_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  height: 124px;\n  padding: 50px 15%;\n"], ["\n  height: 124px;\n  padding: 50px 15%;\n"])));
exports.default = StatusBreakdown;
var templateObject_1;
//# sourceMappingURL=statusBreakdown.jsx.map