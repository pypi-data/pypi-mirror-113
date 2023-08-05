var _a;
Object.defineProperty(exports, "__esModule", { value: true });
exports.displayTypes = exports.DataSet = exports.DisplayType = void 0;
var locale_1 = require("app/locale");
var DisplayType;
(function (DisplayType) {
    DisplayType["AREA"] = "area";
    DisplayType["BAR"] = "bar";
    DisplayType["LINE"] = "line";
    DisplayType["TABLE"] = "table";
    DisplayType["WORLD_MAP"] = "world_map";
    DisplayType["BIG_NUMBER"] = "big_number";
    DisplayType["STACKED_AREA"] = "stacked_area";
})(DisplayType = exports.DisplayType || (exports.DisplayType = {}));
var DataSet;
(function (DataSet) {
    DataSet["EVENTS"] = "events";
    DataSet["METRICS"] = "metrics";
})(DataSet = exports.DataSet || (exports.DataSet = {}));
exports.displayTypes = (_a = {},
    _a[DisplayType.AREA] = locale_1.t('Area Chart'),
    _a[DisplayType.BAR] = locale_1.t('Bar Chart'),
    _a[DisplayType.LINE] = locale_1.t('Line Chart'),
    _a[DisplayType.TABLE] = locale_1.t('Table'),
    _a[DisplayType.WORLD_MAP] = locale_1.t('World Map'),
    _a[DisplayType.BIG_NUMBER] = locale_1.t('Big Number'),
    _a);
//# sourceMappingURL=utils.jsx.map