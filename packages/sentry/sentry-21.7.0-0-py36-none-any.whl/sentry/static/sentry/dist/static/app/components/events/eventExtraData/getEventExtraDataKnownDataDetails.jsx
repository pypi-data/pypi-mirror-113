Object.defineProperty(exports, "__esModule", { value: true });
var locale_1 = require("app/locale");
var types_1 = require("./types");
var getEventExtraDataKnownDataDetails = function (data, key) {
    switch (key) {
        case types_1.EventExtraDataType.CRASHED_PROCESS:
            return {
                subject: locale_1.t('Crashed Process'),
                value: data[key],
            };
        default:
            return {
                subject: key,
                value: data[key],
            };
    }
};
exports.default = getEventExtraDataKnownDataDetails;
//# sourceMappingURL=getEventExtraDataKnownDataDetails.jsx.map