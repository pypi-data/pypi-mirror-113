Object.defineProperty(exports, "__esModule", { value: true });
exports.getDisplayLabel = exports.IssueDisplayOptions = exports.getSortLabel = exports.IssueSortOptions = exports.TAB_MAX_COUNT = exports.isForReviewQuery = exports.getTabsWithCounts = exports.getTabs = exports.Query = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
var Query;
(function (Query) {
    Query["FOR_REVIEW"] = "is:unresolved is:for_review assigned_or_suggested:[me, none]";
    Query["UNRESOLVED"] = "is:unresolved";
    Query["IGNORED"] = "is:ignored";
    Query["REPROCESSING"] = "is:reprocessing";
})(Query = exports.Query || (exports.Query = {}));
/**
 * Get a list of currently active tabs
 */
function getTabs(organization) {
    var tabs = [
        [
            Query.UNRESOLVED,
            {
                name: locale_1.t('All Unresolved'),
                analyticsName: 'unresolved',
                count: true,
                enabled: true,
                tooltipTitle: locale_1.t("All unresolved issues."),
            },
        ],
        [
            Query.FOR_REVIEW,
            {
                name: locale_1.t('For Review'),
                analyticsName: 'needs_review',
                count: true,
                enabled: true,
                tooltipTitle: locale_1.t("Unresolved issues that are new or have reopened. Review, ignore,\n        or resolve an issue to move it out of this list. After 7 days these\n        issues are automatically marked as reviewed."),
            },
        ],
        [
            Query.IGNORED,
            {
                name: locale_1.t('Ignored'),
                analyticsName: 'ignored',
                count: true,
                enabled: true,
                tooltipTitle: locale_1.t("Ignored issues don\u2019t trigger alerts. When their ignore\n        conditions are met they become Unresolved and are flagged for review."),
            },
        ],
        [
            Query.REPROCESSING,
            {
                name: locale_1.t('Reprocessing'),
                analyticsName: 'reprocessing',
                count: true,
                enabled: organization.features.includes('reprocessing-v2'),
                tooltipTitle: locale_1.tct("These [link:reprocessing issues] will take some time to complete.\n        Any new issues that are created during reprocessing will be flagged for review.", {
                    link: (<externalLink_1.default href="https://docs.sentry.io/product/error-monitoring/reprocessing/"/>),
                }),
                tooltipHoverable: true,
            },
        ],
    ];
    return tabs.filter(function (_a) {
        var _b = tslib_1.__read(_a, 2), _query = _b[0], tab = _b[1];
        return tab.enabled;
    });
}
exports.getTabs = getTabs;
/**
 * @returns queries that should have counts fetched
 */
function getTabsWithCounts(organization) {
    var tabs = getTabs(organization);
    return tabs.filter(function (_a) {
        var _b = tslib_1.__read(_a, 2), _query = _b[0], tab = _b[1];
        return tab.count;
    }).map(function (_a) {
        var _b = tslib_1.__read(_a, 1), query = _b[0];
        return query;
    });
}
exports.getTabsWithCounts = getTabsWithCounts;
function isForReviewQuery(query) {
    return !!query && /\bis:for_review\b/.test(query);
}
exports.isForReviewQuery = isForReviewQuery;
// the tab counts will look like 99+
exports.TAB_MAX_COUNT = 99;
var IssueSortOptions;
(function (IssueSortOptions) {
    IssueSortOptions["DATE"] = "date";
    IssueSortOptions["NEW"] = "new";
    IssueSortOptions["PRIORITY"] = "priority";
    IssueSortOptions["FREQ"] = "freq";
    IssueSortOptions["USER"] = "user";
    IssueSortOptions["TREND"] = "trend";
    IssueSortOptions["INBOX"] = "inbox";
})(IssueSortOptions = exports.IssueSortOptions || (exports.IssueSortOptions = {}));
function getSortLabel(key) {
    switch (key) {
        case IssueSortOptions.NEW:
            return locale_1.t('First Seen');
        case IssueSortOptions.PRIORITY:
            return locale_1.t('Priority');
        case IssueSortOptions.FREQ:
            return locale_1.t('Events');
        case IssueSortOptions.USER:
            return locale_1.t('Users');
        case IssueSortOptions.TREND:
            return locale_1.t('Relative Change');
        case IssueSortOptions.INBOX:
            return locale_1.t('Date Added');
        case IssueSortOptions.DATE:
        default:
            return locale_1.t('Last Seen');
    }
}
exports.getSortLabel = getSortLabel;
var IssueDisplayOptions;
(function (IssueDisplayOptions) {
    IssueDisplayOptions["EVENTS"] = "events";
    IssueDisplayOptions["SESSIONS"] = "sessions";
})(IssueDisplayOptions = exports.IssueDisplayOptions || (exports.IssueDisplayOptions = {}));
function getDisplayLabel(key) {
    switch (key) {
        case IssueDisplayOptions.SESSIONS:
            return locale_1.t('Events as %');
        case IssueDisplayOptions.EVENTS:
        default:
            return locale_1.t('Event Count');
    }
}
exports.getDisplayLabel = getDisplayLabel;
//# sourceMappingURL=utils.jsx.map