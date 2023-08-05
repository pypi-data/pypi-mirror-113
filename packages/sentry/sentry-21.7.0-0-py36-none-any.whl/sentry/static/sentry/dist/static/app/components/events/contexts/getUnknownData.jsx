Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var startCase_1 = tslib_1.__importDefault(require("lodash/startCase"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
function getUnknownData(allData, knownKeys) {
    return Object.entries(allData)
        .filter(function (_a) {
        var _b = tslib_1.__read(_a, 1), key = _b[0];
        return key !== 'type' && key !== 'title';
    })
        .filter(function (_a) {
        var _b = tslib_1.__read(_a, 1), key = _b[0];
        return !knownKeys.includes(key);
    })
        .map(function (_a) {
        var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
        return ({
            key: key,
            value: value,
            subject: startCase_1.default(key),
            meta: metaProxy_1.getMeta(allData, key),
        });
    });
}
exports.default = getUnknownData;
//# sourceMappingURL=getUnknownData.jsx.map