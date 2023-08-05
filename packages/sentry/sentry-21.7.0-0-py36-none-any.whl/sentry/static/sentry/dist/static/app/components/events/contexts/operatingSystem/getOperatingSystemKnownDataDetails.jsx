Object.defineProperty(exports, "__esModule", { value: true });
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var types_1 = require("./types");
function getOperatingSystemKnownDataDetails(data, type) {
    switch (type) {
        case types_1.OperatingSystemKnownDataType.NAME:
            return {
                subject: locale_1.t('Name'),
                value: data.name,
            };
        case types_1.OperatingSystemKnownDataType.VERSION:
            return {
                subject: locale_1.t('Version'),
                value: "" + data.version + (data.build ? "(" + data.build + ")" : ''),
            };
        case types_1.OperatingSystemKnownDataType.KERNEL_VERSION:
            return {
                subject: locale_1.t('Kernel Version'),
                value: data.kernel_version,
            };
        case types_1.OperatingSystemKnownDataType.ROOTED:
            return {
                subject: locale_1.t('Rooted'),
                value: utils_1.defined(data.rooted) ? (data.rooted ? locale_1.t('yes') : locale_1.t('no')) : null,
            };
        default:
            return {
                subject: type,
                value: data[type] || null,
            };
    }
}
exports.default = getOperatingSystemKnownDataDetails;
//# sourceMappingURL=getOperatingSystemKnownDataDetails.jsx.map