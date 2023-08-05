Object.defineProperty(exports, "__esModule", { value: true });
exports.makeDefaultCta = exports.PRESET_AGGREGATES = void 0;
var tslib_1 = require("tslib");
var locale_1 = require("app/locale");
var types_1 = require("app/utils/discover/types");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var utils_1 = require("app/views/alerts/utils");
var getIncidentDiscoverUrl_1 = require("app/views/alerts/utils/getIncidentDiscoverUrl");
var utils_2 = require("app/views/performance/transactionSummary/utils");
var types_2 = require("./types");
exports.PRESET_AGGREGATES = [
    {
        name: locale_1.t('Error count'),
        match: /^count\(\)/,
        validDataset: [types_2.Dataset.ERRORS],
        default: 'count()',
        /**
         * Simple "Open in Discover" button
         */
        makeCtaParams: makeDefaultCta,
    },
    {
        name: locale_1.t('Users affected'),
        match: /^count_unique\(tags\[sentry:user\]\)/,
        validDataset: [types_2.Dataset.ERRORS],
        default: 'count_unique(tags[sentry:user])',
        /**
         * Simple "Open in Discover" button
         */
        makeCtaParams: makeDefaultCta,
    },
    {
        name: locale_1.t('Latency'),
        match: /^(p[0-9]{2,3}|percentile\(transaction\.duration,[^)]+\)|avg\([^)]+\))/,
        validDataset: [types_2.Dataset.TRANSACTIONS],
        default: 'percentile(transaction.duration, 0.95)',
        /**
         * see: makeGenericTransactionCta
         */
        makeCtaParams: function (opts) {
            return makeGenericTransactionCta({
                opts: opts,
                tooltip: locale_1.t('Latency by Transaction'),
            });
        },
    },
    {
        name: locale_1.t('Apdex'),
        match: /^apdex\([0-9.]+\)/,
        validDataset: [types_2.Dataset.TRANSACTIONS],
        default: 'apdex(300)',
        /**
         * see: makeGenericTransactionCta
         */
        makeCtaParams: function (opts) {
            return makeGenericTransactionCta({
                opts: opts,
                tooltip: locale_1.t('Apdex by Transaction'),
            });
        },
    },
    {
        name: locale_1.t('Transaction Count'),
        match: /^count\(\)/,
        validDataset: [types_2.Dataset.TRANSACTIONS],
        default: 'count()',
        /**
         * see: makeGenericTransactionCta
         */
        makeCtaParams: function (opts) { return makeGenericTransactionCta({ opts: opts }); },
    },
    {
        name: locale_1.t('Failure rate'),
        match: /^failure_rate\(\)/,
        validDataset: [types_2.Dataset.TRANSACTIONS],
        default: 'failure_rate()',
        /**
         * See makeFailureRateCta
         */
        makeCtaParams: makeFailureRateCta,
    },
];
/**
 * - CASE 1: If has a specific transaction filter
 *   - CTA is: "View Transaction Summary"
 *   - Tooltip is the transaction name
 *   - the same period as the alert graph (i.e. with alert start time in the middle)
 *
 * - CASE 2: If transaction is NOT filtered, or has a * filter:
 *   - "Open in Discover" button with optional tooltip which opens a discover view with...
 *      - fields {transaction, count(), <metric>} sorted by count()
 *      - top-5 activated
 */
