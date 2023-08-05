Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var contextBlock_1 = tslib_1.__importDefault(require("app/components/events/contexts/contextBlock"));
var getUnknownData_1 = tslib_1.__importDefault(require("../getUnknownData"));
var getRuntimeKnownData_1 = tslib_1.__importDefault(require("./getRuntimeKnownData"));
var types_1 = require("./types");
var runtimeKnownDataValues = [types_1.RuntimeKnownDataType.NAME, types_1.RuntimeKnownDataType.VERSION];
var runtimeIgnoredDataValues = [types_1.RuntimeIgnoredDataType.BUILD];
var Runtime = function (_a) {
    var data = _a.data;
    return (<react_1.Fragment>
      <contextBlock_1.default data={getRuntimeKnownData_1.default(data, runtimeKnownDataValues)}/>
      <contextBlock_1.default data={getUnknownData_1.default(data, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(runtimeKnownDataValues)), tslib_1.__read(runtimeIgnoredDataValues)))}/>
    </react_1.Fragment>);
};
exports.default = Runtime;
//# sourceMappingURL=runtime.jsx.map