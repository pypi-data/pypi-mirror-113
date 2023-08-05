Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var contextBlock_1 = tslib_1.__importDefault(require("app/components/events/contexts/contextBlock"));
var utils_1 = require("app/utils");
var getEventExtraDataKnownData_1 = tslib_1.__importDefault(require("./getEventExtraDataKnownData"));
var EventDataContent = function (_a) {
    var data = _a.data, raw = _a.raw;
    if (!utils_1.defined(data)) {
        return null;
    }
    return <contextBlock_1.default data={getEventExtraDataKnownData_1.default(data)} raw={raw}/>;
};
exports.default = EventDataContent;
//# sourceMappingURL=eventDataContent.jsx.map