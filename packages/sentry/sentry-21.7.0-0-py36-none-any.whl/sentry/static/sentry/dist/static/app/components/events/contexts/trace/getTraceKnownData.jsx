Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var utils_1 = require("app/utils");
var getTraceKnownDataDetails_1 = tslib_1.__importDefault(require("./getTraceKnownDataDetails"));
var types_1 = require("./types");
function getTraceKnownData(data, traceKnownDataValues, event, organization) {
    var e_1, _a;
    var knownData = [];
    var dataKeys = traceKnownDataValues.filter(function (traceKnownDataValue) {
        if (traceKnownDataValue === types_1.TraceKnownDataType.TRANSACTION_NAME) {
            return event === null || event === void 0 ? void 0 : event.tags.find(function (tag) {
                return tag.key === 'transaction';
            });
        }
        return data[traceKnownDataValue];
    });
    try {
        for (var dataKeys_1 = tslib_1.__values(dataKeys), dataKeys_1_1 = dataKeys_1.next(); !dataKeys_1_1.done; dataKeys_1_1 = dataKeys_1.next()) {
            var key = dataKeys_1_1.value;
            var knownDataDetails = getTraceKnownDataDetails_1.default(data, key, event, organization);
            if ((knownDataDetails && !utils_1.defined(knownDataDetails.value)) || !knownDataDetails) {
                continue;
            }
            knownData.push(tslib_1.__assign(tslib_1.__assign({ key: key }, knownDataDetails), { meta: metaProxy_1.getMeta(data, key), subjectDataTestId: "trace-context-" + key.toLowerCase() + "-value" }));
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (dataKeys_1_1 && !dataKeys_1_1.done && (_a = dataKeys_1.return)) _a.call(dataKeys_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return knownData;
}
exports.default = getTraceKnownData;
//# sourceMappingURL=getTraceKnownData.jsx.map