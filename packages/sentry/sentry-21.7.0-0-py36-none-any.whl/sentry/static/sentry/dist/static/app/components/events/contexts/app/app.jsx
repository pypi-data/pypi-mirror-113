Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var contextBlock_1 = tslib_1.__importDefault(require("app/components/events/contexts/contextBlock"));
var getUnknownData_1 = tslib_1.__importDefault(require("../getUnknownData"));
var getAppKnownData_1 = tslib_1.__importDefault(require("./getAppKnownData"));
var types_1 = require("./types");
var appKnownDataValues = [
    types_1.AppKnownDataType.ID,
    types_1.AppKnownDataType.START_TIME,
    types_1.AppKnownDataType.DEVICE_HASH,
    types_1.AppKnownDataType.IDENTIFIER,
    types_1.AppKnownDataType.NAME,
    types_1.AppKnownDataType.VERSION,
    types_1.AppKnownDataType.BUILD,
];
var appIgnoredDataValues = [];
var App = function (_a) {
    var data = _a.data, event = _a.event;
    return (<react_1.Fragment>
    <contextBlock_1.default data={getAppKnownData_1.default(event, data, appKnownDataValues)}/>
    <contextBlock_1.default data={getUnknownData_1.default(data, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(appKnownDataValues)), tslib_1.__read(appIgnoredDataValues)))}/>
  </react_1.Fragment>);
};
exports.default = App;
//# sourceMappingURL=app.jsx.map