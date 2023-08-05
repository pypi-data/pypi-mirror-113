Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var contextBlock_1 = tslib_1.__importDefault(require("app/components/events/contexts/contextBlock"));
var getUnknownData_1 = tslib_1.__importDefault(require("../getUnknownData"));
var getGPUKnownData_1 = tslib_1.__importDefault(require("./getGPUKnownData"));
var types_1 = require("./types");
var gpuKnownDataValues = [
    types_1.GPUKnownDataType.NAME,
    types_1.GPUKnownDataType.VERSION,
    types_1.GPUKnownDataType.VENDOR_NAME,
    types_1.GPUKnownDataType.MEMORY,
    types_1.GPUKnownDataType.NPOT_SUPPORT,
    types_1.GPUKnownDataType.MULTI_THREAD_RENDERING,
    types_1.GPUKnownDataType.API_TYPE,
];
var gpuIgnoredDataValues = [];
var GPU = function (_a) {
    var data = _a.data;
    if (data.vendor_id > 0) {
        gpuKnownDataValues.unshift[types_1.GPUKnownDataType.VENDOR_ID];
    }
    if (data.id > 0) {
        gpuKnownDataValues.unshift[types_1.GPUKnownDataType.ID];
    }
    return (<react_1.Fragment>
      <contextBlock_1.default data={getGPUKnownData_1.default(data, gpuKnownDataValues)}/>
      <contextBlock_1.default data={getUnknownData_1.default(data, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(gpuKnownDataValues)), tslib_1.__read(gpuIgnoredDataValues)))}/>
    </react_1.Fragment>);
};
exports.default = GPU;
//# sourceMappingURL=gpu.jsx.map