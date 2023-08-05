Object.defineProperty(exports, "__esModule", { value: true });
exports.getFunctionHelpText = exports.hideParameterSelectorSet = exports.hidePrimarySelectorSet = exports.AlertWizardRuleTemplates = exports.AlertWizardPanelContent = exports.AlertWizardOptions = exports.AlertWizardAlertNames = exports.WebVitalAlertTypes = void 0;
var tslib_1 = require("tslib");
var alerts_wizard_apdex_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/alerts-wizard-apdex.svg"));
var alerts_wizard_cls_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/alerts-wizard-cls.svg"));
var alerts_wizard_custom_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/alerts-wizard-custom.svg"));
var alerts_wizard_errors_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/alerts-wizard-errors.svg"));
var alerts_wizard_failure_rate_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/alerts-wizard-failure-rate.svg"));
var alerts_wizard_fid_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/alerts-wizard-fid.svg"));
var alerts_wizard_issues_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/alerts-wizard-issues.svg"));
var alerts_wizard_lcp_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/alerts-wizard-lcp.svg"));
var alerts_wizard_throughput_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/alerts-wizard-throughput.svg"));
var alerts_wizard_transaction_duration_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/alerts-wizard-transaction-duration.svg"));
var alerts_wizard_users_experiencing_errors_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/alerts-wizard-users-experiencing-errors.svg"));
var locale_1 = require("app/locale");
var types_1 = require("app/views/alerts/incidentRules/types");
exports.WebVitalAlertTypes = new Set(['lcp', 'fid', 'cls', 'fcp']);
exports.AlertWizardAlertNames = {
    issues: locale_1.t('Issues'),
    num_errors: locale_1.t('Number of Errors'),
    users_experiencing_errors: locale_1.t('Users Experiencing Errors'),
    throughput: locale_1.t('Throughput'),
    trans_duration: locale_1.t('Transaction Duration'),
    apdex: locale_1.t('Apdex'),
    failure_rate: locale_1.t('Failure Rate'),
    lcp: locale_1.t('Largest Contentful Paint'),
    fid: locale_1.t('First Input Delay'),
    cls: locale_1.t('Cumulative Layout Shift'),
    custom: locale_1.t('Custom Metric'),
};
exports.AlertWizardOptions = [
    {
        categoryHeading: locale_1.t('Errors'),
        options: ['issues', 'num_errors', 'users_experiencing_errors'],
    },
    {
        categoryHeading: locale_1.t('Performance'),
        options: [
            'throughput',
            'trans_duration',
            'apdex',
            'failure_rate',
            'lcp',
            'fid',
            'cls',
        ],
    },
    {
        categoryHeading: locale_1.t('Other'),
        options: ['custom'],
    },
];
exports.AlertWizardPanelContent = {
    issues: {
        description: locale_1.t('Issues are groups of errors that have a similar stacktrace. Set an alert for new issues, when an issue changes state, frequency of errors, or users affected by an issue.'),
        examples: [
            locale_1.t("When the triggering event's level is fatal."),
            locale_1.t('When an issue was seen 100 times in the last 2 days.'),
            locale_1.t('Create a JIRA ticket when an issue changes state from resolved to unresolved and is unassigned.'),
        ],
        illustration: alerts_wizard_issues_svg_1.default,
    },
    num_errors: {
        description: locale_1.t('Alert when the number of errors in a project matching your filters crosses a threshold. This is useful for monitoring the overall level or errors in your project or errors occurring in specific parts of your app.'),
        examples: [
            locale_1.t('When the signup page has more than 10k errors in 5 minutes.'),
            locale_1.t('When there are more than 500k errors in 10 minutes from a specific file.'),
        ],
        illustration: alerts_wizard_errors_svg_1.default,
    },
    users_experiencing_errors: {
        description: locale_1.t('Alert when the number of users affected by errors in your project crosses a threshold.'),
        examples: [
            locale_1.t('When 100k users experience an error in 1 hour.'),
            locale_1.t('When 100 users experience a problem on the Checkout page.'),
        ],
        illustration: alerts_wizard_users_experiencing_errors_svg_1.default,
    },
    throughput: {
        description: locale_1.t('Throughput is the total number of transactions in a project and you can alert when it reaches a threshold within a period of time.'),
        examples: [
            locale_1.t('When number of transactions on a key page exceeds 100k per minute.'),
            locale_1.t('When number of transactions drops below a threshold.'),
        ],
        illustration: alerts_wizard_throughput_svg_1.default,
    },
    trans_duration: {
        description: locale_1.t('Monitor how long it takes for transactions to complete. Use flexible aggregates like percentiles, averages, and min/max.'),
        examples: [
            locale_1.t('When any transaction is slower than 3 seconds.'),
            locale_1.t('When the 75th percentile response time is higher than 250 milliseconds.'),
        ],
        illustration: alerts_wizard_transaction_duration_svg_1.default,
    },
    apdex: {
        description: locale_1.t('Apdex is a metric used to track and measure user satisfaction based on your application response times. The Apdex score provides the ratio of satisfactory, tolerable, and frustrated requests in a specific transaction or endpoint.'),
        examples: [locale_1.t('When apdex is below 300.')],
        docsLink: 'https://docs.sentry.io/product/performance/metrics/#apdex',
        illustration: alerts_wizard_apdex_svg_1.default,
    },
    failure_rate: {
        description: locale_1.t('Failure rate is the percentage of unsuccessful transactions. Sentry treats transactions with a status other than “ok,” “canceled,” and “unknown” as failures.'),
        examples: [locale_1.t('When the failure rate for an important endpoint reaches 10%.')],
        docsLink: 'https://docs.sentry.io/product/performance/metrics/#failure-rate',
        illustration: alerts_wizard_failure_rate_svg_1.default,
    },
    lcp: {
        description: locale_1.t('Largest Contentful Paint (LCP) measures loading performance. It marks the point when the largest image or text block is visible within the viewport. A fast LCP helps reassure the user that the page is useful, and so we recommend an LCP of less than 2.5 seconds.'),
        examples: [
            locale_1.t('When the 75th percentile LCP of your homepage is longer than 2.5 seconds.'),
        ],
        docsLink: 'https://docs.sentry.io/product/performance/web-vitals',
        illustration: alerts_wizard_lcp_svg_1.default,
    },
    fid: {
        description: locale_1.t('First Input Delay (FID) measures interactivity as the response time when the user tries to interact with the viewport. A low FID helps ensure that a page is useful, and we recommend a FID of less than 100 milliseconds.'),
        examples: [locale_1.t('When the average FID of a page is longer than 4 seconds.')],
        docsLink: 'https://docs.sentry.io/product/performance/web-vitals',
        illustration: alerts_wizard_fid_svg_1.default,
    },
    cls: {
        description: locale_1.t('Cumulative Layout Shift (CLS) measures visual stability by quantifying unexpected layout shifts that occur during the entire lifespan of the page. A CLS of less than 0.1 is a good user experience, while anything greater than 0.25 is poor.'),
        examples: [locale_1.t('When the CLS of a page is more than 0.5.')],
        docsLink: 'https://docs.sentry.io/product/performance/web-vitals',
        illustration: alerts_wizard_cls_svg_1.default,
    },
    custom: {
        description: locale_1.t('Alert on metrics which are not listed above, such as first paint (FP), first contentful paint (FCP), and time to first byte (TTFB).'),
        examples: [
            locale_1.t('When the 95th percentile FP of a page is longer than 250 milliseconds.'),
            locale_1.t('When the average TTFB of a page is longer than 600 millliseconds.'),
        ],
        illustration: alerts_wizard_custom_svg_1.default,
    },
};
exports.AlertWizardRuleTemplates = {
    num_errors: {
        aggregate: 'count()',
        dataset: types_1.Dataset.ERRORS,
        eventTypes: types_1.EventTypes.ERROR,
    },
    users_experiencing_errors: {
        aggregate: 'count_unique(tags[sentry:user])',
        dataset: types_1.Dataset.ERRORS,
        eventTypes: types_1.EventTypes.ERROR,
    },
    throughput: {
        aggregate: 'count()',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    trans_duration: {
        aggregate: 'p95(transaction.duration)',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    apdex: {
        aggregate: 'apdex(300)',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    failure_rate: {
        aggregate: 'failure_rate()',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    lcp: {
        aggregate: 'p95(measurements.lcp)',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    fid: {
        aggregate: 'p95(measurements.fid)',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    cls: {
        aggregate: 'p95(measurements.cls)',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
    custom: {
        aggregate: 'p95(measurements.fp)',
        dataset: types_1.Dataset.TRANSACTIONS,
        eventTypes: types_1.EventTypes.TRANSACTION,
    },
};
exports.hidePrimarySelectorSet = new Set([
    'num_errors',
    'users_experiencing_errors',
    'throughput',
    'apdex',
    'failure_rate',
]);
exports.hideParameterSelectorSet = new Set([
    'trans_duration',
    'lcp',
    'fid',
    'cls',
]);
function getFunctionHelpText(alertType) {
    var timeWindowText = locale_1.t('over');
    if (alertType === 'apdex') {
        return {
            labelText: locale_1.t('Select apdex value and time interval'),
            timeWindowText: timeWindowText,
        };
    }
    else if (exports.hidePrimarySelectorSet.has(alertType)) {
        return {
            labelText: locale_1.t('Select time interval'),
        };
    }
    else {
        return {
            labelText: locale_1.t('Select function and time interval'),
            timeWindowText: timeWindowText,
        };
    }
}
exports.getFunctionHelpText = getFunctionHelpText;
//# sourceMappingURL=options.jsx.map