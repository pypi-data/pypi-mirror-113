Object.defineProperty(exports, "__esModule", { value: true });
exports.getLabel = exports.getConfirm = exports.ConfirmAction = exports.BULK_LIMIT_STR = exports.BULK_LIMIT = void 0;
var tslib_1 = require("tslib");
var capitalize_1 = tslib_1.__importDefault(require("lodash/capitalize"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
var extraDescription_1 = tslib_1.__importDefault(require("./extraDescription"));
exports.BULK_LIMIT = 1000;
exports.BULK_LIMIT_STR = exports.BULK_LIMIT.toLocaleString();
var ConfirmAction;
(function (ConfirmAction) {
    ConfirmAction["RESOLVE"] = "resolve";
    ConfirmAction["UNRESOLVE"] = "unresolve";
    ConfirmAction["IGNORE"] = "ignore";
    ConfirmAction["BOOKMARK"] = "bookmark";
    ConfirmAction["UNBOOKMARK"] = "unbookmark";
    ConfirmAction["MERGE"] = "merge";
    ConfirmAction["DELETE"] = "delete";
})(ConfirmAction = exports.ConfirmAction || (exports.ConfirmAction = {}));
function getBulkConfirmMessage(action, queryCount) {
    if (queryCount > exports.BULK_LIMIT) {
        return locale_1.tct('Are you sure you want to [action] the first [bulkNumber] issues that match the search?', {
            action: action,
            bulkNumber: exports.BULK_LIMIT_STR,
        });
    }
    return locale_1.tct('Are you sure you want to [action] all [bulkNumber] issues that match the search?', {
        action: action,
        bulkNumber: queryCount,
    });
}
function getConfirm(numIssues, allInQuerySelected, query, queryCount) {
    return function (action, canBeUndone, append) {
        if (append === void 0) { append = ''; }
        var question = allInQuerySelected
            ? getBulkConfirmMessage("" + action + append, queryCount)
            : locale_1.tn("Are you sure you want to " + action + " this %s issue" + append + "?", "Are you sure you want to " + action + " these %s issues" + append + "?", numIssues);
        var message;
        switch (action) {
            case ConfirmAction.DELETE:
                message = locale_1.tct('Bulk deletion is only recommended for junk data. To clear your stream, consider resolving or ignoring. [link:When should I delete events?]', {
                    link: (<externalLink_1.default href="https://help.sentry.io/account/billing/when-should-i-delete-events/"/>),
                });
                break;
            case ConfirmAction.MERGE:
                message = locale_1.t('Note that unmerging is currently an experimental feature.');
                break;
            default:
                message = locale_1.t('This action cannot be undone.');
        }
        return (<div>
        <p style={{ marginBottom: '20px' }}>
          <strong>{question}</strong>
        </p>
        <extraDescription_1.default all={allInQuerySelected} query={query} queryCount={queryCount}/>
        {!canBeUndone && <p>{message}</p>}
      </div>);
    };
}
exports.getConfirm = getConfirm;
function getLabel(numIssues, allInQuerySelected) {
    return function (action, append) {
        if (append === void 0) { append = ''; }
        var capitalized = capitalize_1.default(action);
        var text = allInQuerySelected
            ? locale_1.t("Bulk " + action + " issues")
            : locale_1.tn(capitalized + " %s selected issue", capitalized + " %s selected issues", numIssues);
        return text + append;
    };
}
exports.getLabel = getLabel;
//# sourceMappingURL=utils.jsx.map