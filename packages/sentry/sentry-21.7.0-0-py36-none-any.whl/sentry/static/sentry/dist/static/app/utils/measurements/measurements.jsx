Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var constants_1 = require("app/utils/performance/vitals/constants");
function measurementsFromDetails(details) {
    return Object.fromEntries(Object.entries(details).map(function (_a) {
        var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
        var newValue = {
            name: value.name,
            key: key,
        };
        return [key, newValue];
    }));
}
var MOBILE_MEASUREMENTS = measurementsFromDetails(constants_1.MOBILE_VITAL_DETAILS);
var WEB_MEASUREMENTS = measurementsFromDetails(constants_1.WEB_VITAL_DETAILS);
function Measurements(_a) {
    var organization = _a.organization, children = _a.children;
    var measurements = organization.features.includes('performance-mobile-vitals')
        ? tslib_1.__assign(tslib_1.__assign({}, WEB_MEASUREMENTS), MOBILE_MEASUREMENTS) : WEB_MEASUREMENTS;
    return <React.Fragment>{children({ measurements: measurements })}</React.Fragment>;
}
exports.default = Measurements;
//# sourceMappingURL=measurements.jsx.map