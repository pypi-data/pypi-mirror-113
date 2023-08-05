Object.defineProperty(exports, "__esModule", { value: true });
exports.ZOOM_KEYS = exports.VITAL_GROUPS = exports.PERCENTILE = exports.NUM_BUCKETS = void 0;
var tslib_1 = require("tslib");
var fields_1 = require("app/utils/discover/fields");
var constants_1 = require("app/utils/performance/vitals/constants");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
exports.NUM_BUCKETS = 100;
exports.PERCENTILE = 0.75;
/**
 * This defines the grouping for histograms. Histograms that are in the same group
 * will be queried together on initial load for alignment. However, the zoom controls
 * are defined for each measurement independently.
 */
var _VITAL_GROUPS = [
    {
        vitals: [fields_1.WebVital.FP, fields_1.WebVital.FCP, fields_1.WebVital.LCP],
        min: 0,
    },
    {
        vitals: [fields_1.WebVital.FID],
        min: 0,
        precision: 2,
    },
    {
        vitals: [fields_1.WebVital.CLS],
        min: 0,
        precision: 2,
    },
];
var _COLORS = tslib_1.__spreadArray([], tslib_1.__read(theme_1.default.charts.getColorPalette(_VITAL_GROUPS.reduce(function (count, _a) {
    var vitals = _a.vitals;
    return count + vitals.length;
}, 0) - 1))).reverse();
exports.VITAL_GROUPS = _VITAL_GROUPS.map(function (group) { return (tslib_1.__assign(tslib_1.__assign({}, group), { colors: _COLORS.splice(0, group.vitals.length) })); });
exports.ZOOM_KEYS = _VITAL_GROUPS.reduce(function (keys, _a) {
    var vitals = _a.vitals;
    vitals.forEach(function (vital) {
        var vitalSlug = constants_1.WEB_VITAL_DETAILS[vital].slug;
        keys.push(vitalSlug + "Start");
        keys.push(vitalSlug + "End");
    });
    return keys;
}, []);
//# sourceMappingURL=constants.jsx.map