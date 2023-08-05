Object.defineProperty(exports, "__esModule", { value: true });
exports.generatePerformanceVitalDetailView = exports.generatePerformanceEventView = exports.getTermHelp = exports.getMobileAxisOptions = exports.getBackendAxisOptions = exports.getFrontendOtherAxisOptions = exports.getFrontendAxisOptions = exports.getAxisOptions = exports.PERFORMANCE_TERM = exports.COLUMN_TITLES = exports.DEFAULT_STATS_PERIOD = void 0;
var tslib_1 = require("tslib");
var gridEditable_1 = require("app/components/gridEditable");
var locale_1 = require("app/locale");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var utils_1 = require("./landing/utils");
var utils_2 = require("./vitalDetail/utils");
exports.DEFAULT_STATS_PERIOD = '24h';
exports.COLUMN_TITLES = [
    'transaction',
    'project',
    'tpm',
    'p50',
    'p95',
    'failure rate',
    'apdex',
    'users',
    'user misery',
];
var PERFORMANCE_TERM;
(function (PERFORMANCE_TERM) {
    PERFORMANCE_TERM["APDEX"] = "apdex";
    PERFORMANCE_TERM["TPM"] = "tpm";
    PERFORMANCE_TERM["THROUGHPUT"] = "throughput";
    PERFORMANCE_TERM["FAILURE_RATE"] = "failureRate";
    PERFORMANCE_TERM["P50"] = "p50";
    PERFORMANCE_TERM["P75"] = "p75";
    PERFORMANCE_TERM["P95"] = "p95";
    PERFORMANCE_TERM["P99"] = "p99";
    PERFORMANCE_TERM["LCP"] = "lcp";
    PERFORMANCE_TERM["FCP"] = "fcp";
    PERFORMANCE_TERM["USER_MISERY"] = "userMisery";
    PERFORMANCE_TERM["STATUS_BREAKDOWN"] = "statusBreakdown";
    PERFORMANCE_TERM["DURATION_DISTRIBUTION"] = "durationDistribution";
    PERFORMANCE_TERM["USER_MISERY_NEW"] = "userMiseryNew";
    PERFORMANCE_TERM["APDEX_NEW"] = "apdexNew";
    PERFORMANCE_TERM["APP_START_COLD"] = "appStartCold";
    PERFORMANCE_TERM["APP_START_WARM"] = "appStartWarm";
})(PERFORMANCE_TERM = exports.PERFORMANCE_TERM || (exports.PERFORMANCE_TERM = {}));
function getAxisOptions(organization) {
    var apdexOption;
    if (organization.features.includes('project-transaction-threshold')) {
        apdexOption = {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APDEX_NEW),
            value: 'apdex()',
            label: locale_1.t('Apdex'),
        };
    }
    else {
        apdexOption = {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APDEX),
            value: "apdex(" + organization.apdexThreshold + ")",
            label: locale_1.t('Apdex'),
        };
    }
    return [
        apdexOption,
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.TPM),
            value: 'tpm()',
            label: locale_1.t('Transactions Per Minute'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE),
            value: 'failure_rate()',
            label: locale_1.t('Failure Rate'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P50),
            value: 'p50()',
            label: locale_1.t('p50 Duration'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P95),
            value: 'p95()',
            label: locale_1.t('p95 Duration'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P99),
            value: 'p99()',
            label: locale_1.t('p99 Duration'),
        },
    ];
}
exports.getAxisOptions = getAxisOptions;
function getFrontendAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.LCP),
            value: "p75(lcp)",
            label: locale_1.t('LCP p75'),
            field: 'p75(measurements.lcp)',
            isLeftDefault: true,
            backupOption: {
                tooltip: getTermHelp(organization, PERFORMANCE_TERM.FCP),
                value: "p75(fcp)",
                label: locale_1.t('FCP p75'),
                field: 'p75(measurements.fcp)',
            },
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            value: 'lcp_distribution',
            label: locale_1.t('LCP Distribution'),
            field: 'measurements.lcp',
            isDistribution: true,
            isRightDefault: true,
            backupOption: {
                tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
                value: 'fcp_distribution',
                label: locale_1.t('FCP Distribution'),
                field: 'measurements.fcp',
                isDistribution: true,
            },
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.TPM),
            value: 'tpm()',
            label: locale_1.t('Transactions Per Minute'),
            field: 'tpm()',
        },
    ];
}
exports.getFrontendAxisOptions = getFrontendAxisOptions;
function getFrontendOtherAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P50),
            value: "p50()",
            label: locale_1.t('Duration p50'),
            field: 'p50(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P75),
            value: "p75()",
            label: locale_1.t('Duration p75'),
            field: 'p75(transaction.duration)',
            isLeftDefault: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P95),
            value: "p95()",
            label: locale_1.t('Duration p95'),
            field: 'p95(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            value: 'duration_distribution',
            label: locale_1.t('Duration Distribution'),
            field: 'transaction.duration',
            isDistribution: true,
            isRightDefault: true,
        },
    ];
}
exports.getFrontendOtherAxisOptions = getFrontendOtherAxisOptions;
function getBackendAxisOptions(organization) {
    var apdexOption;
    if (organization.features.includes('project-transaction-threshold')) {
        apdexOption = {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APDEX),
            value: 'apdex()',
            label: locale_1.t('Apdex'),
            field: 'apdex()',
        };
    }
    else {
        apdexOption = {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APDEX),
            value: "apdex(" + organization.apdexThreshold + ")",
            label: locale_1.t('Apdex'),
            field: "apdex(" + organization.apdexThreshold + ")",
        };
    }
    return [
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P50),
            value: "p50()",
            label: locale_1.t('Duration p50'),
            field: 'p50(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P75),
            value: "p75()",
            label: locale_1.t('Duration p75'),
            field: 'p75(transaction.duration)',
            isLeftDefault: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P95),
            value: "p95()",
            label: locale_1.t('Duration p95'),
            field: 'p95(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P99),
            value: "p99()",
            label: locale_1.t('Duration p99'),
            field: 'p99(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.TPM),
            value: 'tpm()',
            label: locale_1.t('Transactions Per Minute'),
            field: 'tpm()',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE),
            value: 'failure_rate()',
            label: locale_1.t('Failure Rate'),
            field: 'failure_rate()',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            value: 'duration_distribution',
            label: locale_1.t('Duration Distribution'),
            field: 'transaction.duration',
            isDistribution: true,
            isRightDefault: true,
        },
        apdexOption,
    ];
}
exports.getBackendAxisOptions = getBackendAxisOptions;
function getMobileAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_COLD),
            value: "p50(measurements.app_start_cold)",
            label: locale_1.t('Cold Start Duration p50'),
            field: 'p50(measurements.app_start_cold)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_COLD),
            value: "p75(measurements.app_start_cold)",
            label: locale_1.t('Cold Start Duration p75'),
            field: 'p75(measurements.app_start_cold)',
            isLeftDefault: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_COLD),
            value: "p95(measurements.app_start_cold)",
            label: locale_1.t('Cold Start Duration p95'),
            field: 'p95(measurements.app_start_cold)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_COLD),
            value: "p99(measurements.app_start_cold)",
            label: locale_1.t('Cold Start Duration p99'),
            field: 'p99(measurements.app_start_cold)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            value: 'app_start_cold_distribution',
            label: locale_1.t('Cold Start Distribution'),
            field: 'measurements.app_start_cold',
            isDistribution: true,
            isRightDefault: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_WARM),
            value: "p50(measurements.app_start_warm)",
            label: locale_1.t('Warm Start Duration p50'),
            field: 'p50(measurements.app_start_warm)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_WARM),
            value: "p75(measurements.app_start_warm)",
            label: locale_1.t('Warm Start Duration p75'),
            field: 'p75(measurements.app_start_warm)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_WARM),
            value: "p95(measurements.app_start_warm)",
            label: locale_1.t('Warm Start Duration p95'),
            field: 'p95(measurements.app_start_warm)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APP_START_WARM),
            value: "p99(measurements.app_start_warm)",
            label: locale_1.t('Warm Start Duration p99'),
            field: 'p99(measurements.app_start_warm)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            value: 'app_start_warm_distribution',
            label: locale_1.t('Warm Start Distribution'),
            field: 'measurements.app_start_warm',
            isDistribution: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.TPM),
            value: 'tpm()',
            label: locale_1.t('Transactions Per Minute'),
            field: 'tpm()',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE),
            value: 'failure_rate()',
            label: locale_1.t('Failure Rate'),
            field: 'failure_rate()',
        },
    ];
}
exports.getMobileAxisOptions = getMobileAxisOptions;
var PERFORMANCE_TERMS = {
    apdex: function () {
        return locale_1.t('Apdex is the ratio of both satisfactory and tolerable response times to all response times. To adjust the tolerable threshold, go to performance settings.');
    },
    tpm: function () { return locale_1.t('TPM is the number of recorded transaction events per minute.'); },
    throughput: function () {
        return locale_1.t('Throughput is the number of recorded transaction events per minute.');
    },
    failureRate: function () {
        return locale_1.t('Failure rate is the percentage of recorded transactions that had a known and unsuccessful status.');
    },
    p50: function () { return locale_1.t('p50 indicates the duration that 50% of transactions are faster than.'); },
    p75: function () { return locale_1.t('p75 indicates the duration that 75% of transactions are faster than.'); },
    p95: function () { return locale_1.t('p95 indicates the duration that 95% of transactions are faster than.'); },
    p99: function () { return locale_1.t('p99 indicates the duration that 99% of transactions are faster than.'); },
    lcp: function () {
        return locale_1.t('Largest contentful paint (LCP) is a web vital meant to represent user load times');
    },
    fcp: function () {
        return locale_1.t('First contentful paint (FCP) is a web vital meant to represent user load times');
    },
    userMisery: function (organization) {
        return locale_1.t("User Misery is a score that represents the number of unique users who have experienced load times 4x your organization's apdex threshold of %sms.", organization.apdexThreshold);
    },
    statusBreakdown: function () {
        return locale_1.t('The breakdown of transaction statuses. This may indicate what type of failure it is.');
    },
    durationDistribution: function () {
        return locale_1.t('Distribution buckets counts of transactions at specifics times for your current date range');
    },
    userMiseryNew: function () {
        return locale_1.t("User Misery is a score that represents the number of unique users who have experienced load times 4x the project's configured threshold. Adjust project threshold in project performance settings.");
    },
    apdexNew: function () {
        return locale_1.t('Apdex is the ratio of both satisfactory and tolerable response times to all response times. To adjust the tolerable threshold, go to project performance settings.');
    },
    appStartCold: function () {
        return locale_1.t('Cold start is a measure of the application start up time from scratch.');
    },
    appStartWarm: function () {
        return locale_1.t('Warm start is a measure of the application start up time while still in memory.');
    },
};
function getTermHelp(organization, term) {
    if (!PERFORMANCE_TERMS.hasOwnProperty(term)) {
        return '';
    }
    return PERFORMANCE_TERMS[term](organization);
}
exports.getTermHelp = getTermHelp;
function generateGenericPerformanceEventView(organization, location) {
    var query = location.query;
    var fields = [
        organization.features.includes('team-key-transactions')
            ? 'team_key_transaction'
            : 'key_transaction',
        'transaction',
        'project',
        'tpm()',
        'p50()',
        'p95()',
        'failure_rate()',
    ];
    var featureFields = organization.features.includes('project-transaction-threshold')
        ? ['apdex()', 'count_unique(user)', 'count_miserable(user)', 'user_misery()']
        : [
            "apdex(" + organization.apdexThreshold + ")",
            'count_unique(user)',
            "count_miserable(user," + organization.apdexThreshold + ")",
            "user_misery(" + organization.apdexThreshold + ")",
        ];
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: locale_1.t('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(fields)), tslib_1.__read(featureFields)),
        version: 2,
    };
    var widths = Array(savedQuery.fields.length).fill(gridEditable_1.COL_WIDTH_UNDEFINED);
    widths[savedQuery.fields.length - 1] = '110';
    savedQuery.widths = widths;
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = exports.DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = queryString_1.decodeScalar(query.sort, '-tpm');
    var searchQuery = queryString_1.decodeScalar(query.query, '');
    var conditions = tokenizeSearch_1.tokenizeSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasTag('transaction.duration')) {
        conditions.setTagValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        // the query here is a user entered condition, no need to escape it
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"], false);
        conditions.query = [];
    }
    savedQuery.query = conditions.formatString();
    var eventView = eventView_1.default.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions.addTagValues('event.type', ['transaction']);
    return eventView;
}
function generateBackendPerformanceEventView(organization, location) {
    var query = location.query;
    var fields = [
        organization.features.includes('team-key-transactions')
            ? 'team_key_transaction'
            : 'key_transaction',
        'transaction',
        'project',
        'transaction.op',
        'http.method',
        'tpm()',
        'p50()',
        'p95()',
        'failure_rate()',
    ];
    var featureFields = organization.features.includes('project-transaction-threshold')
        ? ['apdex()', 'count_unique(user)', 'count_miserable(user)', 'user_misery()']
        : [
            "apdex(" + organization.apdexThreshold + ")",
            'count_unique(user)',
            "count_miserable(user," + organization.apdexThreshold + ")",
            "user_misery(" + organization.apdexThreshold + ")",
        ];
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: locale_1.t('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(fields)), tslib_1.__read(featureFields)),
        version: 2,
    };
    var widths = Array(savedQuery.fields.length).fill(gridEditable_1.COL_WIDTH_UNDEFINED);
    widths[savedQuery.fields.length - 1] = '110';
    savedQuery.widths = widths;
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = exports.DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = queryString_1.decodeScalar(query.sort, '-tpm');
    var searchQuery = queryString_1.decodeScalar(query.query, '');
    var conditions = tokenizeSearch_1.tokenizeSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasTag('transaction.duration')) {
        conditions.setTagValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        // the query here is a user entered condition, no need to escape it
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"], false);
        conditions.query = [];
    }
    savedQuery.query = conditions.formatString();
    var eventView = eventView_1.default.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions.addTagValues('event.type', ['transaction']);
    return eventView;
}
function generateMobilePerformanceEventView(organization, location) {
    var query = location.query;
    var fields = [
        organization.features.includes('team-key-transactions')
            ? 'team_key_transaction'
            : 'key_transaction',
        'transaction',
        'project',
        'transaction.op',
        'tpm()',
        'p50(measurements.app_start_cold)',
        'p95(measurements.app_start_cold)',
        'p50(measurements.app_start_warm)',
        'p95(measurements.app_start_warm)',
        'failure_rate()',
    ];
    var featureFields = organization.features.includes('project-transaction-threshold')
        ? ['apdex()', 'count_unique(user)', 'count_miserable(user)', 'user_misery()']
        : [
            "apdex(" + organization.apdexThreshold + ")",
            'count_unique(user)',
            "count_miserable(user," + organization.apdexThreshold + ")",
            "user_misery(" + organization.apdexThreshold + ")",
        ];
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: locale_1.t('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(fields)), tslib_1.__read(featureFields)),
        version: 2,
    };
    var widths = Array(savedQuery.fields.length).fill(gridEditable_1.COL_WIDTH_UNDEFINED);
    widths[savedQuery.fields.length - 1] = '110';
    savedQuery.widths = widths;
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = exports.DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = queryString_1.decodeScalar(query.sort, '-tpm');
    var searchQuery = queryString_1.decodeScalar(query.query, '');
    var conditions = tokenizeSearch_1.tokenizeSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasTag('transaction.duration')) {
        conditions.setTagValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        // the query here is a user entered condition, no need to escape it
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"], false);
        conditions.query = [];
    }
    savedQuery.query = conditions.formatString();
    var eventView = eventView_1.default.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions.addTagValues('event.type', ['transaction']);
    return eventView;
}
function generateFrontendPageloadPerformanceEventView(organization, location) {
    var query = location.query;
    var fields = [
        organization.features.includes('team-key-transactions')
            ? 'team_key_transaction'
            : 'key_transaction',
        'transaction',
        'project',
        'tpm()',
        'p75(measurements.fcp)',
        'p75(measurements.lcp)',
        'p75(measurements.fid)',
        'p75(measurements.cls)',
    ];
    var featureFields = organization.features.includes('project-transaction-threshold')
        ? ['count_unique(user)', 'count_miserable(user)', 'user_misery()']
        : [
            'count_unique(user)',
            "count_miserable(user," + organization.apdexThreshold + ")",
            "user_misery(" + organization.apdexThreshold + ")",
        ];
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: locale_1.t('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(fields)), tslib_1.__read(featureFields)),
        version: 2,
    };
    var widths = Array(savedQuery.fields.length).fill(gridEditable_1.COL_WIDTH_UNDEFINED);
    widths[savedQuery.fields.length - 1] = '110';
    savedQuery.widths = widths;
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = exports.DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = queryString_1.decodeScalar(query.sort, '-tpm');
    var searchQuery = queryString_1.decodeScalar(query.query, '');
    var conditions = tokenizeSearch_1.tokenizeSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasTag('transaction.duration')) {
        conditions.setTagValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        // the query here is a user entered condition, no need to escape it
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"], false);
        conditions.query = [];
    }
    savedQuery.query = conditions.formatString();
    var eventView = eventView_1.default.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions
        .addTagValues('event.type', ['transaction'])
        .addTagValues('transaction.op', ['pageload']);
    return eventView;
}
function generateFrontendOtherPerformanceEventView(organization, location) {
    var query = location.query;
    var fields = [
        organization.features.includes('team-key-transactions')
            ? 'team_key_transaction'
            : 'key_transaction',
        'transaction',
        'project',
        'transaction.op',
        'tpm()',
        'p50(transaction.duration)',
        'p75(transaction.duration)',
        'p95(transaction.duration)',
    ];
    var featureFields = organization.features.includes('project-transaction-threshold')
        ? ['count_unique(user)', 'count_miserable(user)', 'user_misery()']
        : [
            'count_unique(user)',
            "count_miserable(user," + organization.apdexThreshold + ")",
            "user_misery(" + organization.apdexThreshold + ")",
        ];
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: locale_1.t('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(fields)), tslib_1.__read(featureFields)),
        version: 2,
    };
    var widths = Array(savedQuery.fields.length).fill(gridEditable_1.COL_WIDTH_UNDEFINED);
    widths[savedQuery.fields.length - 1] = '110';
    savedQuery.widths = widths;
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = exports.DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = queryString_1.decodeScalar(query.sort, '-tpm');
    var searchQuery = queryString_1.decodeScalar(query.query, '');
    var conditions = tokenizeSearch_1.tokenizeSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasTag('transaction.duration')) {
        conditions.setTagValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        // the query here is a user entered condition, no need to escape it
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"], false);
        conditions.query = [];
    }
    savedQuery.query = conditions.formatString();
    var eventView = eventView_1.default.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions
        .addTagValues('event.type', ['transaction'])
        .addTagValues('!transaction.op', ['pageload']);
    return eventView;
}
function generatePerformanceEventView(organization, location, projects, isTrends) {
    if (isTrends === void 0) { isTrends = false; }
    var eventView = generateGenericPerformanceEventView(organization, location);
    if (isTrends) {
        return eventView;
    }
    var display = utils_1.getCurrentLandingDisplay(location, projects, eventView);
    switch (display === null || display === void 0 ? void 0 : display.field) {
        case utils_1.LandingDisplayField.FRONTEND_PAGELOAD:
            return generateFrontendPageloadPerformanceEventView(organization, location);
        case utils_1.LandingDisplayField.FRONTEND_OTHER:
            return generateFrontendOtherPerformanceEventView(organization, location);
        case utils_1.LandingDisplayField.BACKEND:
            return generateBackendPerformanceEventView(organization, location);
        case utils_1.LandingDisplayField.MOBILE:
            return generateMobilePerformanceEventView(organization, location);
        default:
            return eventView;
    }
}
exports.generatePerformanceEventView = generatePerformanceEventView;
function generatePerformanceVitalDetailView(organization, location) {
    var query = location.query;
    var vitalName = utils_2.vitalNameFromLocation(location);
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: locale_1.t('Vitals Performance Details'),
        query: 'event.type:transaction',
        projects: [],
        fields: [
            organization.features.includes('team-key-transactions')
                ? 'team_key_transaction'
                : 'key_transaction',
            'transaction',
            'project',
            'count_unique(user)',
            'count()',
            "p50(" + vitalName + ")",
            "p75(" + vitalName + ")",
            "p95(" + vitalName + ")",
            utils_2.getVitalDetailTablePoorStatusFunction(vitalName),
            utils_2.getVitalDetailTableMehStatusFunction(vitalName),
        ],
        version: 2,
    };
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = exports.DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = queryString_1.decodeScalar(query.sort, '-count');
    var searchQuery = queryString_1.decodeScalar(query.query, '');
    var conditions = tokenizeSearch_1.tokenizeSearch(searchQuery);
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        // the query here is a user entered condition, no need to escape it
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"], false);
        conditions.query = [];
    }
    savedQuery.query = conditions.formatString();
    var eventView = eventView_1.default.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions
        .addTagValues('event.type', ['transaction'])
        .addTagValues('has', [vitalName]);
    return eventView;
}
exports.generatePerformanceVitalDetailView = generatePerformanceVitalDetailView;
//# sourceMappingURL=data.jsx.map