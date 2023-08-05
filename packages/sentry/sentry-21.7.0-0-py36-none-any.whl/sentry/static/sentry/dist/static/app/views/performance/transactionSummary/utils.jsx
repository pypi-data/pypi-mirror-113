Object.defineProperty(exports, "__esModule", { value: true });
exports.SidebarSpacer = exports.generateTransactionLink = exports.generateTraceLink = exports.transactionSummaryRouteWithQuery = exports.generateTransactionSummaryRoute = exports.TransactionFilterOptions = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var urls_1 = require("app/utils/discover/urls");
var utils_1 = require("app/views/performance/traceDetails/utils");
var utils_2 = require("../utils");
var TransactionFilterOptions;
(function (TransactionFilterOptions) {
    TransactionFilterOptions["FASTEST"] = "fastest";
    TransactionFilterOptions["SLOW"] = "slow";
    TransactionFilterOptions["OUTLIER"] = "outlier";
    TransactionFilterOptions["RECENT"] = "recent";
})(TransactionFilterOptions = exports.TransactionFilterOptions || (exports.TransactionFilterOptions = {}));
function generateTransactionSummaryRoute(_a) {
    var orgSlug = _a.orgSlug;
    return "/organizations/" + orgSlug + "/performance/summary/";
}
exports.generateTransactionSummaryRoute = generateTransactionSummaryRoute;
function transactionSummaryRouteWithQuery(_a) {
    var orgSlug = _a.orgSlug, transaction = _a.transaction, projectID = _a.projectID, query = _a.query, _b = _a.unselectedSeries, unselectedSeries = _b === void 0 ? 'p100()' : _b, display = _a.display, trendFunction = _a.trendFunction, trendColumn = _a.trendColumn, showTransactions = _a.showTransactions;
    var pathname = generateTransactionSummaryRoute({
        orgSlug: orgSlug,
    });
    return {
        pathname: pathname,
        query: {
            transaction: transaction,
            project: projectID,
            environment: query.environment,
            statsPeriod: query.statsPeriod,
            start: query.start,
            end: query.end,
            query: query.query,
            unselectedSeries: unselectedSeries,
            showTransactions: showTransactions,
            display: display,
            trendFunction: trendFunction,
            trendColumn: trendColumn,
        },
    };
}
exports.transactionSummaryRouteWithQuery = transactionSummaryRouteWithQuery;
function generateTraceLink(dateSelection) {
    return function (organization, tableRow, _query) {
        var traceId = "" + tableRow.trace;
        if (!traceId) {
            return {};
        }
        return utils_1.getTraceDetailsUrl(organization, traceId, dateSelection, {});
    };
}
exports.generateTraceLink = generateTraceLink;
function generateTransactionLink(transactionName) {
    return function (organization, tableRow, query) {
        var eventSlug = urls_1.generateEventSlug(tableRow);
        return utils_2.getTransactionDetailsUrl(organization, eventSlug, transactionName, query);
    };
}
exports.generateTransactionLink = generateTransactionLink;
exports.SidebarSpacer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(3));
var templateObject_1;
//# sourceMappingURL=utils.jsx.map