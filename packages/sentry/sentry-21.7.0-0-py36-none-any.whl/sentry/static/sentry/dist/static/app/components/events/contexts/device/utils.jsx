Object.defineProperty(exports, "__esModule", { value: true });
exports.getInferredData = exports.commonDisplayResolutions = exports.formatStorage = exports.formatMemory = void 0;
var tslib_1 = require("tslib");
var utils_1 = require("app/utils");
var types_1 = require("./types");
function formatMemory(memory_size, free_memory, usable_memory) {
    if (!Number.isInteger(memory_size) ||
        memory_size <= 0 ||
        !Number.isInteger(free_memory) ||
        free_memory <= 0) {
        return null;
    }
    var memory = "Total: " + utils_1.formatBytesBase2(memory_size) + " / Free: " + utils_1.formatBytesBase2(free_memory);
    if (Number.isInteger(usable_memory) && usable_memory > 0) {
        memory = memory + " / Usable: " + utils_1.formatBytesBase2(usable_memory);
    }
    return memory;
}
exports.formatMemory = formatMemory;
function formatStorage(storage_size, free_storage, external_storage_size, external_free_storage) {
    if (!Number.isInteger(storage_size) || storage_size <= 0) {
        return null;
    }
    var storage = "Total: " + utils_1.formatBytesBase2(storage_size);
    if (Number.isInteger(free_storage) && free_storage > 0) {
        storage = storage + " / Free: " + utils_1.formatBytesBase2(free_storage);
    }
    if (Number.isInteger(external_storage_size) &&
        external_storage_size > 0 &&
        Number.isInteger(external_free_storage) &&
        external_free_storage > 0) {
        storage = storage + " (External Total: " + utils_1.formatBytesBase2(external_storage_size) + " / Free: " + utils_1.formatBytesBase2(external_free_storage) + ")";
    }
    return storage;
}
exports.formatStorage = formatStorage;
// List of common display resolutions taken from the source: https://en.wikipedia.org/wiki/Display_resolution#Common_display_resolutions
exports.commonDisplayResolutions = {
    '640x360': 'nHD',
    '800x600': 'SVGA',
    '1024x768': 'XGA',
    '1280x720': 'WXGA',
    '1280x800': 'WXGA',
    '1280x1024': 'SXGA',
    '1360x768': 'HD',
    '1366x768': 'HD',
    '1440x900': 'WXGA+',
    '1536x864': 'NA',
    '1600x900': 'HD+',
    '1680x1050': 'WSXGA+',
    '1920x1080': 'FHD',
    '1920x1200': 'WUXGA',
    '2048x1152': 'QWXGA',
    '2560x1080': 'N/A',
    '2560x1440': 'QHD',
    '3440x1440': 'N/A',
    '3840x2160': '4K UHD',
};
function getInferredData(data) {
    var _a, _b, _c;
    var screenResolution = data[types_1.DeviceKnownDataType.SCREEN_RESOLUTION];
    var screenWidth = data[types_1.DeviceKnownDataType.SCREEN_WIDTH_PIXELS];
    var screenHeight = data[types_1.DeviceKnownDataType.SCREEN_HEIGHT_PIXELS];
    if (screenResolution) {
        var displayResolutionDescription = exports.commonDisplayResolutions[screenResolution];
        var commonData = tslib_1.__assign(tslib_1.__assign({}, data), (_a = {}, _a[types_1.DeviceKnownDataType.SCREEN_RESOLUTION] = displayResolutionDescription
            ? screenResolution + " (" + displayResolutionDescription + ")"
            : screenResolution, _a));
        if (!utils_1.defined(screenWidth) && !utils_1.defined(screenHeight)) {
            var _d = tslib_1.__read(screenResolution.split('x'), 2), width = _d[0], height = _d[1];
            if (width && height) {
                return tslib_1.__assign(tslib_1.__assign({}, commonData), (_b = {}, _b[types_1.DeviceKnownDataType.SCREEN_WIDTH_PIXELS] = Number(width), _b[types_1.DeviceKnownDataType.SCREEN_HEIGHT_PIXELS] = Number(height), _b));
            }
        }
        return commonData;
    }
    if (utils_1.defined(screenWidth) && utils_1.defined(screenHeight)) {
        var displayResolution = screenWidth + "x" + screenHeight;
        var displayResolutionDescription = exports.commonDisplayResolutions[displayResolution];
        return tslib_1.__assign(tslib_1.__assign({}, data), (_c = {}, _c[types_1.DeviceKnownDataType.SCREEN_RESOLUTION] = displayResolutionDescription
            ? displayResolution + " (" + displayResolutionDescription + ")"
            : displayResolution, _c));
    }
    return data;
}
exports.getInferredData = getInferredData;
//# sourceMappingURL=utils.jsx.map