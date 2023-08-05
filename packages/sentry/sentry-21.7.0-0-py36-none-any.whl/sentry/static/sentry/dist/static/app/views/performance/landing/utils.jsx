Object.defineProperty(exports, "__esModule", { value: true });
exports.getDisplayAxes = exports.backendCardDetails = exports.getDefaultDisplayFieldForPlatform = exports.getBackendFunction = exports.getChartWidth = exports.getCurrentLandingDisplay = exports.LANDING_DISPLAYS = exports.LandingDisplayField = exports.RIGHT_AXIS_QUERY_KEY = exports.LEFT_AXIS_QUERY_KEY = void 0;
var locale_1 = require("app/locale");
var formatters_1 = require("app/utils/formatters");
var queryString_1 = require("app/utils/queryString");
var data_1 = require("../data");
var utils_1 = require("../utils");
exports.LEFT_AXIS_QUERY_KEY = 'left';
exports.RIGHT_AXIS_QUERY_KEY = 'right';
var LandingDisplayField;
(function (LandingDisplayField) {
    LandingDisplayField["ALL"] = "all";
    LandingDisplayField["FRONTEND_PAGELOAD"] = "frontend_pageload";
    LandingDisplayField["FRONTEND_OTHER"] = "frontend_other";
    LandingDisplayField["BACKEND"] = "backend";
    LandingDisplayField["MOBILE"] = "mobile";
})(LandingDisplayField = exports.LandingDisplayField || (exports.LandingDisplayField = {}));
exports.LANDING_DISPLAYS = [
    {
        label: 'All Transactions',
        field: LandingDisplayField.ALL,
    },
    {
        label: 'Frontend (Pageload)',
        field: LandingDisplayField.FRONTEND_PAGELOAD,
    },
    {
        label: 'Frontend (Other)',
        field: LandingDisplayField.FRONTEND_OTHER,
    },
    {
        label: 'Backend',
        field: LandingDisplayField.BACKEND,
    },
    {
        label: 'Mobile',
        field: LandingDisplayField.MOBILE,
        isShown: function (organization) {
            return organization.features.includes('performance-mobile-vitals');
        },
        alpha: true,
    },
];
function getCurrentLandingDisplay(location, projects, eventView) {
    var _a;
    var landingField = queryString_1.decodeScalar((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.landingDisplay);
    var display = exports.LANDING_DISPLAYS.find(function (_a) {
        var field = _a.field;
        return field === landingField;
    });
    if (display) {
        return display;
    }
    var defaultDisplayField = getDefaultDisplayFieldForPlatform(projects, eventView);
    var defaultDisplay = exports.LANDING_DISPLAYS.find(function (_a) {
        var field = _a.field;
        return field === defaultDisplayField;
    });
    return defaultDisplay || exports.LANDING_DISPLAYS[0];
}
exports.getCurrentLandingDisplay = getCurrentLandingDisplay;
function getChartWidth(chartData, refPixelRect) {
    var distance = refPixelRect ? refPixelRect.point2.x - refPixelRect.point1.x : 0;
    var chartWidth = chartData.length * distance;
    return {
        chartWidth: chartWidth,
    };
}
exports.getChartWidth = getChartWidth;
function getBackendFunction(functionName, organization) {
    switch (functionName) {
        case 'p75':
            return {
                kind: 'function',
                function: ['p75', 'transaction.duration', undefined, undefined],
            };
        case 'tpm':
            return { kind: 'function', function: ['tpm', '', undefined, undefined] };
        case 'failure_rate':
            return { kind: 'function', function: ['failure_rate', '', undefined, undefined] };
        case 'apdex':
            if (organization.features.includes('project-transaction-threshold')) {
                return {
                    kind: 'function',
                    function: ['apdex', '', undefined, undefined],
                };
            }
            return {
                kind: 'function',
                function: ['apdex', "" + organization.apdexThreshold, undefined, undefined],
            };
        default:
            throw new Error("Unsupported backend function: " + functionName);
    }
}
exports.getBackendFunction = getBackendFunction;
function getDefaultDisplayFieldForPlatform(projects, eventView) {
    var _a;
    var _b;
    if (!eventView) {
        return LandingDisplayField.ALL;
    }
    var projectIds = eventView.project;
    var performanceTypeToDisplay = (_a = {},
        _a[utils_1.PROJECT_PERFORMANCE_TYPE.ANY] = LandingDisplayField.ALL,
        _a[utils_1.PROJECT_PERFORMANCE_TYPE.FRONTEND] = LandingDisplayField.FRONTEND_PAGELOAD,
        _a[utils_1.PROJECT_PERFORMANCE_TYPE.BACKEND] = LandingDisplayField.BACKEND,
        _a);
    var performanceType = utils_1.platformToPerformanceType(projects, projectIds);
    var landingField = (_b = performanceTypeToDisplay[performanceType]) !== null && _b !== void 0 ? _b : LandingDisplayField.ALL;
    return landingField;
}
exports.getDefaultDisplayFieldForPlatform = getDefaultDisplayFieldForPlatform;
var backendCardDetails = function (organization) {
    return {
        p75: {
            title: locale_1.t('Duration (p75)'),
            tooltip: data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.P75),
            formatter: function (value) { return formatters_1.getDuration(value / 1000, value >= 1000 ? 3 : 0, true); },
        },
        tpm: {
            title: locale_1.t('Throughput'),
            tooltip: data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.THROUGHPUT),
            formatter: formatters_1.formatAbbreviatedNumber,
        },
        failure_rate: {
            title: locale_1.t('Failure Rate'),
            tooltip: data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.FAILURE_RATE),
            formatter: function (value) { return formatters_1.formatPercentage(value, 2); },
        },
        apdex: {
            title: locale_1.t('Apdex'),
            tooltip: organization.features.includes('project-transaction-threshold')
                ? data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.APDEX_NEW)
                : data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.APDEX),
            formatter: function (value) { return formatters_1.formatFloat(value, 4); },
        },
    };
};
exports.backendCardDetails = backendCardDetails;
function getDisplayAxes(options, location) {
    var leftDefault = options.find(function (opt) { return opt.isLeftDefault; }) || options[0];
    var rightDefault = options.find(function (opt) { return opt.isRightDefault; }) || options[1];
    var leftAxis = options.find(function (opt) { return opt.value === location.query[exports.LEFT_AXIS_QUERY_KEY]; }) || leftDefault;
    var rightAxis = options.find(function (opt) { return opt.value === location.query[exports.RIGHT_AXIS_QUERY_KEY]; }) ||
        rightDefault;
    return {
        leftAxis: leftAxis,
        rightAxis: rightAxis,
    };
}
exports.getDisplayAxes = getDisplayAxes;
//# sourceMappingURL=utils.jsx.map