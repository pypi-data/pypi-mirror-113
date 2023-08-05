var _a;
Object.defineProperty(exports, "__esModule", { value: true });
exports.API_INTERVAL_POINTS_MIN = exports.API_INTERVAL_POINTS_LIMIT = exports.TIME_WINDOWS = exports.TIME_OPTIONS = void 0;
var locale_1 = require("app/locale");
var types_1 = require("app/views/alerts/incidentRules/types");
exports.TIME_OPTIONS = [
    { label: locale_1.t('Last 6 hours'), value: types_1.TimePeriod.SIX_HOURS },
    { label: locale_1.t('Last 24 hours'), value: types_1.TimePeriod.ONE_DAY },
    { label: locale_1.t('Last 3 days'), value: types_1.TimePeriod.THREE_DAYS },
    { label: locale_1.t('Last 7 days'), value: types_1.TimePeriod.SEVEN_DAYS },
];
exports.TIME_WINDOWS = (_a = {},
    _a[types_1.TimePeriod.SIX_HOURS] = types_1.TimeWindow.ONE_HOUR * 6 * 60 * 1000,
    _a[types_1.TimePeriod.ONE_DAY] = types_1.TimeWindow.ONE_DAY * 60 * 1000,
    _a[types_1.TimePeriod.THREE_DAYS] = types_1.TimeWindow.ONE_DAY * 3 * 60 * 1000,
    _a[types_1.TimePeriod.SEVEN_DAYS] = types_1.TimeWindow.ONE_DAY * 7 * 60 * 1000,
    _a);
exports.API_INTERVAL_POINTS_LIMIT = 10000;
exports.API_INTERVAL_POINTS_MIN = 150;
//# sourceMappingURL=constants.jsx.map