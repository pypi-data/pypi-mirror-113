Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var utils_1 = require("app/utils");
var getDeviceKnownDataDetails_1 = tslib_1.__importDefault(require("./getDeviceKnownDataDetails"));
function getDeviceKnownData(event, data, deviceKnownDataValues) {
    var e_1, _a;
    var knownData = [];
    var dataKeys = deviceKnownDataValues.filter(function (deviceKnownDataValue) {
        return utils_1.defined(data[deviceKnownDataValue]);
    });
    try {
        for (var dataKeys_1 = tslib_1.__values(dataKeys), dataKeys_1_1 = dataKeys_1.next(); !dataKeys_1_1.done; dataKeys_1_1 = dataKeys_1.next()) {
            var key = dataKeys_1_1.value;
            var knownDataDetails = getDeviceKnownDataDetails_1.default(event, data, key);
            knownData.push(tslib_1.__assign(tslib_1.__assign({ key: key }, knownDataDetails), { meta: metaProxy_1.getMeta(data, key), subjectDataTestId: "device-context-" + key.toLowerCase() + "-value" }));
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
exports.default = getDeviceKnownData;
//# sourceMappingURL=getDeviceKnownData.jsx.map