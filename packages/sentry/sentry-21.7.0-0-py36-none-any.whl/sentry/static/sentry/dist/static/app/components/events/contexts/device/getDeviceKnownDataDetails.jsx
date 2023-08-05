Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var deviceName_1 = tslib_1.__importDefault(require("app/components/deviceName"));
var fileSize_1 = tslib_1.__importDefault(require("app/components/fileSize"));
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var utils_2 = require("../utils");
var types_1 = require("./types");
var utils_3 = require("./utils");
function getDeviceKnownDataDetails(event, data, type) {
    switch (type) {
        case types_1.DeviceKnownDataType.NAME:
            return {
                subject: locale_1.t('Name'),
                value: data.name,
            };
        case types_1.DeviceKnownDataType.FAMILY:
            return {
                subject: locale_1.t('Family'),
                value: data.family,
            };
        case types_1.DeviceKnownDataType.MODEL_ID:
            return {
                subject: locale_1.t('Model Id'),
                value: data.model_id,
            };
        case types_1.DeviceKnownDataType.MODEL:
            return {
                subject: locale_1.t('Model'),
                value: typeof data.model === 'string' ? (<deviceName_1.default value={data.model + " " + ((data === null || data === void 0 ? void 0 : data.model_id) ? "(" + data.model_id + ")" : '')}/>) : undefined,
            };
        case types_1.DeviceKnownDataType.RENDERED_MODEL:
            return {
                subject: locale_1.t('Rendered Model'),
                value: data.renderedModel,
            };
        case types_1.DeviceKnownDataType.CPU_DESCRIPTION:
            return {
                subject: locale_1.t('CPU Description'),
                value: data.cpu_description,
            };
        case types_1.DeviceKnownDataType.ARCH:
            return {
                subject: locale_1.t('Architecture'),
                value: data.arch,
            };
        case types_1.DeviceKnownDataType.BATTERY_LEVEL:
            return {
                subject: locale_1.t('Battery Level'),
                value: utils_1.defined(data.battery_level) ? data.battery_level + "%" : undefined,
            };
        case types_1.DeviceKnownDataType.BATTERY_STATUS:
            return {
                subject: locale_1.t('Battery Status'),
                value: data.battery_status,
            };
        case types_1.DeviceKnownDataType.ORIENTATION:
            return {
                subject: locale_1.t('Orientation'),
                value: data.orientation,
            };
        case types_1.DeviceKnownDataType.MEMORY:
            var memory_size = data.memory_size, free_memory = data.free_memory, usable_memory = data.usable_memory;
            return {
                subject: locale_1.t('Memory'),
                value: memory_size && free_memory && usable_memory
                    ? utils_3.formatMemory(memory_size, free_memory, usable_memory)
                    : undefined,
            };
        case types_1.DeviceKnownDataType.STORAGE:
            var storage_size = data.storage_size, free_storage = data.free_storage, external_storage_size = data.external_storage_size, external_free_storage = data.external_free_storage;
            return {
                subject: locale_1.t('Capacity'),
                value: storage_size && free_storage && external_storage_size && external_free_storage
                    ? utils_3.formatStorage(storage_size, free_storage, external_storage_size, external_free_storage)
                    : undefined,
            };
        case types_1.DeviceKnownDataType.FREE_STORAGE: {
            return {
                subject: locale_1.t('Free Storage'),
                value: data.free_storage ? <fileSize_1.default bytes={data.free_storage}/> : undefined,
            };
        }
        case types_1.DeviceKnownDataType.STORAGE_SIZE: {
            return {
                subject: locale_1.t('Storage Size'),
                value: data.storage_size ? <fileSize_1.default bytes={data.storage_size}/> : undefined,
            };
        }
        case types_1.DeviceKnownDataType.EXTERNAL_STORAGE_SIZE: {
            return {
                subject: locale_1.t('External Storage Size'),
                value: data.external_storage_size ? (<fileSize_1.default bytes={data.external_storage_size}/>) : undefined,
            };
        }
        case types_1.DeviceKnownDataType.EXTERNAL_FREE_STORAGE: {
            return {
                subject: locale_1.t('External Free Storage'),
                value: data.external_free_storage ? (<fileSize_1.default bytes={data.external_free_storage}/>) : undefined,
            };
        }
        case types_1.DeviceKnownDataType.SIMULATOR:
            return {
                subject: locale_1.t('Simulator'),
                value: data.simulator,
            };
        case types_1.DeviceKnownDataType.BOOT_TIME:
            return {
                subject: locale_1.t('Boot Time'),
                value: utils_2.getRelativeTimeFromEventDateCreated(event.dateCreated, data.boot_time),
            };
        case types_1.DeviceKnownDataType.TIMEZONE:
            return {
                subject: locale_1.t('Timezone'),
                value: data.timezone,
            };
        case types_1.DeviceKnownDataType.DEVICE_TYPE:
            return {
                subject: locale_1.t('Device Type'),
                value: data.device_type,
            };
        case types_1.DeviceKnownDataType.ARCHS:
            return {
                subject: locale_1.t('Architectures'),
                value: data.archs,
            };
        case types_1.DeviceKnownDataType.BRAND:
            return {
                subject: locale_1.t('Brand'),
                value: data.brand,
            };
        case types_1.DeviceKnownDataType.CHARGING:
            return {
                subject: locale_1.t('Charging'),
                value: data.charging,
            };
        case types_1.DeviceKnownDataType.CONNECTION_TYPE:
            return {
                subject: locale_1.t('Connection Type'),
                value: data.connection_type,
            };
        case types_1.DeviceKnownDataType.ID:
            return {
                subject: locale_1.t('Id'),
                value: data.id,
            };
        case types_1.DeviceKnownDataType.LANGUAGE:
            return {
                subject: locale_1.t('Language'),
                value: utils_2.getFullLanguageDescription(data.language),
            };
        case types_1.DeviceKnownDataType.LOW_MEMORY:
            return {
                subject: locale_1.t('Low Memory'),
                value: data.low_memory,
            };
        case types_1.DeviceKnownDataType.FREE_MEMORY:
            return {
                subject: locale_1.t('Free Memory'),
                value: data.free_memory ? <fileSize_1.default bytes={data.free_memory}/> : undefined,
            };
        case types_1.DeviceKnownDataType.MEMORY_SIZE:
            return {
                subject: locale_1.t('Memory Size'),
                value: data.memory_size ? <fileSize_1.default bytes={data.memory_size}/> : undefined,
            };
        case types_1.DeviceKnownDataType.USABLE_MEMORY:
            return {
                subject: locale_1.t('Usable Memory'),
                value: data.usable_memory ? <fileSize_1.default bytes={data.usable_memory}/> : undefined,
            };
        case types_1.DeviceKnownDataType.MANUFACTURER:
            return {
                subject: locale_1.t('Manufacturer'),
                value: data.manufacturer,
            };
        case types_1.DeviceKnownDataType.ONLINE:
            return {
                subject: locale_1.t('Online'),
                value: data.online,
            };
        case types_1.DeviceKnownDataType.SCREEN_DENSITY:
            return {
                subject: locale_1.t('Screen Density'),
                value: data.screen_density,
            };
        case types_1.DeviceKnownDataType.SCREEN_DPI:
            return {
                subject: locale_1.t('Screen DPI'),
                value: data.screen_dpi,
            };
        case types_1.DeviceKnownDataType.SCREEN_HEIGHT_PIXELS:
            return {
                subject: locale_1.t('Screen Height Pixels'),
                value: data.screen_height_pixels,
            };
        case types_1.DeviceKnownDataType.SCREEN_RESOLUTION:
            return {
                subject: locale_1.t('Screen Resolution'),
                value: data.screen_resolution,
            };
        case types_1.DeviceKnownDataType.SCREEN_WIDTH_PIXELS:
            return {
                subject: locale_1.t('Screen Width Pixels'),
                value: data.screen_width_pixels,
            };
        default:
            return {
                subject: type,
                value: data[type],
            };
    }
}
exports.default = getDeviceKnownDataDetails;
//# sourceMappingURL=getDeviceKnownDataDetails.jsx.map