function makeGenericTransactionCta(opts) {
    var _a, _b;
    var _c = opts.opts, orgSlug = _c.orgSlug, projects = _c.projects, incident = _c.incident, stats = _c.stats, tooltip = opts.tooltip;
    if (!incident || !stats) {
        return { to: '', buttonText: locale_1.t('Incident details') };
    }
    var query = tokenizeSearch_1.tokenizeSearch((_a = incident.discoverQuery) !== null && _a !== void 0 ? _a : '');
    var transaction = (_b = query
        .getTagValues('transaction')) === null || _b === void 0 ? void 0 : _b.find(function (filter) { return !filter.includes('*'); });
    // CASE 1
    if (transaction !== undefined) {
        var period = utils_1.getStartEndFromStats(stats);
        var summaryUrl = utils_2.transactionSummaryRouteWithQuery({
            orgSlug: orgSlug,
            transaction: transaction,
            projectID: projects
                .filter(function (_a) {
                var slug = _a.slug;
                return incident.projects.includes(slug);
            })
                .map(function (_a) {
                var id = _a.id;
                return id;
            }),
            query: tslib_1.__assign({}, period),
        });
        return {
            to: summaryUrl,
            buttonText: locale_1.t('View Transaction Summary'),
            title: transaction,
        };
    }
    // CASE 2
    var extraQueryParams = {
        fields: tslib_1.__spreadArray([], tslib_1.__read(new Set(['transaction', 'count()', incident.alertRule.aggregate]))),
        orderby: '-count',
        display: types_1.DisplayModes.TOP5,
    };
    var discoverUrl = getIncidentDiscoverUrl_1.getIncidentDiscoverUrl({
        orgSlug: orgSlug,
        projects: projects,
        incident: incident,
        stats: stats,
        extraQueryParams: extraQueryParams,
    });
    return {
        to: discoverUrl,
        buttonText: locale_1.t('Open in Discover'),
        title: tooltip,
    };
}
/**
 * - CASE 1: Filtered to a specific transaction, "Open in Discover" with...
 *   - fields [transaction.status, count()] sorted by count(),
 *   - "Top 5 period" activated.
 *
 * - CASE 2: If filtered on multiple transactions, "Open in Discover" button
 *   with tooltip "Failure rate by transaction" which opens a discover view
 *   - fields [transaction, failure_rate()] sorted by failure_rate
 *   - top 5 activated
 */
function makeFailureRateCta(_a) {
    var _b, _c;
    var orgSlug = _a.orgSlug, incident = _a.incident, projects = _a.projects, stats = _a.stats;
    if (!incident || !stats) {
        return { to: '', buttonText: locale_1.t('Incident details') };
    }
    var query = tokenizeSearch_1.tokenizeSearch((_b = incident.discoverQuery) !== null && _b !== void 0 ? _b : '');
    var transaction = (_c = query
        .getTagValues('transaction')) === null || _c === void 0 ? void 0 : _c.find(function (filter) { return !filter.includes('*'); });
    var extraQueryParams = transaction !== undefined
        ? // CASE 1
            {
                fields: ['transaction.status', 'count()'],
                orderby: '-count',
                display: types_1.DisplayModes.TOP5,
            }
        : // Case 2
            {
                fields: ['transaction', 'failure_rate()'],
                orderby: '-failure_rate',
                display: types_1.DisplayModes.TOP5,
            };
    var discoverUrl = getIncidentDiscoverUrl_1.getIncidentDiscoverUrl({
        orgSlug: orgSlug,
        projects: projects,
        incident: incident,
        stats: stats,
        extraQueryParams: extraQueryParams,
    });
    return {
        to: discoverUrl,
        buttonText: locale_1.t('Open in Discover'),
        title: transaction === undefined ? locale_1.t('Failure rate by transaction') : undefined,
    };
}
/**
 * Get the CTA used for alerts that do not have a preset
 */
function makeDefaultCta(_a) {
    var orgSlug = _a.orgSlug, projects = _a.projects, incident = _a.incident, stats = _a.stats;
    if (!incident) {
        return {
            buttonText: locale_1.t('Open in Discover'),
            to: '',
        };
    }
    var extraQueryParams = {
        display: types_1.DisplayModes.TOP5,
    };
    return {
        buttonText: locale_1.t('Open in Discover'),
        to: getIncidentDiscoverUrl_1.getIncidentDiscoverUrl({ orgSlug: orgSlug, projects: projects, incident: incident, stats: stats, extraQueryParams: extraQueryParams }),
    };
}
exports.makeDefaultCta = makeDefaultCta;
//# sourceMappingURL=presets.jsx.map