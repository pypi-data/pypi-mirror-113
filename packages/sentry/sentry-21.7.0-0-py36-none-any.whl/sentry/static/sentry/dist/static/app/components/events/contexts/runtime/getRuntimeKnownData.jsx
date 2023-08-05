Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var utils_1 = require("app/utils");
var getRuntimeKnownDataDetails_1 = tslib_1.__importDefault(require("./getRuntimeKnownDataDetails"));
function getRuntimeKnownData(data, runTimerKnownDataValues) {
    var e_1, _a;
    var knownData = [];
    var dataKeys = runTimerKnownDataValues.filter(function (runTimerKnownDataValue) {
        return utils_1.defined(data[runTimerKnownDataValue]);
    });
    try {
        for (var dataKeys_1 = tslib_1.__values(dataKeys), dataKeys_1_1 = dataKeys_1.next(); !dataKeys_1_1.done; dataKeys_1_1 = dataKeys_1.next()) {
            var key = dataKeys_1_1.value;
            var knownDataDetails = getRuntimeKnownDataDetails_1.default(data, key);
            knownData.push(tslib_1.__assign(tslib_1.__assign({ key: key }, knownDataDetails), { meta: metaProxy_1.getMeta(data, key) }));
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
exports.default = getRuntimeKnownData;
//# sourceMappingURL=getRuntimeKnownData.jsx.map