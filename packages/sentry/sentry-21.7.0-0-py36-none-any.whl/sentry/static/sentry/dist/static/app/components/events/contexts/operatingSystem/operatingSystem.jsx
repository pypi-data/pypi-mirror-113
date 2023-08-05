Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var contextBlock_1 = tslib_1.__importDefault(require("app/components/events/contexts/contextBlock"));
var getUnknownData_1 = tslib_1.__importDefault(require("../getUnknownData"));
var getOperatingSystemKnownData_1 = tslib_1.__importDefault(require("./getOperatingSystemKnownData"));
var types_1 = require("./types");
var operatingSystemKnownDataValues = [
    types_1.OperatingSystemKnownDataType.NAME,
    types_1.OperatingSystemKnownDataType.VERSION,
    types_1.OperatingSystemKnownDataType.KERNEL_VERSION,
    types_1.OperatingSystemKnownDataType.ROOTED,
];
var operatingSystemIgnoredDataValues = [types_1.OperatingSystemIgnoredDataType.BUILD];
var OperatingSystem = function (_a) {
    var data = _a.data;
    return (<react_1.Fragment>
    <contextBlock_1.default data={getOperatingSystemKnownData_1.default(data, operatingSystemKnownDataValues)}/>
    <contextBlock_1.default data={getUnknownData_1.default(data, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(operatingSystemKnownDataValues)), tslib_1.__read(operatingSystemIgnoredDataValues)))}/>
  </react_1.Fragment>);
};
exports.default = OperatingSystem;
//# sourceMappingURL=operatingSystem.jsx.map