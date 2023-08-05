Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var deviceName_1 = tslib_1.__importDefault(require("app/components/deviceName"));
var annotatedText_1 = tslib_1.__importDefault(require("app/components/events/meta/annotatedText"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var utils_1 = require("app/utils");
var EventTagsPillValue = function (_a) {
    var _b;
    var _c = _a.tag, key = _c.key, value = _c.value, meta = _a.meta, isRelease = _a.isRelease, streamPath = _a.streamPath, locationSearch = _a.locationSearch;
    var getContent = function () {
        return isRelease ? (<version_1.default version={String(value)} anchor={false} tooltipRawVersion truncate/>) : (<annotatedText_1.default value={utils_1.defined(value) && <deviceName_1.default value={String(value)}/>} meta={meta}/>);
    };
    var content = getContent();
    if (!((_b = meta === null || meta === void 0 ? void 0 : meta.err) === null || _b === void 0 ? void 0 : _b.length) && utils_1.defined(key)) {
        return <link_1.default to={{ pathname: streamPath, search: locationSearch }}>{content}</link_1.default>;
    }
    return content;
};
exports.default = EventTagsPillValue;
//# sourceMappingURL=eventTagsPillValue.jsx.map