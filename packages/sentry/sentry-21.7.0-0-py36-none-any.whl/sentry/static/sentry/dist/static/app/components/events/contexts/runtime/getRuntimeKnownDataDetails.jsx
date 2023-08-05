Object.defineProperty(exports, "__esModule", { value: true });
var locale_1 = require("app/locale");
var types_1 = require("./types");
function getRuntimeKnownDataDetails(data, type) {
    switch (type) {
        case types_1.RuntimeKnownDataType.NAME:
            return {
                subject: locale_1.t('Name'),
                value: data.name,
            };
        case types_1.RuntimeKnownDataType.VERSION:
            return {
                subject: locale_1.t('Version'),
                value: "" + data.version + (data.build ? "(" + data.build + ")" : ''),
            };
        default:
            return {
                subject: type,
                value: data[type],
            };
    }
}
exports.default = getRuntimeKnownDataDetails;
//# sourceMappingURL=getRuntimeKnownDataDetails.jsx.map