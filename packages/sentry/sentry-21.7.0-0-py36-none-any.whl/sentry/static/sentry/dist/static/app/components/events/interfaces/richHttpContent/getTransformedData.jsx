Object.defineProperty(exports, "__esModule", { value: true });
var utils_1 = require("app/utils");
function getTransformedData(data) {
    if (Array.isArray(data)) {
        return data
            .filter(function (dataValue) {
            if (typeof dataValue === 'string') {
                return !!dataValue;
            }
            return utils_1.defined(dataValue);
        })
            .map(function (dataValue) {
            if (Array.isArray(dataValue)) {
                return dataValue;
            }
            if (typeof data === 'object') {
                return Object.keys(dataValue).flatMap(function (key) { return [key, dataValue[key]]; });
            }
            return dataValue;
        });
    }
    if (typeof data === 'object') {
        return Object.keys(data).map(function (key) { return [key, data[key]]; });
    }
    return [];
}
exports.default = getTransformedData;
//# sourceMappingURL=getTransformedData.jsx.map