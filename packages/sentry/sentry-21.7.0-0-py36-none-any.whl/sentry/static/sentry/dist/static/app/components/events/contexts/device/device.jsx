Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var contextBlock_1 = tslib_1.__importDefault(require("app/components/events/contexts/contextBlock"));
var getUnknownData_1 = tslib_1.__importDefault(require("../getUnknownData"));
var getDeviceKnownData_1 = tslib_1.__importDefault(require("./getDeviceKnownData"));
var types_1 = require("./types");
var utils_1 = require("./utils");
var deviceKnownDataValues = [
    types_1.DeviceKnownDataType.NAME,
    types_1.DeviceKnownDataType.FAMILY,
    types_1.DeviceKnownDataType.CPU_DESCRIPTION,
    types_1.DeviceKnownDataType.ARCH,
    types_1.DeviceKnownDataType.BATTERY_LEVEL,
    types_1.DeviceKnownDataType.BATTERY_STATUS,
    types_1.DeviceKnownDataType.ORIENTATION,
    types_1.DeviceKnownDataType.MEMORY,
    types_1.DeviceKnownDataType.MEMORY_SIZE,
    types_1.DeviceKnownDataType.FREE_MEMORY,
    types_1.DeviceKnownDataType.USABLE_MEMORY,
    types_1.DeviceKnownDataType.LOW_MEMORY,
    types_1.DeviceKnownDataType.STORAGE_SIZE,
    types_1.DeviceKnownDataType.EXTERNAL_STORAGE_SIZE,
    types_1.DeviceKnownDataType.EXTERNAL_FREE_STORAGE,
    types_1.DeviceKnownDataType.STORAGE,
    types_1.DeviceKnownDataType.FREE_STORAGE,
    types_1.DeviceKnownDataType.SIMULATOR,
    types_1.DeviceKnownDataType.BOOT_TIME,
    types_1.DeviceKnownDataType.TIMEZONE,
    types_1.DeviceKnownDataType.DEVICE_TYPE,
    types_1.DeviceKnownDataType.ARCHS,
    types_1.DeviceKnownDataType.BRAND,
    types_1.DeviceKnownDataType.CHARGING,
    types_1.DeviceKnownDataType.CONNECTION_TYPE,
    types_1.DeviceKnownDataType.ID,
    types_1.DeviceKnownDataType.LANGUAGE,
    types_1.DeviceKnownDataType.MANUFACTURER,
    types_1.DeviceKnownDataType.ONLINE,
    types_1.DeviceKnownDataType.SCREEN_DENSITY,
    types_1.DeviceKnownDataType.SCREEN_DPI,
    types_1.DeviceKnownDataType.SCREEN_RESOLUTION,
    types_1.DeviceKnownDataType.SCREEN_HEIGHT_PIXELS,
    types_1.DeviceKnownDataType.SCREEN_WIDTH_PIXELS,
    types_1.DeviceKnownDataType.MODEL,
    types_1.DeviceKnownDataType.MODEL_ID,
    types_1.DeviceKnownDataType.RENDERED_MODEL,
];
var deviceIgnoredDataValues = [];
function Device(_a) {
    var data = _a.data, event = _a.event;
    var inferredData = utils_1.getInferredData(data);
    return (<react_1.Fragment>
      <contextBlock_1.default data={getDeviceKnownData_1.default(event, inferredData, deviceKnownDataValues)}/>
      <contextBlock_1.default data={getUnknownData_1.default(inferredData, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(deviceKnownDataValues)), tslib_1.__read(deviceIgnoredDataValues)))}/>
    </react_1.Fragment>);
}
exports.default = Device;
//# sourceMappingURL=device.jsx.map